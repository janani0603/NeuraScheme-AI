from datetime import datetime, UTC
from typing import List


def new_scheme_document(
    scheme_name: str,
    slug: str,
    details: str,
    benefits: str,
    eligibility: str,
    application: str,
    documents: str,
    level: str,
    scheme_category: List[str],
    tags: List[str],
    search_text: str,
) -> dict:
    now = datetime.now(UTC)
    return {
        "scheme_name": scheme_name,
        "slug": slug,
        "details": details,
        "benefits": benefits,
        "eligibility": eligibility,
        "application": application,
        "documents": documents,
        "level": level,
        "schemeCategory": scheme_category,
        "tags": tags,
        "search_text": search_text,
        "embedding": None,
        "createdAt": now,
        "updatedAt": now,
    }
