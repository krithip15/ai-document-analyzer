# DocuMind

AI-powered PDF Q&A using Retrieval-Augmented Generation (RAG). Upload a document, ask questions, get answers grounded in the text with source page references.

**Stack:** React · FastAPI · ChromaDB · Sentence Transformers · Ollama (Qwen2.5) · PyPDF

## How it works

PDF → chunked → embedded → stored in ChromaDB → retrieved on query → answered by Qwen2.5 with source pages.

## Setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Ollama
ollama pull qwen2.5:3b

# Frontend
npm install && npm run dev
```
