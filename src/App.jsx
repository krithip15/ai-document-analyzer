import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";
import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [documentInfo, setDocumentInfo] = useState(null);

  const uploadDocument = async () => {
    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      setDocumentInfo(data);
    } catch (error) {
      console.error(error);
      alert("Failed to upload document.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      <Navbar />

      <main className="hero">
        <h1>Understand your documents.</h1>

        <p>Upload a research paper and ask questions about it.</p>

        <UploadBox file={file} setFile={setFile} />

        <button
          onClick={uploadDocument}
          disabled={!file || uploading}
          className="analyze-button"
        >
          {uploading ? "Analyzing..." : "Analyze Document"}
        </button>

        {documentInfo && (
          <div>
            <p>Document analyzed successfully!</p>
            <p>File: {documentInfo.filename}</p>
            <p>Pages: {documentInfo.pages}</p>
            <p>Chunks: {documentInfo.chunks}</p>
          </div>
        )}
      </main>
    </>
  );
}

export default App;
