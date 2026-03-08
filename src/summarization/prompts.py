from src.core.models import Paper
from src.profiles.schema import UserProfile


def build_synonym_prompt(profile: UserProfile) -> str:
    """Build prompt for LLM synonym/related-term expansion."""
    interests = ", ".join(profile.topic_interests) if profile.topic_interests else "not specified"
    context = profile.project_context or "not specified"
    level = profile.expertise_level or "intermediate"

    return f"""You are helping a researcher find relevant academic papers. Given their profile, generate related search terms.

**Researcher Profile:**
- Topic interests: {interests}
- Research context: {context}
- Expertise level: {level}

Generate a list of related terms, synonyms, and adjacent concepts that would help identify papers relevant to THIS SPECIFIC researcher. Include abbreviations, alternative phrasings, and closely related subfields.

IMPORTANT constraints:
- Stay within the researcher's domain and expertise. Do not expand into unrelated fields.
- Consider the research context — terms should help find papers useful for their specific project.
- Include technical synonyms and abbreviations (e.g., "RAG" for "retrieval-augmented generation").
- Do NOT include terms from unrelated disciplines just because they share a word.

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

**Scoring rubric** (use these anchors consistently):
- **9-10**: Directly addresses the researcher's active project or core methods. A must-read.
- **7-8**: Same subfield with relevant methods, results, or insights. Likely useful.
- **4-6**: Adjacent field or tangentially related technique. Might be interesting.
- **1-3**: Different field or minimal overlap with the researcher's work.

Score based on how useful this paper would be to THIS SPECIFIC researcher given their project context, not general paper quality.

For each paper, provide:
1. **relevance_score**: integer 1-10 using the rubric above
2. **reasoning**: one sentence explaining why this score, referencing the researcher's specific interests or project context
3. **abstract_takeaway**: 2-4 sentence factual summary grounded strictly in the abstract. Cover: (a) what problem the paper addresses, (b) what technique or method is applied, and (c) what the key results or findings are. Do not add interpretation — only report what the abstract states.
4. **why_relevant**: 2-4 sentence explanation of why this paper matters to THIS researcher. Explain: (a) which of the researcher's topic interests it connects to and how, (b) how it relates to or could benefit their specific project context. Be concrete — do not just say "this aligns with the researcher's interests".
5. **summary**: 2-3 sentence summary tailored to the researcher's expertise level ({level})

Return a JSON object with a single key "papers" containing a list of objects, one per paper, in the same order as provided. Each object must have keys: "paper_id", "relevance_score", "reasoning", "abstract_takeaway", "why_relevant", "summary".

Example format:
{{"papers": [{{"paper_id": "2603.01234v1", "relevance_score": 8, "reasoning": "Directly addresses...", "abstract_takeaway": "This paper presents a method for...", "why_relevant": "This could improve your...", "summary": "This paper proposes..."}}]}}"""
