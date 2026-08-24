from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pdf_processor import extract_text
from chunker import create_chunks
from vector_store import add_chunks, search_chunks

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "DocuMind API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    pages = extract_text(file.file)

    chunks = create_chunks(pages)

    stored_chunks = add_chunks(
        chunks,
        file.filename
    )

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": stored_chunks
    }

class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search_document(request: SearchRequest):
    results = search_chunks(request.query)

    return results
