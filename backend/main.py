from fastapi import FastAPI, UploadFile, File
from pdf_processor import extract_text
from chunker import create_chunks

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

    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(chunks)
    }