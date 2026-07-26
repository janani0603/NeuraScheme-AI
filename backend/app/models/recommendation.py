from datetime import datetime, UTC
from typing import List


def new_recommendation_document(
    user_id: str,
    scheme_id: str,
    scheme_name: str,
    slug: str,
    eligibility_score: float,
    confidence_score: float,
    matched_conditions: List[str],
    missing_conditions: List[str],
    explanation: str,
) -> dict:
    return {
        "userId": user_id,
        "schemeId": scheme_id,
        "scheme_name": scheme_name,
        "slug": slug,
        "eligibility_score": eligibility_score,
        "confidence_score": confidence_score,
        "matched_conditions": matched_conditions,
        "missing_conditions": missing_conditions,
        "explanation": explanation,
        "generatedAt": datetime.now(UTC),
    }
