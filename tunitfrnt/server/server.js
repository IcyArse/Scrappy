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
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
