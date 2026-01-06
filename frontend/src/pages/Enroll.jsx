import { useState } from "react";
import AudioRecorder from "../components/AudioRecorder";

export default function Enroll() {
  const [audioBlob, setAudioBlob] = useState(null);
  const [message, setMessage] = useState("");

  const submitEnrollment = async () => {
    if (!audioBlob) {
      setMessage("Please record your voice first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", audioBlob, "enroll.webm");

    try {
      const res = await fetch("http://127.0.0.1:8000/enroll", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setMessage(data.message || "Enrollment completed");
    } catch (err) {
      setMessage("Enrollment failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-6">
      <h1 className="text-2xl font-bold">Voice Enrollment</h1>

      <AudioRecorder onRecordingComplete={setAudioBlob} />

      <button
        onClick={submitEnrollment}
        className="px-6 py-2 bg-blue-600 text-white rounded"
      >
        Submit Enrollment
      </button>

      {message && <p className="text-gray-700">{message}</p>}
    </div>
  );
}
