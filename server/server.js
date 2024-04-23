const express = require("express");
const app = express();
const PORT = 5000;
const cors = require("cors");
const fs = require("fs");
const path = require("path");

app.use(cors());
app.use(express.json());

// Define the path to the data.json file
const dataFilePath = path.join(__dirname, "data.json");

app.post("/api/submit-data", (req, res) => {
  const { email, classId, submissionId } = req.body;

  const { exec } = require('child_process');

  try {
    fs.writeFileSync(
      dataFilePath,
      JSON.stringify({ email, classId, submissionId })
    );
    res.status(200).json({ message: "Data received and saved successfully!" });
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ error: "Failed to process the request" });
  }
  exec('python mainf.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });

  
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
