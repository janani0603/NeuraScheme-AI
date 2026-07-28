def explanation_prompt(scheme: dict, profile: dict, matched: list, missing: list) -> str:
    return f"""You are an expert government scheme advisor for India.

A citizen has been matched with the following government scheme. Generate a clear, helpful, and personalized explanation.

SCHEME INFORMATION:
Name: {scheme.get('scheme_name', '')}
Level: {scheme.get('level', '')}
Categories: {', '.join(scheme.get('schemeCategory', []))}
Benefits: {scheme.get('benefits', '')}
Eligibility: {scheme.get('eligibility', '')}
Required Documents: {scheme.get('documents', '')}
Application Process: {scheme.get('application', '')}

CITIZEN PROFILE:
State: {profile.get('state', 'Not specified')}
Gender: {profile.get('gender', 'Not specified')}
Occupation: {profile.get('occupation', 'Not specified')}
Education: {profile.get('education', 'Not specified')}
Annual Income: {profile.get('annual_income', 'Not specified')}
Category: {profile.get('category', 'Not specified')}
Student: {profile.get('is_student', False)}
Farmer: {profile.get('is_farmer', False)}
Business Owner: {profile.get('is_business_owner', False)}
Has Disability: {profile.get('has_disability', False)}

MATCHED CONDITIONS: {', '.join(matched) if matched else 'None identified'}
MISSING CONDITIONS: {', '.join(missing) if missing else 'None identified'}

Write a 3-4 sentence personalized explanation covering:
1. Why this scheme is recommended for this citizen
2. Key benefits they will receive
3. Any important conditions or documents they should prepare
4. A brief note on how to apply

Use only the information provided above. Do not invent or assume any details not present in the scheme information.
Keep the tone friendly, clear, and encouraging. Write in plain English."""


def assistant_prompt(question: str, scheme_context: str, conversation_history: str, history_status: str = "first message") -> str:
    has_scheme_context = "No specific schemes selected" not in scheme_context and "No scheme information found" not in scheme_context

    if has_scheme_context:
        context_instruction = """IMPORTANT RULES:
- Prioritize the scheme information provided below when answering
- You may use your general knowledge about Indian government schemes to supplement answers
- Never invent specific eligibility criteria, amounts, or deadlines not in the provided data
- Be concise, friendly, and helpful
- Do NOT greet the user (no Namaste, Hi, Hello) unless this is the very first message (conversation history is empty)"""
    else:
        context_instruction = """IMPORTANT RULES:
- Answer using your knowledge of Indian government schemes and welfare programs
- Provide helpful, accurate general information about schemes, eligibility, documents, and application processes
- If you are unsure about specific details, say so and suggest the citizen verify on the official portal
- Be concise, friendly, and helpful
- Do NOT greet the user (no Namaste, Hi, Hello) unless this is the very first message (conversation history is empty)"""

    return f"""You are NeuraScheme AI, a helpful government scheme assistant for Indian citizens.

You help citizens understand government welfare schemes, eligibility requirements, application procedures, required documents, and deadlines.

{context_instruction}

SCHEME CONTEXT:
{scheme_context}

CONVERSATION HISTORY ({history_status}):
{conversation_history}

CITIZEN QUESTION:
{question}

Provide a helpful, accurate answer."""


def eligibility_interpretation_prompt(eligibility_text: str, profile: dict) -> str:
    return f"""You are analyzing government scheme eligibility criteria for an Indian citizen.

ELIGIBILITY CRITERIA (from official scheme):
{eligibility_text}

CITIZEN PROFILE:
- State: {profile.get('state', 'Not specified')}
- Age: {profile.get('age', 'Not specified')}
- Gender: {profile.get('gender', 'Not specified')}
- Occupation: {profile.get('occupation', 'Not specified')}
- Education: {profile.get('education', 'Not specified')}
- Annual Income: {profile.get('annual_income', 'Not specified')}
- Category: {profile.get('category', 'Not specified')}
- Is Student: {profile.get('is_student', False)}
- Is Farmer: {profile.get('is_farmer', False)}
- Has Disability: {profile.get('has_disability', False)}

Based ONLY on the eligibility criteria text above, identify:
1. Which conditions the citizen clearly meets
2. Which conditions the citizen clearly does not meet
3. Which conditions cannot be determined from the profile

Respond in this exact JSON format:
{{
  "meets": ["condition 1", "condition 2"],
  "does_not_meet": ["condition 1"],
  "cannot_determine": ["condition 1"]
}}

Do not add any explanation outside the JSON."""


def ranking_prompt(schemes_summary: str, profile: dict) -> str:
    return f"""You are ranking government schemes for an Indian citizen based on relevance.

CITIZEN PROFILE:
- State: {profile.get('state', 'Not specified')}
- Occupation: {profile.get('occupation', 'Not specified')}
- Education: {profile.get('education', 'Not specified')}
- Annual Income: {profile.get('annual_income', 'Not specified')}
- Category: {profile.get('category', 'Not specified')}
- Is Student: {profile.get('is_student', False)}
- Is Farmer: {profile.get('is_farmer', False)}
- Is Business Owner: {profile.get('is_business_owner', False)}
- Has Disability: {profile.get('has_disability', False)}

SCHEMES TO RANK (slug: name):
{schemes_summary}

Return ONLY a JSON array of slugs ordered from most relevant to least relevant.
Example: ["slug-1", "slug-2", "slug-3"]

Base ranking on how well each scheme matches the citizen's profile. Do not add explanation."""


def intent_router_prompt(question: str, history: str) -> str:
    return f"""You are an intent classifier for a government scheme assistant.

Analyze the user's question and classify which agents are needed to answer it.

Available agents:
- "recommendations": User wants to know what schemes they qualify for
- "comparison": User wants to compare 2 or more specific schemes
- "documents": User wants to know what documents are needed or if they have the right documents
- "deadlines": User wants to know about deadlines or time-sensitive schemes
- "general": General question about a scheme, eligibility, benefits, how to apply

CONVERSATION HISTORY:
{history}

USER QUESTION: {question}

Respond in this exact JSON format:
{{
  "intents": ["intent1", "intent2"],
  "scheme_slugs_mentioned": ["slug1", "slug2"],
  "needs_profile": true or false
}}

- intents: list of agents needed (can be multiple)
- scheme_slugs_mentioned: any specific scheme slugs or names mentioned (convert names to likely slugs using lowercase-hyphen format)
- needs_profile: true if the question requires the user's personal profile to answer
Do not add explanation outside the JSON."""


def synthesis_prompt(question: str, agent_outputs: str, history: str, history_status: str) -> str:
    return f"""You are NeuraScheme AI, a helpful government scheme assistant for Indian citizens.

You have gathered information from multiple specialized agents to answer the user's question.
Synthesize all the information into one clear, conversational, helpful response.

RULES:
- Combine insights from all agent outputs naturally
- Be concise but complete
- Use bullet points or sections if the answer has multiple parts
- Do NOT greet the user unless this is the first message
- Do not mention "agents" or internal workings to the user
- If data is missing or agents returned no results, say so honestly

CONVERSATION HISTORY ({history_status}):
{history}

AGENT OUTPUTS:
{agent_outputs}

USER QUESTION: {question}

Provide a single, unified, helpful response:"""
