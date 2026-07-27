import logging
from typing import Optional
from app.agents.profile_agent import AgentState
from app.agents.embedding_model import embed_text
from app.agents.chroma_client import chroma_query, chroma_count
from app.database.connection import db

logger = logging.getLogger(__name__)

VECTOR_CANDIDATES = 100
FALLBACK_CANDIDATES = 150


def _build_query_text(profile: dict) -> str:
    parts = []
    if profile.get("occupation"):
        parts.append(profile["occupation"])
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


def _build_chroma_filter(profile: dict) -> Optional[dict]:
    """
    Build a ChromaDB metadata pre-filter to narrow candidates before vector search.
    Only filters on level (Central always included).
    Returns None if no useful filter can be built.
    """
    state = (profile.get("state") or "").strip().lower()
    if not state:
        return None

    # Include Central schemes always + state-specific schemes
    # ChromaDB $or filter syntax
    return {
        "$or": [
            {"level": {"$eq": "Central"}},
            {"level": {"$eq": "State"}},
        ]
    }


async def retrieval_agent(state: AgentState) -> AgentState:
    """
    Retrieves candidate schemes using ChromaDB semantic search.
    Falls back to MongoDB text search if ChromaDB is empty or unavailable.
    """
    if not state.get("profile_valid"):
        return {**state, "candidates": []}

    profile = state["profile"]
    query_text = _build_query_text(profile)

    # ── Step 1: ChromaDB semantic search ──────────────────────────────────────
    try:
        if chroma_count() > 0:
            query_vector = embed_text(query_text)
            where_filter = _build_chroma_filter(profile)

            chroma_hits = chroma_query(
                query_vector=query_vector,
                n_results=VECTOR_CANDIDATES,
                where=where_filter,
            )

            if chroma_hits:
                # Fetch full scheme documents from MongoDB by slug
                slugs = [h["slug"] for h in chroma_hits]
                slug_to_score = {h["slug"]: h["vector_score"] for h in chroma_hits}

                cursor = db["schemes"].find({"slug": {"$in": slugs}})
                docs = await cursor.to_list(length=VECTOR_CANDIDATES)

                # Attach vector_score to each document
                for doc in docs:
                    doc["vector_score"] = slug_to_score.get(doc.get("slug", ""), 0.0)

                # Preserve ChromaDB ranking order
                slug_order = {slug: i for i, slug in enumerate(slugs)}
                docs.sort(key=lambda d: slug_order.get(d.get("slug", ""), 999))

                logger.info(f"ChromaDB returned {len(docs)} candidates")
                return {**state, "candidates": docs}

    except Exception as e:
        logger.warning(f"ChromaDB search failed, falling back to MongoDB text search: {e}")

    # ── Step 2: MongoDB text search fallback ──────────────────────────────────
    candidates = await _fallback_search(profile)
    return {**state, "candidates": candidates}


async def _fallback_search(profile: dict) -> list:
    """MongoDB regex/text search fallback when ChromaDB is unavailable."""
    query = {}
    keywords = []

    if profile.get("is_student"):
        keywords += ["student", "scholarship"]
    if profile.get("is_farmer"):
        keywords += ["farmer", "agriculture"]
    if profile.get("is_business_owner"):
        keywords += ["entrepreneur", "msme"]
    if profile.get("occupation"):
        keywords.append(profile["occupation"])

    if keywords:
        search_str = "|".join(keywords)
        query["$or"] = [
            {"scheme_name": {"$regex": search_str, "$options": "i"}},
            {"eligibility": {"$regex": search_str, "$options": "i"}},
            {"tags": {"$regex": search_str, "$options": "i"}},
        ]

    cursor = db["schemes"].find(query).limit(FALLBACK_CANDIDATES)
    candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    if not candidates:
        cursor = db["schemes"].find({}).limit(FALLBACK_CANDIDATES)
        candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    logger.info(f"MongoDB fallback returned {len(candidates)} candidates")
    return candidates
