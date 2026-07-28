import logging
from app.agents.profile_agent import AgentState
from app.services.eligibility_service import score_scheme

logger = logging.getLogger(__name__)

MIN_SCORE = 35.0


async def eligibility_agent(state: AgentState) -> AgentState:
    candidates = state.get("candidates", [])
    profile = state.get("profile", {})

    if not candidates:
        return {**state, "scored_schemes": []}

    scored = []
    for scheme in candidates:
        result = score_scheme(scheme, profile)
        if result["eligibility_score"] >= MIN_SCORE:
            scored.append({
                "scheme": scheme,
                "eligibility_score": round(result["eligibility_score"], 1),
                "confidence_score": result["confidence_score"],
                "matched_conditions": result["matched_conditions"],
                "missing_conditions": result["missing_conditions"],
                "vector_score": scheme.get("vector_score", 0.0),
            })

    scored.sort(key=lambda x: x["eligibility_score"], reverse=True)
    logger.info(f"Eligibility agent scored {len(scored)} schemes above threshold")
    return {**state, "scored_schemes": scored}
