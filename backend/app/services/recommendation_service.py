from datetime import datetime, UTC
from typing import Optional
from bson import ObjectId

from app.database.connection import db
from app.models.recommendation import new_recommendation_document
from app.services.eligibility_service import score_scheme, _profile_completeness

# Minimum eligibility score to include in results
MIN_SCORE = 40.0
# Max candidates to score (pre-filter before scoring)
CANDIDATE_LIMIT = 200


async def _get_candidates(profile: dict) -> list:
    """
    Broad pre-filter from MongoDB to get candidate schemes before scoring.
    Uses $or so we cast a wide net.
    """
    conditions = []

    # Central schemes are always candidates
    conditions.append({"level": {"$regex": "^central$", "$options": "i"}})

    # State-specific schemes
    state = profile.get("state")
    if state:
        conditions.append({"$text": {"$search": state}})

    # Occupation / profile flag keywords
    keywords = []
    if profile.get("is_student"):
        keywords += ["student", "scholarship", "education"]
    if profile.get("is_farmer"):
        keywords += ["farmer", "agriculture", "kisan"]
    if profile.get("is_business_owner"):
        keywords += ["entrepreneur", "msme", "business"]
    if profile.get("has_disability"):
        keywords += ["disability", "pwd"]
    if profile.get("occupation"):
        keywords.append(profile["occupation"])

    if keywords:
        conditions.append({"$text": {"$search": " ".join(keywords)}})

    query = {"$or": conditions} if conditions else {}

    cursor = db["schemes"].find(query).limit(CANDIDATE_LIMIT)
    return await cursor.to_list(length=CANDIDATE_LIMIT)


async def generate_recommendations(profile: dict, user_id: Optional[str] = None) -> dict:
    candidates = await _get_candidates(profile)

    # If too few candidates, fall back to all schemes (paginated)
    if len(candidates) < 20:
        cursor = db["schemes"].find({}).limit(CANDIDATE_LIMIT)
        candidates = await cursor.to_list(length=CANDIDATE_LIMIT)

    # Score every candidate
    scored = []
    for scheme in candidates:
        result = score_scheme(scheme, profile)
        if result["eligibility_score"] >= MIN_SCORE:
            scored.append({
                "id": str(scheme["_id"]),
                "scheme_name": scheme.get("scheme_name", ""),
                "slug": scheme.get("slug", ""),
                "level": scheme.get("level", ""),
                "schemeCategory": scheme.get("schemeCategory", []),
                "tags": scheme.get("tags", []),
                "benefits": scheme.get("benefits", ""),
                "documents": scheme.get("documents", ""),
                **result,
                "generatedAt": datetime.now(UTC).isoformat(),
            })

    # Sort by eligibility_score descending
    scored.sort(key=lambda x: x["eligibility_score"], reverse=True)

    # Save to recommendations collection if user is logged in
    if user_id:
        await db["recommendations"].delete_many({"userId": user_id})
        if scored:
            docs = [
                new_recommendation_document(
                    user_id=user_id,
                    scheme_id=r["id"],
                    scheme_name=r["scheme_name"],
                    slug=r["slug"],
                    eligibility_score=r["eligibility_score"],
                    confidence_score=r["confidence_score"],
                    matched_conditions=r["matched_conditions"],
                    missing_conditions=r["missing_conditions"],
                    explanation=r["explanation"],
                )
                for r in scored[:50]  # store top 50
            ]
            await db["recommendations"].insert_many(docs)

    completeness = _profile_completeness(profile)

    return {
        "total": len(scored),
        "profile_completeness": round(completeness * 100, 1),
        "recommendations": scored[:50],
    }


async def get_user_recommendations(user_id: str) -> dict:
    cursor = db["recommendations"].find(
        {"userId": user_id}
    ).sort("eligibility_score", -1)

    docs = await cursor.to_list(length=50)

    results = [
        {
            "id": str(d["_id"]),
            "scheme_name": d.get("scheme_name", ""),
            "slug": d.get("slug", ""),
            "level": "",
            "schemeCategory": [],
            "tags": [],
            "benefits": "",
            "documents": "",
            "eligibility_score": d.get("eligibility_score", 0),
            "confidence_score": d.get("confidence_score", 0),
            "matched_conditions": d.get("matched_conditions", []),
            "missing_conditions": d.get("missing_conditions", []),
            "explanation": d.get("explanation", ""),
            "generatedAt": d["generatedAt"].isoformat() if d.get("generatedAt") else "",
        }
        for d in docs
    ]

    return {
        "total": len(results),
        "profile_completeness": 0,
        "recommendations": results,
    }
