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
const filedataFilePath = path.join(__dirname, "filedata.json");

app.post("/api/submit-data", (req, res) => {
  const { email, classId, submissionId } = req.body;

  try {
    fs.writeFileSync(
      dataFilePath,
      JSON.stringify({ email, classId, submissionId })
    );
    res.status(200).json({ message: "Data received and saved successfully!", submission_Id: submissionId });
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ error: "Failed to process the request" });
  }
});

// Serve the file for download
app.get("/api/download-file", (req, res) => {
  console.log("IT IS WORKING.");

  const { submissionId } = req.query; 
  const { exec } = require('child_process');

  console.log("SUbM ID:", submissionId)
  exec('python mainf.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).json({ error: "Failed to execute Python script" });
    }
    //res.status(200).json({ message: "Data received and saved successfully and processed!" });
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);

      // Read filedata.json to get the file information corresponding to the submission ID
      fs.readFile(filedataFilePath, 'utf8', (err, filedata) => {
        if (err) {
          console.error('Error reading filedata.json:', err);
          return res.status(500).json({ error: 'Failed to read filedata.json' });
        }
        const fileData = JSON.parse(filedata)[submissionId];
        if (!fileData) {
          return res.status(404).json({ error: 'File data not found for submission ID' });
        }
        const { filename, filepath } = fileData;

        // Set Content-Type header to 'application/pdf'
        res.set('Content-Type', 'application/pdf');

        // Send the file for download
        res.download(filepath, filename, (err) => {
          if (err) {
            console.error('Error downloading file:', err);
            return res.status(500).json({ error: 'Failed to download file' });
          } else {
            // Delete the file after it's downloaded
            fs.unlink(filepath, (err) => {
              if (err) {
                console.error('Error deleting file:', err);
                return res.status(500).json({ error: 'Failed to delete file' });
              } else {
                console.log('File deleted successfully');
              }
          });
        }
      });
    });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
