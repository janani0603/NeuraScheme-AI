import logging
from app.agents.profile_agent import AgentState
from app.agents.embedding_model import embed_text
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


async def retrieval_agent(state: AgentState) -> AgentState:
    """
    Performs semantic search using MongoDB Atlas Vector Search.
    Falls back to text search if no embeddings are available.
    """
    if not state.get("profile_valid"):
        return {**state, "candidates": []}

    profile = state["profile"]
    query_text = _build_query_text(profile)

    try:
        query_vector = embed_text(query_text)

        # MongoDB Atlas Vector Search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "scheme_vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": VECTOR_CANDIDATES * 2,
                    "limit": VECTOR_CANDIDATES,
                }
            },
            {
                "$addFields": {
                    "vector_score": {"$meta": "vectorSearchScore"}
                }
            },
        ]

        cursor = db["schemes"].aggregate(pipeline)
        candidates = await cursor.to_list(length=VECTOR_CANDIDATES)

        if candidates:
            logger.info(f"Vector search returned {len(candidates)} candidates")
            return {**state, "candidates": candidates}

    except Exception as e:
        logger.warning(f"Vector search failed, falling back to text search: {e}")

    # Fallback — broad text/filter search
    candidates = await _fallback_search(profile)
    return {**state, "candidates": candidates}


async def _fallback_search(profile: dict) -> list:
    """Text search fallback when vector search is unavailable."""
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
        query["$text"] = {"$search": " ".join(keywords)}

    cursor = db["schemes"].find(query).limit(FALLBACK_CANDIDATES)
    candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    # If still empty, return a broad sample
    if not candidates:
        cursor = db["schemes"].find({}).limit(FALLBACK_CANDIDATES)
        candidates = await cursor.to_list(length=FALLBACK_CANDIDATES)

    return candidates
