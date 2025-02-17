import { useState } from "react";
import axios from "axios";
import "./App.css"; // Keep if you want styling

function App() {
  const [text, setText] = useState("");
  const [model, setModel] = useState("llama"); // Default model
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeClick = async () => {
    if (!text.trim()) {
      alert("Please enter some text to analyze.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze/", {
        text,
        model,
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
      setResult({ sentiment: "Error", confidence: "N/A" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: "600px", margin: "auto", textAlign: "center", padding: "20px" }}>
      <h1>Sentiment Analysis</h1>
      
      {/* Text Input */}
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text here..."
        rows="4"
        cols="50"
        style={{ width: "100%", marginBottom: "10px", padding: "10px" }}
      />
      
      {/* Model Selection Dropdown */}
      <div>
        <label>Select Model: </label>
        <select value={model} onChange={(e) => setModel(e.target.value)} style={{ padding: "5px" }}>
          <option value="custom">Custom Model</option>
          <option value="llama">Llama 3</option>
        </select>
      </div>
      
      {/* Analyze Button */}
      <button 
        onClick={handleAnalyzeClick} 
        style={{ marginTop: "10px", padding: "10px 20px", cursor: "pointer" }}
      >
        {loading ? "Analyzing..." : "Analyze Sentiment"}
      </button>

      {/* Result Display */}
      {result && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc", borderRadius: "5px" }}>
          <h2>Result:</h2>
          <p>Sentiment: {result.sentiment}</p>
          {result.confidence !== undefined && <p>Confidence: {result.confidence}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
