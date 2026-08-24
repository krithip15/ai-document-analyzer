import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";

function App() {
  return (
    <>
      <Navbar />

      <main className="hero">
        <h1>Understand your documents.</h1>

        <p>Upload a research paper and ask questions about it.</p>

        <UploadBox />

        <button className="analyze-button">Analyze Document</button>
      </main>
    </>
  );
}

export default App;
