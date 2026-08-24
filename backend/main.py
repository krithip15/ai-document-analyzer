from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pdf_processor import extract_text
from chunker import create_chunks
from vector_store import add_chunks, search_chunks
from rag import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "DocuMind API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    pages = extract_text(file.file)

    chunks = create_chunks(pages)

    stored_chunks = add_chunks(chunks, file.filename)

    return {"filename": file.filename, "pages": len(pages), "chunks": stored_chunks}


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search_document(request: SearchRequest):
    results = search_chunks(request.question, request.filename)

    return results


class QuestionRequest(BaseModel):
    question: str
    filename: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return generate_answer(request.question)
