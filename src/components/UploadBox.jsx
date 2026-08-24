import { useRef, useState } from "react";

function UploadBox({ file, setFile }) {
  const fileInputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    // Check file type
    if (selectedFile.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }

    // Check file size (20 MB)
    const maxSize = 20 * 1024 * 1024;

    if (selectedFile.size > maxSize) {
      alert("File size must be less than 20 MB.");
      return;
    }

    setFile(selectedFile);
  };

  const handleFileChange = (event) => {
    handleFile(event.target.files[0]);
  };

  const handleBrowse = () => {
    fileInputRef.current.click();
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);

    const droppedFile = event.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
    fileInputRef.current.value = "";
  };

  return (
    <div className="upload-section">
      {!file ? (
        <div
          className={`upload-box ${dragging ? "dragging" : ""}`}
          onClick={handleBrowse}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-icon">↑</div>

          <h3>{dragging ? "Drop your PDF here" : "Drop your PDF here"}</h3>

          <p>or click to browse files</p>

          <span>PDF • Max 20 MB</span>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            hidden
          />
        </div>
      ) : (
        <div className="selected-file">
          <div>
            <strong>{file.name}</strong>

            <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>

          <button onClick={removeFile}>Remove</button>
        </div>
      )}
    </div>
  );
}

export default UploadBox;
