from src.core.models import Paper
from src.profiles.schema import UserProfile


def build_synonym_prompt(profile: UserProfile) -> str:
    """Build prompt for LLM synonym/related-term expansion."""
    interests = ", ".join(profile.topic_interests) if profile.topic_interests else "not specified"
    context = profile.project_context or "not specified"
    level = profile.expertise_level or "intermediate"
    signals = ", ".join(profile.required_signals) if profile.required_signals else "none"
    negatives = ", ".join(profile.negative_filters) if profile.negative_filters else "none"

    return f"""Let's roleplay. You are a senior academic researcher and domain expert who mentors graduate students. You have deep knowledge of the literature and know exactly which search terms would surface relevant papers versus noise.

A researcher has asked you to help them find papers. Based on their profile, suggest precise search terms that would appear in paper titles and abstracts they'd actually want to read.

**Researcher Profile:**
- Topic interests: {interests}
- Research context: {context}
- Expertise level: {level}
- Must-have signals (terms the researcher specifically cares about): {signals}
- Negative filters (topics to AVOID expanding toward): {negatives}

**Your task:** Generate search terms — synonyms, abbreviations, and closely related concepts — that would help identify papers relevant to THIS SPECIFIC researcher's project.

**Quality rules:**
- ALWAYS include the original topic interests exactly as written — do not rephrase or merge them.
- Add synonyms, abbreviations, and closely related concepts as SHORT terms (1-3 words) that would appear in paper titles or abstracts. Examples: "GNN", "graph neural network", "track fitting", "Kalman filter".
- Anchor expansions around the researcher's must-have signals — these indicate what they consider most important. Generate related terms in those directions.
- Do NOT generate terms related to the negative filters — those are explicitly unwanted.
- Every expanded term should be something THIS researcher would plausibly search for given their project context. Ask yourself: "Would this term appear in a paper this person needs to read?"
- Do NOT generate long phrases like "machine learning for medical imaging" — these are too specific to match. Instead, add the individual concepts: "machine learning", "medical imaging".
- Stay tightly within the researcher's domain. Do NOT expand into adjacent fields unless the researcher's context explicitly bridges them.
- Do NOT pad the list with generic terms (e.g., "supervised learning", "data augmentation") unless directly relevant to the project context.

Return a JSON object with a single key "expanded_terms" containing a flat list of strings. Start with the original terms, then add your short synonyms and related concepts. Aim for 15-25 high-quality terms total — fewer precise terms is better than many vague ones.

Example format:
{{"expanded_terms": ["term1", "term2", "term3"]}}"""


def build_ranking_prompt(papers: list[Paper], profile: UserProfile) -> str:
    """Build prompt for LLM batch ranking + summarization."""
    interests = ", ".join(profile.topic_interests) if profile.topic_interests else "not specified"
    context = profile.project_context or "not specified"
    level = profile.expertise_level or "intermediate"

    papers_text = ""
    for i, p in enumerate(papers):
        papers_text += f"""
---
Paper {i + 1}:
ID: {p.source_id}
Title: {p.title}
Abstract: {p.abstract}
Categories: {", ".join(p.categories)}
---
"""

    return f"""Let's roleplay. You are a senior academic researcher who screens papers for a colleague. You have decades of experience in their field and understand what makes a paper genuinely useful versus superficially related. You are rigorous — you don't inflate scores just because a paper mentions a relevant keyword.

**Researcher Profile:**
- Topic interests: {interests}
- Research context: {context}
- Expertise level: {level}

**Papers to evaluate:**
{papers_text}

**Scoring rubric** (use these anchors consistently — most papers should score 3-6, not 8-10):
- **9-10**: Paper's PRIMARY contribution is one of the researcher's listed methods applied to their exact problem domain. Reserve for true must-reads. Most batches will have 0-1 papers at this level.
- **7-8**: Same subfield with directly transferable methods or results. The researcher could cite or build on this work.
- **4-6**: Related field or tangentially useful technique. Interesting but not actionable for their current project.
- **1-3**: Different field, different methods, or only superficial keyword overlap. Being in the same broad discipline is NOT enough for a high score.

**Anti-inflation rules:**
- Sharing a broad topic area is NOT automatic relevance. The methods and application must actually match the researcher's work.
- Sharing a category or venue does not mean relevance. Score based on methodological and topical overlap with the researcher's PROJECT CONTEXT.
- When in doubt, score lower. A 5 is not a bad score — it means "might be interesting".

For each paper, provide:
1. **relevance_score**: integer 1-10 using the rubric above
2. **reasoning**: one sentence explaining why this score, referencing the researcher's specific interests or project context
3. **abstract_takeaway**: 2-4 sentence factual summary grounded strictly in the abstract. Cover: (a) what problem the paper addresses, (b) what technique or method is applied, and (c) what the key results or findings are. Do not add interpretation — only report what the abstract states.
4. **why_relevant**: 2-4 sentence explanation of why this paper matters to THIS researcher. Explain: (a) which of the researcher's topic interests it connects to and how, (b) how it relates to or could benefit their specific project context. Be concrete — do not just say "this aligns with the researcher's interests".
5. **summary**: 2-3 sentence summary tailored to the researcher's expertise level ({level})

Return a JSON object with a single key "papers" containing a list of objects, one per paper, in the same order as provided. Each object must have keys: "paper_id", "relevance_score", "reasoning", "abstract_takeaway", "why_relevant", "summary".

Example format:
{{"papers": [{{"paper_id": "2603.01234v1", "relevance_score": 8, "reasoning": "Directly addresses...", "abstract_takeaway": "This paper presents a method for...", "why_relevant": "This could improve your...", "summary": "This paper proposes..."}}]}}"""
