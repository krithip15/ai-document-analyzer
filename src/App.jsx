import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";
import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [documentInfo, setDocumentInfo] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [asking, setAsking] = useState(false);

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

  const askQuestion = async () => {
    if (!question.trim()) return;

    setAsking(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Question failed");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources);
    } catch (error) {
      console.error(error);
      alert("Failed to get an answer.");
    } finally {
      setAsking(false);
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
          <section className="question-section">
            <h2>Ask a question</h2>

            <div className="question-box">
              <input
                type="text"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="What dataset was used in the study?"
              />

              <button
                onClick={askQuestion}
                disabled={!question.trim() || asking}
              >
                {asking ? "Thinking..." : "Ask"}
              </button>
            </div>

            {answer && (
              <div className="answer-section">
                <h3>Answer</h3>

                <p>{answer}</p>

                {sources.length > 0 && (
                  <div className="sources">
                    <h4>Sources</h4>

                    {sources.map((source, index) => (
                      <span key={index} className="source">
                        Page {source.page}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </section>
        )}
      </main>
    </>
  );
}

export default App;
