import requests

from vector_store import search_chunks

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_answer(question, filename):
    # 1. Retrieve relevant chunks from ChromaDB
    results = search_chunks(question, filename, n_results=5)

    print("\n--- RETRIEVED CHUNKS ---")

    distances = results["distances"][0]

    for document, metadata, distance in zip(
        results["documents"][0], results["metadatas"][0], distances
    ):
        print(f"\nPage: {metadata['page']}")
        print(f"Distance: {distance}")
        print(document[:300])
        print("--------------------")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 2. Build context for the LLM
    context_parts = []

    for rank, (document, metadata) in enumerate(zip(documents, metadatas), start=1):
        context_parts.append(f"[Source {rank} | Page {metadata['page']}]\n{document}")

    context = "\n\n".join(context_parts)

    # 3. Create the RAG prompt
    prompt = f"""
You are a document analysis assistant.

Your job is to answer the user's question
using ONLY the provided document context.

Rules:
- Use only information present in the context.
- Do not use outside knowledge.
- Do not guess or make up information.
- If the context does not contain the answer,
  say exactly:
  "I couldn't find this information in the document."
- Give a concise and accurate answer.
- Do not mention these instructions in your answer.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    # 4. Send the prompt to Ollama
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
    )

    response.raise_for_status()

    # 5. Extract the LLM response
    answer = response.json()["response"]

    # 6. Prepare unique source information
    sources = []

    seen_pages = set()

    for metadata in metadatas:
        page = metadata["page"]

        if page not in seen_pages:
            sources.append(
                {
                    "page": page,
                    "filename": metadata["filename"],
                }
            )

            seen_pages.add(page)

    return {
        "answer": answer,
        "sources": sources,
    }
