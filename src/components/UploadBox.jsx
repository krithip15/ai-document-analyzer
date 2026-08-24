import { useRef } from "react";

function UploadBox({ file, setFile }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      alert("Please select a PDF file.");
    }
  };

  const handleBrowse = () => {
    fileInputRef.current.click();
  };

  const removeFile = () => {
    setFile(null);
    fileInputRef.current.value = "";
  };

  return (
    <div className="upload-section">
      {!file ? (
        <div className="upload-box" onClick={handleBrowse}>
          <div className="upload-icon">↑</div>

          <h3>Drop your PDF here</h3>

          <p>or click to browse files</p>

          <span>PDF • Max 20 MB</span>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
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
