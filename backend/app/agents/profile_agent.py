from typing import TypedDict, Optional


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

    # Normalize boolean flags
    bool_fields = ["is_student", "is_farmer", "is_business_owner", "has_disability"]
    for field in bool_fields:
        profile[field] = bool(profile.get(field, False))

    # Calculate completeness
    scored_fields = ["state", "gender", "occupation", "education", "annual_income", "category", "age"]
    filled = sum(1 for f in scored_fields if profile.get(f) not in (None, "", 0))
    completeness = round(filled / len(scored_fields), 2)

    # Profile is valid if at least 2 fields are filled
    profile_valid = filled >= 2

    return {
        **state,
        "profile": profile,
        "profile_valid": profile_valid,
        "profile_completeness": completeness,
        "error": None if profile_valid else "Profile has insufficient information for recommendations",
    }
