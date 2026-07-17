from __future__ import annotations

from flask import Flask, jsonify, request

from lib.ai_client import generate_response
from lib.company_documents import COMPANY_DOCUMENTS
from lib.people_api_client import people_client
from lib.rag_service import build_prompt, retrieve_context, source_metadata


def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.get("/api/people")
    def get_people():
        """Return the JSON payload from the people API endpoint."""
        return jsonify(people_client.get_response_body())

    @app.post("/api/ask")
    def ask_question():
        """Accept a query and return a source-backed generated answer.

        TODO:
        1. Read JSON request data safely.
        2. Validate that `query` is a non-empty string.
        3. Retrieve relevant context from COMPANY_DOCUMENTS.
        4. If no context is found, return a safe fallback with an empty sources list.
        5. Build a structured prompt from the selected context.
        6. Call generate_response(prompt).
        7. Return query, answer, and sources as JSON.
        8. If generate_response raises RuntimeError, return a 503 service error.
        """
        payload = request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        query = payload.get("query")
        if not isinstance(query, str) or not query.strip():
            return jsonify({"error": "Query must be provided as a non-empty string."}), 400

        context_matches = retrieve_context(query, COMPANY_DOCUMENTS)
        if not context_matches:
            return jsonify(
                {
                    "query": query,
                    "answer": "The approved company documents do not contain enough information to answer that question.",
                    "sources": [],
                }
            )

        prompt = build_prompt(query, context_matches)
        try:
            answer = generate_response(prompt)
        except RuntimeError as error:
            return jsonify({"error": str(error)}), 503

        sources = [source_metadata(match) for match in context_matches]
        return jsonify({"query": query, "answer": answer, "sources": sources})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
