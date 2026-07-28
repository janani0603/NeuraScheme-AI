import asyncio
import logging
from app.agents.profile_agent import AgentState
from app.agents.embedding_model import embed_text
from app.agents.chroma_client import chroma_query, chroma_count
from app.database.connection import db

logger = logging.getLogger(__name__)

VECTOR_CANDIDATES = 100
FALLBACK_CANDIDATES = 150


OCCUPATION_KEYWORD_MAP = {
    "business owner": "entrepreneur business msme startup",
    "government employee": "government employee service",
    "private employee": "employee worker skills employment",
    "self employed": "self employed business msme",
    "homemaker": "women empowerment welfare",
    "retired": "senior citizen pension welfare",
    "unemployed": "employment skills training",
}


def _build_query_text(profile: dict) -> str:
    parts = []
    occupation = (profile.get("occupation") or "").lower().strip()
    if occupation:
        parts.append(OCCUPATION_KEYWORD_MAP.get(occupation, occupation))
    if profile.get("education"):
        parts.append(profile["education"])
    if profile.get("state"):
        parts.append(profile["state"])
    if profile.get("category"):
        parts.append(profile["category"])
    if profile.get("is_student"):
        parts.append("student scholarship education")
    if profile.get("is_farmer"):
        parts.append("farmer agriculture kisan")
    if profile.get("is_business_owner"):
        parts.append("entrepreneur business msme startup")
    if profile.get("has_disability"):
        parts.append("disability pwd divyang")
    if profile.get("gender") == "female":
        parts.append("women empowerment mahila")
    return " ".join(parts) if parts else "government welfare scheme"


async def retrieval_agent(state: AgentState) -> AgentState:
    if not state.get("profile_valid"):
        logger.warning("Retrieval agent: profile invalid, skipping")
        return {**state, "candidates": []}

    profile = state["profile"]
    query_text = _build_query_text(profile)
    logger.info(f"Retrieval agent: query='{query_text[:80]}'")

    # ── Step 1: ChromaDB semantic search ──────────────────────────────────────
    try:
        loop = asyncio.get_event_loop()
        count = await asyncio.wait_for(
            loop.run_in_executor(None, chroma_count), timeout=5.0
        )
        logger.info(f"Retrieval agent: ChromaDB count={count}")
        if count > 0:
            query_vector = await asyncio.wait_for(
                loop.run_in_executor(None, embed_text, query_text), timeout=20.0
            )
            chroma_hits = await asyncio.wait_for(
                loop.run_in_executor(None, chroma_query, query_vector, VECTOR_CANDIDATES, None),
                timeout=10.0
            )
            if chroma_hits:
                slugs = [h["slug"] for h in chroma_hits]
                slug_to_score = {h["slug"]: h["vector_score"] for h in chroma_hits}
                cursor = db["schemes"].find({"slug": {"$in": slugs}})
                docs = await cursor.to_list(length=VECTOR_CANDIDATES)
                for doc in docs:
                    doc["vector_score"] = slug_to_score.get(doc.get("slug", ""), 0.0)
                slug_order = {slug: i for i, slug in enumerate(slugs)}
                docs.sort(key=lambda d: slug_order.get(d.get("slug", ""), 999))
                logger.info(f"ChromaDB returned {len(docs)} candidates")
                return {**state, "candidates": docs}
    except asyncio.TimeoutError:
        logger.warning("Retrieval agent: ChromaDB timed out, falling back to MongoDB")
    except Exception as e:
        logger.warning(f"Retrieval agent: ChromaDB failed ({e}), falling back to MongoDB")

    # ── Step 2: MongoDB fallback ───────────────────────────────────────────────
    candidates = await _fallback_search(profile)
    return {**state, "candidates": candidates}


async def _fallback_search(profile: dict) -> list:
    """MongoDB fallback when ChromaDB is unavailable."""
    conditions = []
    keywords = []
    occupation = (profile.get("occupation") or "").lower().strip()

    if profile.get("is_student") or occupation == "student":
        keywords += ["student", "scholarship"]
    if profile.get("is_farmer") or occupation == "farmer":
        keywords += ["farmer", "agriculture"]
    if profile.get("is_business_owner") or occupation in ("business owner", "entrepreneur"):
        keywords += ["entrepreneur", "msme", "business"]
    if occupation == "government employee":
        keywords += ["government", "employee", "service"]
    if occupation == "private employee":
        keywords += ["employee", "worker", "labour"]
    if occupation in ("self employed", "self-employed"):
        keywords += ["self employed", "msme", "business"]
    if occupation == "unemployed":
        keywords += ["employment", "skills", "training"]
    if occupation == "homemaker":
        keywords += ["women", "empowerment", "welfare"]
    if occupation == "retired":
        keywords += ["senior citizen", "pension"]
    if occupation and not keywords:
        keywords.append(occupation)

    if keywords:
        search_str = "|".join(keywords)
        conditions.append({"$or": [
            {"scheme_name": {"$regex": search_str, "$options": "i"}},
            {"eligibility": {"$regex": search_str, "$options": "i"}},
            {"tags": {"$regex": search_str, "$options": "i"}},
        ]})

    state = (profile.get("state") or "").strip()
    if state:
        conditions.append({"$or": [
            {"level": {"$regex": "^central$", "$options": "i"}},
            {"eligibility": {"$regex": state, "$options": "i"}},
            {"details": {"$regex": state, "$options": "i"}},
        ]})

    category = (profile.get("category") or "").strip()
    if category and category.lower() != "general":
        conditions.append({"$or": [
            {"eligibility": {"$regex": category, "$options": "i"}},
            {"tags": {"$regex": category, "$options": "i"}},
        ]})

    query = {"$and": conditions} if len(conditions) > 1 else conditions[0] if conditions else {}

    logger.info(f"MongoDB fallback: {len(conditions)} conditions")
    cursor = db["schemes"].find(query).limit(FALLBACK_CANDIDATES)
    candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    if not candidates:
        logger.warning("MongoDB fallback: no results with filters, fetching all")
        cursor = db["schemes"].find({}).limit(FALLBACK_CANDIDATES)
        candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    logger.info(f"MongoDB fallback returned {len(candidates)} candidates")
    return candidates
