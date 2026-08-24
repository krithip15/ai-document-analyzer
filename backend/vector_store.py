import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")


# Create or reuse our collection
collection = chroma_client.get_or_create_collection(name="documents")


def add_chunks(chunks, filename):
    documents = []
    metadatas = []
    ids = []

    # Remove previous version of this document
    collection.delete(where={"filename": filename})

    for index, chunk in enumerate(chunks):
        documents.append(chunk["text"])

        metadatas.append({"page": chunk["page"], "filename": filename})

        ids.append(f"{filename}-{index}")

    # Convert text into embeddings
    embeddings = embedding_model.encode(documents).tolist()

    # Store everything in ChromaDB
    collection.add(
        documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids
    )

    return len(documents)


def search_chunks(query, filename, n_results=5):
    # Convert the question into an embedding
    query_embedding = embedding_model.encode([query]).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where={"filename": filename},
    )

    return results
