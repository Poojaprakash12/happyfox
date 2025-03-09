const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");

const app = express();
const PORT = 5000;

// Ensure 'uploads' directory exists
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

app.use(cors());
app.use(express.json());

// Serve uploaded files statically
app.use("/uploads", express.static(uploadDir));

// Set up Multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
});

// ✅ Route 1: Resume Upload and Processing
app.post("/upload", upload.single("file"), (req, res) => {
  try {
    if (!req.file) {
      console.log("No file received!");
      return res.status(400).json({ error: "No file uploaded!" });
    }

    console.log("Uploaded file:", req.file);

    // ✅ Run Python script to process resume
    const pythonScriptPath = path.join(__dirname, "resume_matcher.py");
    const pythonProcess = spawn("python", [pythonScriptPath, req.file.path]);

    let resultData = "";
    pythonProcess.stdout.on("data", (data) => {
      resultData += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
      console.log(`Python script exited with code ${code}`);
      res.json({
        message: "File uploaded successfully!",
        filePath: `/uploads/${req.file.filename}`,
        result: resultData.trim(),
      });
    });
  } catch (error) {
    console.error("Upload Error:", error);
    res.status(500).json({ error: "Server error during file upload" });
  }
});

// ✅ Route 2: Match Candidates Based on User Query
app.post("/api/match", async (req, res) => {
  try {
    const { query } = req.body;
    
    if (!query || query.trim() === '') {
      return res.status(400).json({ 
        error: "Please enter a search query" 
      });
    }
    
    console.log("Received search query:", query);
    
    // Call your Python script to match resumes
    const pythonProcess = spawn('python', ['resume_matcher.py', query]);
    
    let result = '';
    let errorOutput = '';
    
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
      console.log("Python output:", data.toString());
    });
    
    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
      console.error(`Python Error: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
      console.log("Python process exited with code:", code);
      console.log("Full Python output:", result);
      
      if (code !== 0) {
        return res.status(500).json({ error: "Failed to process request: " + errorOutput });
      }
      
      try {
        // Clean the output to ensure it's valid JSON
        const cleanedResult = result.trim();
        
        // Try to parse the JSON directly
        const parsedResult = JSON.parse(cleanedResult);
        
        // Check if it's an error message
        if (parsedResult.error) {
          return res.status(400).json({ error: parsedResult.error });
        }
        
        // Return the parsed result directly
        return res.json({ result: parsedResult });
      } catch (e) {
        console.error("JSON parsing error:", e);
        return res.status(500).json({ error: "Invalid response format from Python script" });
      }
    });
  } catch (error) {
    console.error("Error in /api/match:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// ✅ Start the Server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
