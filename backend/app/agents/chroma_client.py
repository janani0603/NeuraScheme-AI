import logging
from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config.settings import settings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "schemes"

_client: Optional[chromadb.PersistentClient] = None
_collection = None


def get_chroma_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_chroma_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def chroma_query(query_vector: list, n_results: int = 100, where: Optional[dict] = None) -> list:
    """
    Query ChromaDB and return list of metadata dicts with distance scores.
    """
    collection = get_chroma_collection()

    count = collection.count()
    if count == 0:
        logger.warning("ChromaDB collection is empty — index not built yet")
        return []

    n_results = min(n_results, count)

    kwargs = {
        "query_embeddings": [query_vector],
        "n_results": n_results,
        "include": ["metadatas", "documents", "distances"],
    }
    if where:
        kwargs["where"] = where

    try:
        results = collection.query(**kwargs)
    except Exception as e:
        logger.warning(f"ChromaDB query failed: {e}")
        return []

    hits = []
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for slug, meta, dist in zip(ids, metadatas, distances):
        # cosine distance → similarity score (0–1)
        similarity = round(1 - dist, 4)
        hits.append({
            "slug": slug,
            "vector_score": similarity,
            **meta,
        })

    return hits


def chroma_count() -> int:
    return get_chroma_collection().count()
