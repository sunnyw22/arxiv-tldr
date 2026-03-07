from src.core.models import Paper
from src.profiles.schema import UserProfile


def build_synonym_prompt(profile: UserProfile) -> str:
    """Build prompt for LLM synonym/related-term expansion."""
    interests = ", ".join(profile.topic_interests) if profile.topic_interests else "not specified"
    context = profile.project_context or "not specified"

    return f"""Given the following researcher profile, generate a list of related terms, synonyms, and adjacent concepts that would help identify relevant academic papers. Include abbreviations, alternative phrasings, and closely related subfields.

**Topic interests:** {interests}
**Research context:** {context}

Return a JSON object with a single key "expanded_terms" containing a flat list of strings. Include the original terms plus synonyms and related concepts. Aim for 20-40 terms total.

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

    return f"""You are a research paper screening assistant. Given a researcher's profile and a batch of papers, score each paper's relevance and provide a brief summary.

**Researcher Profile:**
- Topic interests: {interests}
- Research context: {context}
- Expertise level: {level}

**Papers to evaluate:**
{papers_text}

For each paper, provide:
1. **relevance_score**: integer 1-10 (10 = highly relevant to researcher's interests)
2. **reasoning**: one sentence explaining why this score (reference specific interests or context)
3. **summary**: 2-3 sentence summary tailored to the researcher's expertise level ({level})

Return a JSON object with a single key "papers" containing a list of objects, one per paper, in the same order as provided. Each object must have keys: "paper_id", "relevance_score", "reasoning", "summary".

Example format:
{{"papers": [{{"paper_id": "2603.01234v1", "relevance_score": 8, "reasoning": "Directly addresses...", "summary": "This paper proposes..."}}]}}"""
