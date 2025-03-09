import React, { useState } from "react";
import axios from "axios";
import "./ResumeUpload.css";

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [candidates, setCandidates] = useState([]);

  const handleFileChange = (event) => {
    const selected = event.target.files[0];
    if (selected) {
      setFile(selected);
      setFileName(selected.name);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    setUploadStatus("");

    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setUploadStatus("✅ File uploaded successfully!");
      setUploadedFiles((prevFiles) => [...prevFiles, res.data.filePath]);
    } catch (err) {
      console.error("Upload failed", err);
      setUploadStatus("❌ Upload failed. Try again.");
    }
    setLoading(false);
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      alert("Please enter a skill to search!");
      return;
    }

    setUploadStatus("");
    setCandidates([]);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:5000/api/match", { query });
      console.log("Full API Response:", res);
      
      if (!res.data) {
        console.error("Received empty response from backend.");
        alert("No response from the server. Try again.");
        return;
      }
      
      // Check if the response contains an error message about invalid input
      if (res.data.error) {
        setUploadStatus(`❌ ${res.data.error}`);
        return;
      }
      
      // Handle the nested JSON response
      if (res.data.result && typeof res.data.result === "string") {
        try {
          // Extract the JSON array from the string
          const jsonStartIndex = res.data.result.indexOf('[{');
          const jsonEndIndex = res.data.result.lastIndexOf('}]') + 2;
          
          if (jsonStartIndex >= 0 && jsonEndIndex > jsonStartIndex) {
            const jsonStr = res.data.result.substring(jsonStartIndex, jsonEndIndex);
            const parsedCandidates = JSON.parse(jsonStr);
            
            if (parsedCandidates.length === 0) {
              setUploadStatus("No matching candidates found for these skills.");
            } else {
              setCandidates(parsedCandidates);
            }
          } else {
            console.error("Could not find JSON array in result string");
            setUploadStatus("❌ Invalid response format from server.");
          }
        } catch (parseError) {
          console.error("JSON Parsing Error:", parseError);
          setUploadStatus("❌ Received invalid JSON from backend.");
        }
      } else if (Array.isArray(res.data.result)) {
        // If result is already an array
        if (res.data.result.length === 0) {
          setUploadStatus("No matching candidates found for these skills.");
        } else {
          setCandidates(res.data.result);
        }
      } else {
        console.error("Unexpected response format:", res.data);
        setUploadStatus("❌ Received unexpected response format from server.");
      }
    } catch (err) {
      console.error("Error fetching candidates", err);
      setUploadStatus("❌ Failed to fetch candidates. Try again.");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="resume-container">
      <div className="upload-card">
        <h2>📂 Upload Your Resume</h2>

        <input type="file" id="fileInput" onChange={handleFileChange} accept=".pdf" />
        <label htmlFor="fileInput" className="choose-file-btn">
          Choose File
        </label>

        {fileName && <p className="selected-file">Selected: {fileName}</p>}

        <button onClick={handleUpload} className="upload-btn" disabled={loading}>
          {loading ? "Uploading..." : "Upload"}
        </button>

        {uploadStatus && <p className="status-message">{uploadStatus}</p>}

        <h2>🔍 Search Candidates</h2>
        <div className="search-container">
          <input
            type="text"
            placeholder="Enter skills (e.g., Python Developer)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
          />
          <button onClick={handleSearch} className="search-btn" disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        {candidates.length > 0 && (
          <div className="candidates-list">
            <h3>👥 Recommended Candidates</h3>
            <ul>
              {candidates.map((candidate, index) => (
                <li key={index}>
                  <div className="candidate-name">{candidate.Name}</div>
                  <div className="candidate-skills">
                    {candidate["Technical Skills"].split(", ").map((skill, i) => (
                      <span key={i} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;
