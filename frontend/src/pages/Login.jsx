import { useState } from "react";
import AudioRecorder from "../components/AudioRecorder";

export default function Login() {
  const [email, setEmail] = useState("");
  const [audioBlob, setAudioBlob] = useState(null);
  const [result, setResult] = useState(null);

  const authenticate = async () => {
    if (!email || !audioBlob) {
      alert("Please enter email and record your voice");
      return;
    }

    const formData = new FormData();
    formData.append("email", email);
    formData.append("file", audioBlob);

    try {
      const res = await fetch("http://127.0.0.1:8000/authenticate", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ authenticated: false });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-5">
      <h1 className="text-2xl font-bold">Voice Login</h1>

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="px-4 py-2 border rounded w-80"
      />

      <AudioRecorder onRecordingComplete={setAudioBlob} />

      <button
        onClick={authenticate}
        disabled={!email || !audioBlob}
        className={`px-6 py-2 rounded text-white ${
          email && audioBlob
            ? "bg-green-600 hover:bg-green-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        Login
      </button>

      {result && (
        <div className="text-center">
          <p>Similarity Score: {result.similarity_score}</p>
          <p
            className={
              result.authenticated ? "text-green-600" : "text-red-600"
            }
          >
            {result.authenticated ? "Access Granted" : "Access Denied"}
          </p>
        </div>
      )}
    </div>
  );
}
