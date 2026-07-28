from typing import TypedDict, Optional
import logging

logger = logging.getLogger(__name__)


class AgentState(TypedDict, total=False):
    # Input
    user_id: str
    profile: dict
    question: Optional[str]
    conversation_id: Optional[str]

    # Pipeline outputs
    profile_valid: bool
    profile_completeness: float
    candidates: list
    scored_schemes: list
    ranked_schemes: list
    explanations: dict        # slug -> explanation string
    final_recommendations: list
    assistant_response: str
    error: Optional[str]

    # Deadline agent
    deadlines: list
    urgent_count: int

    # Document checker agent
    document_check: dict

    # Comparison agent
    comparison: dict


def profile_agent(state: AgentState) -> AgentState:
    """
    Validates and normalizes the user profile.
    Sets profile_valid = False if critical fields are missing.
    """
    profile = state.get("profile", {})

    # Normalize string fields to lowercase stripped
    str_fields = ["state", "gender", "occupation", "education", "category"]
    for field in str_fields:
        if profile.get(field):
            profile[field] = str(profile[field]).strip().lower()

    # Normalize numeric fields
    if profile.get("age") is not None:
        try:
            profile["age"] = int(profile["age"])
        except (ValueError, TypeError):
            profile["age"] = None

    if profile.get("annual_income") is not None:
        try:
            profile["annual_income"] = float(profile["annual_income"])
        except (ValueError, TypeError):
            profile["annual_income"] = None

    # Normalize boolean flags
    bool_fields = ["is_student", "is_farmer", "is_business_owner", "has_disability"]
    for field in bool_fields:
        profile[field] = bool(profile.get(field, False))

    # Calculate completeness — annual_income=0 is valid (unemployed), age=0 is not
    def _is_filled(field, val):
        if val is None or val == "":
            return False
        if field == "age" and val == 0:
            return False
        return True

    scored_fields = ["state", "gender", "occupation", "education", "annual_income", "category", "age"]
    filled = sum(1 for f in scored_fields if _is_filled(f, profile.get(f)))
    completeness = round(filled / len(scored_fields), 2)

    # Valid if at least one meaningful field (occupation/income/category) is present
    meaningful_fields = ["occupation", "annual_income", "category", "is_student", "is_farmer", "is_business_owner"]
    has_meaningful = any(
        profile.get(f) not in (None, "", False)
        for f in meaningful_fields
    )
    profile_valid = filled >= 2 and has_meaningful

    logger.info(f"Profile agent: valid={profile_valid}, completeness={completeness}, filled={filled}")

    return {
        **state,
        "profile": profile,
        "profile_valid": profile_valid,
        "profile_completeness": completeness,
        "error": None if profile_valid else "Profile has insufficient information for recommendations",
    }
