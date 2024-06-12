const express = require("express");
const app = express();
const PORT = process.env.PORT || 5000;
const cors = require("cors");
const fs = require("fs");
const fsp = require("fs").promises;
const path = require("path");
const axios = require('axios');

var app_http = express(); // this one to handle http request

var app_https = express(); // this to handle httpS requests.

app.use(cors());
app.use(express.json({ limit: '50mb' }));

// Define the path to the data.json file
const dataFilePath = path.join(__dirname, "data.json");
const filedataFilePath = path.join(__dirname, "filedata.json");
const errorFilePath = path.join(__dirname, 'error.json');

//Middleware to trust cloudflare's proxy
app.set('trust proxy',true);

// Set timeout globally
app.use((req, res, next) => {
  res.setTimeout(300000, () => { // 5 minutes
    console.log('Request has timed out.');
    res.status(408).send('Request timed out.');
  });
  next();
});

app_https.post("/api/submit-data", async (req, res) => {
  const { email, classId, submissionId, recaptchaToken } = req.body;

  try {
    // Verify reCAPTCHA token
    const response = await axios.post('https://www.google.com/recaptcha/api/siteverify', null, {
      params: {
        secret: '6LfKItMpAAAAAENNPNWXxMTJXP1eIzsAwGUBbTUm',
        response: recaptchaToken,
      },
    });

    if (!response.data.success) {
      return res.status(400).json({ error: 'reCAPTCHA verification failed' });
    }

    await fs.writeFileSync(
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
app.get("/api/download-file", async (req, res) => {
  try {
    console.log("IT IS WORKING.");

    const { submissionId } = req.query; 
    const { exec } = require('child_process');

    console.log("SUbM ID:", submissionId)
    exec('python3 mainf.py', async (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return res.status(500).json({ error: "Failed to execute Python script" });
      }
      //res.status(200).json({ message: "Data received and saved successfully and processed!" });
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);

      // Read filedata.json asynchronously to get the file information corresponding to the submission ID
      const filedata = await fsp.readFile(filedataFilePath, 'utf8');
      const fileData = JSON.parse(filedata)[submissionId];

      if (!fileData) {
        return res.status(404).json({ error: 'File data not found for submission ID' });
      }
      const { filename, filepath } = fileData;

      // Set Content-Type header to 'application/pdf'
      res.set('Content-Type', 'application/pdf');

      // Send the file for download
      res.download(filepath, filename, async (err) => {
        if (err) {
          console.error('Error downloading file:', err);
          return res.status(500).json({ error: 'Failed to download file' });
        } else {
          // Delete the file after it's downloaded
          await fsp.unlink(filepath);
          console.log('File deleted successfully');
          }
      });
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Route to serve the error.json file
app.get('/api/error', async (req, res) => {
  try {
    console.log('WERE HERE');
    // Read the error.json file and send its content as response
    const data = await fsp.readFile(errorFilePath, 'utf8');
    if (data !== null) {
      res.json(data);
    } else {
      res.json({ "download_error": "There was a problem with our network, please try again." });
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
app.setTimeout(() => {
  
}, timeout);
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
