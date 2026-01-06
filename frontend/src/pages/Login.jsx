import { useState } from "react";
import AudioRecorder from "../components/AudioRecorder";

export default function Login() {
  const [audioBlob, setAudioBlob] = useState(null);
  const [result, setResult] = useState(null);

  const authenticate = async () => {
    if (!audioBlob) return;

    const formData = new FormData();
    formData.append("file", audioBlob, "login.webm");

    try {
      const res = await fetch("http://127.0.0.1:8000/authenticate", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ authenticated: false });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-6">
      <h1 className="text-2xl font-bold">Voice Login</h1>

      <AudioRecorder onRecordingComplete={setAudioBlob} />

      <button
        onClick={authenticate}
        className="px-6 py-2 bg-green-600 text-white rounded"
      >
        Authenticate
      </button>

      {result && (
        <div className="text-center">
          <p>Similarity: {result.similarity_score}</p>
          <p className={result.authenticated ? "text-green-600" : "text-red-600"}>
            {result.authenticated ? "Access Granted" : "Access Denied"}
          </p>
        </div>
      )}
    </div>
  );
}
