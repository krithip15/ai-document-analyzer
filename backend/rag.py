import requests

from vector_store import search_chunks

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_answer(question):
    # 1. Retrieve relevant chunks from ChromaDB
    results = search_chunks(question, n_results=3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 2. Build context for the LLM
    context_parts = []

    for document, metadata in zip(documents, metadatas):
        context_parts.append(f"[Page {metadata['page']}]\n{document}")

    context = "\n\n".join(context_parts)

    # 3. Create the RAG prompt
    prompt = f"""
You are a document analysis assistant.

Answer the user's question using ONLY
the provided document context.

If the answer cannot be found in the
document context, say:

"I couldn't find this information
in the document."

Do not use outside knowledge.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

Give a concise and accurate answer.
"""

    # 4. Send the prompt to Ollama
    response = requests.post(
        OLLAMA_URL, json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )

    response.raise_for_status()

    # 5. Extract the LLM response
    answer = response.json()["response"]

    # 6. Prepare source information
    sources = [
        {"page": metadata["page"], "filename": metadata["filename"]}
        for metadata in metadatas
    ]

    return {"answer": answer, "sources": sources}
