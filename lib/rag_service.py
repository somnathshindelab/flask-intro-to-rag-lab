from __future__ import annotations

import re
from typing import Any

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "do",
    "does",
    "for",
    "from",
    "get",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "need",
    "of",
    "on",
    "or",
    "our",
    "should",
    "so",
    "the",
    "their",
    "to",
    "use",
    "what",
    "when",
    "where",
    "who",
    "why",
    "with",
    "you",
    "your",
}


def tokenize(text: str) -> set[str]:
    """Convert text into a set of searchable lowercase tokens.

    TODO:
    - Lowercase the text.
    - Extract word-like values.
    - Remove leading/trailing apostrophes.
    - Remove tokens with length <= 1.
    - Remove tokens in STOPWORDS.
    - Return a set of searchable terms.
    """
    tokens: set[str] = set()
    if not text:
        return tokens

    for match in re.finditer(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower()):
        token = match.group(0).strip("'")
        if len(token) <= 1 or token in STOPWORDS:
            continue
        tokens.add(token)

    return tokens


def document_search_text(document: dict[str, Any]) -> str:
    """Combine searchable document fields into one text value.

    TODO:
    Include title, category, tags, and text.
    """
    title = document.get("title", "") or ""
    category = document.get("category", "") or ""
    tags = " ".join(document.get("tags", []) or [])
    body = document.get("text", "") or ""
    return " ".join(part for part in [title, category, tags, body] if part)


def score_document(query: str, document: dict[str, Any]) -> dict[str, Any]:
    """Score a document using keyword overlap.

    TODO:
    - Tokenize the query.
    - Tokenize the combined searchable document text.
    - Tokenize the document title.
    - Find matched terms between query tokens and document tokens.
    - Add a small title boost: 0.5 for each query token found in the title.
    - Return a dictionary with keys: document, score, matched_terms.
    """
    query_tokens = tokenize(query)
    document_tokens = tokenize(document_search_text(document))
    title_tokens = tokenize(document.get("title", "") or "")

    matched_terms = sorted(query_tokens & document_tokens)
    title_boost = 0.5 * sum(1 for term in query_tokens if term in title_tokens)
    score = len(matched_terms) + title_boost

    return {
        "document": document,
        "score": score,
        "matched_terms": matched_terms,
    }


def retrieve_context(
    query: str,
    documents: list[dict[str, Any]],
    limit: int = 2,
    minimum_score: float = 1.0,
) -> list[dict[str, Any]]:
    """Select the most relevant documents for the query.

    TODO:
    - Score all documents.
    - Keep only matches with score >= minimum_score.
    - Sort by score from highest to lowest.
    - Return only the top `limit` matches.

    The selected context must depend on the user's query. Do not return the same
    hardcoded document for every request.
    """
    scored_documents = [score_document(query, document) for document in documents]
    relevant_matches = [
        item for item in scored_documents if item["score"] >= minimum_score
    ]
    relevant_matches.sort(key=lambda item: item["score"], reverse=True)
    return relevant_matches[:limit]


def format_context(context_matches: list[dict[str, Any]]) -> str:
    """Format retrieved documents into a context block for the prompt.

    TODO:
    - If no matches exist, return a short no-context message.
    - For each match, include Source ID, Title, Category, and Content.
    - Separate document blocks clearly.
    """
    if not context_matches:
        return "No relevant context found for the provided query."

    blocks: list[str] = []
    for match in context_matches:
        document = match["document"]
        blocks.append(
            "\n".join(
                [
                    "Source ID: " + document["id"],
                    "Title: " + document["title"],
                    "Category: " + document["category"],
                    "Content: " + document["text"],
                ]
            )
        )
    return "\n\n".join(blocks)


def build_prompt(query: str, context_matches: list[dict[str, Any]]) -> str:
    """Build a structured prompt with instructions, context, question, and requirements.

    TODO:
    The prompt should include these sections:
    - Instructions
    - Context
    - Question
    - Response requirements

    The prompt should tell the model to use only the provided context and avoid
    inventing unsupported details.
    """
    context_text = format_context(context_matches)
    return "\n\n".join(
        [
            "Instructions:",
            "You are a helpful assistant. Use only the information in the provided context. If the context does not contain enough information, say so clearly and do not invent unsupported details.",
            "Context:",
            context_text,
            "Question:",
            query,
            "Response requirements:",
            "- Answer using only the provided context.",
            "- Mention the relevant source IDs when available.",
            "- Do not invent unsupported details.",
        ]
    )


def source_metadata(match: dict[str, Any]) -> dict[str, str]:
    """Return source information that is safe to expose in the API response.

    TODO:
    Return only the document id and title.
    """
    return {
        "id": match["document"]["id"],
        "title": match["document"]["title"],
    }
