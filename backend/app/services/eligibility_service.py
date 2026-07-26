from typing import Optional


# ── Occupation → Tag/Category keyword mapping ─────────────────────────────────

OCCUPATION_TAG_MAP = {
    "student":      ["student", "scholarship", "education", "school", "fellowship"],
    "farmer":       ["farmer", "agriculture", "farming", "crop", "irrigation", "kisan"],
    "entrepreneur": ["entrepreneurship", "entrepreneur", "startup", "business", "msme", "msmes"],
    "business":     ["business", "entrepreneurship", "msme", "msmes", "loan"],
    "labour":       ["labour", "labor", "worker", "construction worker", "building worker"],
    "teacher":      ["education", "teacher", "training", "school"],
    "doctor":       ["health", "medical", "wellness", "doctor"],
    "engineer":     ["skills", "employment", "technology", "it"],
    "unemployed":   ["employment", "skills", "training", "loan"],
    "self-employed":["self employed", "business", "msme", "loan"],
    "retired":      ["senior citizen", "pension", "welfare"],
    "homemaker":    ["women", "empowerment", "welfare", "child"],
}

OCCUPATION_CATEGORY_MAP = {
    "student":      ["education & learning"],
    "farmer":       ["agriculture", "rural & environment"],
    "entrepreneur": ["business & entrepreneurship"],
    "business":     ["business & entrepreneurship", "banking"],
    "labour":       ["social welfare & empowerment", "skills & employment"],
    "teacher":      ["education & learning"],
    "doctor":       ["health & wellness"],
    "engineer":     ["skills & employment", "it & communications"],
    "unemployed":   ["skills & employment"],
    "self-employed":["business & entrepreneurship"],
    "retired":      ["social welfare & empowerment"],
    "homemaker":    ["women and child", "social welfare & empowerment"],
}

EDUCATION_TAG_MAP = {
    "10th":         ["school", "student"],
    "12th":         ["school", "student", "scholarship"],
    "diploma":      ["skills", "training", "student"],
    "graduate":     ["student", "scholarship", "education", "fellowship"],
    "post graduate":["research", "fellowship", "scholarship"],
    "phd":          ["research", "fellowship", "science"],
}

CATEGORY_TAG_MAP = {
    "sc":  ["scheduled caste", "sc", "dalit"],
    "st":  ["scheduled tribe", "st", "tribal"],
    "obc": ["obc", "other backward class"],
    "ews": ["ews", "bpl", "economically weaker"],
    "general": [],
}


def _contains_any(text: str, keywords: list) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _profile_completeness(profile: dict) -> float:
    fields = [
        "state", "gender", "occupation", "education",
        "annual_income", "category", "age",
    ]
    filled = sum(1 for f in fields if profile.get(f))
    return round(filled / len(fields), 2)


def score_scheme(scheme: dict, profile: dict) -> dict:
    """
    Returns eligibility_score, confidence_score, matched_conditions,
    missing_conditions, explanation for one scheme against a user profile.
    """
    matched = []
    missing = []

    scheme_text = (
        scheme.get("eligibility", "") + " " +
        scheme.get("details", "") + " " +
        scheme.get("benefits", "")
    ).lower()

    tags_lower = [t.lower() for t in scheme.get("tags", [])]
    cats_lower = [c.lower() for c in scheme.get("schemeCategory", [])]
    combined_text = scheme_text + " " + " ".join(tags_lower) + " " + " ".join(cats_lower)

    scores = {}

    # ── 1. State Match (25%) ──────────────────────────────────────────────────
    state = (profile.get("state") or "").lower()
    scheme_level = scheme.get("level", "").lower()

    if scheme_level == "central":
        matched.append("Central scheme — open to all states")
        scores["state"] = 1.0
    elif state and state in combined_text:
        matched.append(f"State match: {profile['state']}")
        scores["state"] = 1.0
    elif state:
        missing.append(f"Scheme may be state-specific (your state: {profile['state']})")
        scores["state"] = 0.3
    else:
        scores["state"] = 0.5  # unknown state, neutral

    # ── 2. Occupation Match (20%) ─────────────────────────────────────────────
    occupation = (profile.get("occupation") or "").lower().strip()
    occ_tags = []
    occ_cats = []
    for key in OCCUPATION_TAG_MAP:
        if key in occupation or occupation in key:
            occ_tags = OCCUPATION_TAG_MAP[key]
            occ_cats = OCCUPATION_CATEGORY_MAP.get(key, [])
            break

    # Also handle boolean flags
    if profile.get("is_student"):
        occ_tags += OCCUPATION_TAG_MAP["student"]
        occ_cats += OCCUPATION_CATEGORY_MAP["student"]
    if profile.get("is_farmer"):
        occ_tags += OCCUPATION_TAG_MAP["farmer"]
        occ_cats += OCCUPATION_CATEGORY_MAP["farmer"]
    if profile.get("is_business_owner"):
        occ_tags += OCCUPATION_TAG_MAP["entrepreneur"]
        occ_cats += OCCUPATION_CATEGORY_MAP["entrepreneur"]

    if occ_tags and (_contains_any(combined_text, occ_tags) or
                     any(c in cats_lower for c in occ_cats)):
        matched.append(f"Occupation match: {profile.get('occupation') or 'profile flags'}")
        scores["occupation"] = 1.0
    elif occ_tags:
        missing.append("Occupation may not match scheme requirements")
        scores["occupation"] = 0.2
    else:
        scores["occupation"] = 0.5  # no occupation info

    # ── 3. Income Match (20%) ─────────────────────────────────────────────────
    income = profile.get("annual_income")
    if income is not None:
        # Schemes for low-income groups
        low_income_keywords = ["bpl", "below poverty", "low income", "economically weaker",
                                "ews", "annual income", "family income", "household income"]
        if _contains_any(combined_text, low_income_keywords):
            if income <= 250000:
                matched.append("Income within low-income scheme limit")
                scores["income"] = 1.0
            elif income <= 500000:
                matched.append("Income within moderate scheme limit")
                scores["income"] = 0.7
            elif income <= 800000:
                scores["income"] = 0.4
                missing.append("Income may exceed scheme limit")
            else:
                scores["income"] = 0.1
                missing.append("Income likely exceeds scheme limit")
        else:
            # Scheme doesn't mention income restriction
            matched.append("No strict income restriction mentioned")
            scores["income"] = 0.8
    else:
        scores["income"] = 0.5  # unknown income, neutral

    # ── 4. Category Match (15%) ───────────────────────────────────────────────
    user_category = (profile.get("category") or "").lower().strip()
    cat_keywords = CATEGORY_TAG_MAP.get(user_category, [])

    if cat_keywords and _contains_any(combined_text, cat_keywords):
        matched.append(f"Category match: {profile['category'].upper()}")
        scores["category"] = 1.0
    elif user_category == "general":
        # General category — check if scheme is restricted to reserved categories
        restricted_keywords = ["scheduled caste", "scheduled tribe", "obc", "sc only", "st only"]
        if _contains_any(combined_text, restricted_keywords):
            missing.append("Scheme may be restricted to reserved categories")
            scores["category"] = 0.2
        else:
            matched.append("General category eligible")
            scores["category"] = 0.8
    else:
        scores["category"] = 0.5

    # ── 5. Education Match (10%) ──────────────────────────────────────────────
    education = (profile.get("education") or "").lower().strip()
    edu_tags = []
    for key in EDUCATION_TAG_MAP:
        if key in education or education in key:
            edu_tags = EDUCATION_TAG_MAP[key]
            break

    if edu_tags and _contains_any(combined_text, edu_tags):
        matched.append(f"Education match: {profile.get('education')}")
        scores["education"] = 1.0
    elif education:
        scores["education"] = 0.5
    else:
        scores["education"] = 0.5

    # ── 6. Tag Match (10%) ────────────────────────────────────────────────────
    tag_score = 0.0
    tag_hits = 0

    if profile.get("has_disability") and _contains_any(combined_text, ["disability", "pwd", "person with disability", "divyang"]):
        matched.append("Disability benefit available")
        tag_hits += 1

    if profile.get("gender", "").lower() == "female" and _contains_any(combined_text, ["women", "woman", "girl", "female", "mahila"]):
        matched.append("Scheme targets women")
        tag_hits += 1

    if profile.get("is_student") and _contains_any(combined_text, ["student", "scholarship", "education"]):
        tag_hits += 1

    if profile.get("is_farmer") and _contains_any(combined_text, ["farmer", "agriculture", "kisan"]):
        tag_hits += 1

    tag_score = min(1.0, tag_hits * 0.5) if tag_hits else 0.4
    scores["tags"] = tag_score

    # ── Weighted Eligibility Score ────────────────────────────────────────────
    weights = {
        "state":      0.25,
        "occupation": 0.20,
        "income":     0.20,
        "category":   0.15,
        "education":  0.10,
        "tags":       0.10,
    }

    eligibility_score = sum(scores[k] * weights[k] for k in weights)
    eligibility_score = round(eligibility_score * 100, 1)

    # ── Confidence Score ──────────────────────────────────────────────────────
    completeness = _profile_completeness(profile)
    confidence_score = round(eligibility_score * (0.6 + 0.4 * completeness), 1)
    confidence_score = min(confidence_score, 100.0)

    # ── Explanation ───────────────────────────────────────────────────────────
    if eligibility_score >= 75:
        verdict = "You are likely eligible for this scheme."
    elif eligibility_score >= 50:
        verdict = "You may partially qualify for this scheme."
    else:
        verdict = "You may not meet all requirements for this scheme."

    matched_str = "; ".join(matched) if matched else "No strong matches found"
    missing_str = "; ".join(missing) if missing else "No major gaps identified"

    explanation = (
        f"{verdict} "
        f"Matched: {matched_str}. "
        f"Gaps: {missing_str}."
    )

    return {
        "eligibility_score": eligibility_score,
        "confidence_score": confidence_score,
        "matched_conditions": matched,
        "missing_conditions": missing,
        "explanation": explanation,
    }
