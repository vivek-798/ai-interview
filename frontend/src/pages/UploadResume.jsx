import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("resume", file);

    const response = await fetch("http://127.0.0.1:5000/upload_resume", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      navigate("/aptitude");
    } else {
      alert("Upload failed");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "150px 8%" }}>
      <h2>Upload Your Resume</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} className="primary-btn">
        {loading ? "Processing..." : "Upload & Continue"}
      </button>
    </div>
  );
}
