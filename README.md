# Context-Aware RAG Flask Lab

## Overview

This project implements a small Flask API that combines two capabilities:

- a simplified Retrieval-Augmented Generation (RAG) workflow for approved company documents
- a small external API client that fetches people data from a public JSON endpoint

The app exposes:

- `GET /api/health` for a simple health check
- `POST /api/ask` for context-backed answers from approved company documents
- `GET /api/people` for JSON data returned by the public people endpoint

## What the app does

The RAG endpoint accepts a user query, retrieves relevant company documents, builds a prompt using that context, and returns a generated answer with source metadata. If no relevant documents are found, it returns a safe fallback response. If the model service is unavailable, it returns a 503 response.

The people API client fetches data from:

- https://learn-co-curriculum.github.io/json-site-example/endpoints/people.json

## Project structure

- `lib/app.py` – Flask routes and request handling
- `lib/rag_service.py` – document tokenization, retrieval, prompt construction, and source formatting
- `lib/company_documents.py` – approved company documents used for the RAG flow
- `lib/ai_client.py` – wrapper around the model-generation client
- `lib/people_api_client.py` – client for fetching people data from the public endpoint
- `lib/tests/` – pytest coverage for the RAG logic, Flask routes, and people API client

## Screenshot

![Completed API demo](docs/api-demo.png)

## Setup

Install dependencies:

```bash
pipenv install
pipenv shell
```

Run tests:

```bash
pytest
```

Run the app locally:

```bash
flask --app lib.app run --debug
```

Example requests:

```bash
curl -i http://127.0.0.1:5000/api/health
curl -i -X POST http://127.0.0.1:5000/api/ask -H "Content-Type: application/json" -d '{"query":"How do I request access to approved software?"}'
curl -i http://127.0.0.1:5000/api/people
```

## Notes

- The RAG flow uses simple keyword-based matching rather than embeddings.
- The AI model call is mocked in the test suite, so Ollama is not required for automated verification.
- The implementation avoids stale or unnecessary comments and keeps the code focused on the requested behavior.
