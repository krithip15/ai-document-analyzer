from fastapi import FastAPI, UploadFile, File
from pdf_processor import extract_text

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

    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    return {
        "filename": file.filename,
        "pages": len(pages),
        "characters": total_characters
    }