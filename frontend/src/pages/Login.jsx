import { useState } from "react";
import AudioRecorder from "../components/AudioRecorder";

export default function Login() {
  const [email, setEmail] = useState("");
  const [audioBlob, setAudioBlob] = useState(null);
  const [result, setResult] = useState(null);
  const [challenge, setChallenge] = useState("");
  const [loadingChallenge, setLoadingChallenge] = useState(false);

  // 🔐 Fetch challenge from backend
  const fetchChallenge = async () => {
    if (!email) {
      alert("Enter email first");
      return;
    }

    setLoadingChallenge(true);
    setResult(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/challenge?email=${email}`
      );
      const data = await res.json();

      if (data.challenge) {
        setChallenge(data.challenge);
      } else {
        alert("Failed to get challenge");
      }
    } catch (err) {
      console.error(err);
      alert("Challenge service unavailable");
    } finally {
      setLoadingChallenge(false);
    }
  };

  // 🔐 Authenticate with challenge + voice
  const authenticate = async () => {
    if (!email || !audioBlob || !challenge) {
      alert("Get challenge and record your voice first");
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
      <h1 className="text-2xl font-bold">Secure Voice Login</h1>

      {/* Email Input */}
      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="px-4 py-2 border rounded w-80"
      />

      {/* Challenge Button */}
      <button
        onClick={fetchChallenge}
        disabled={!email || loadingChallenge}
        className={`px-4 py-2 rounded text-white ${
          email
            ? "bg-blue-600 hover:bg-blue-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        {loadingChallenge ? "Generating..." : "Get Challenge"}
      </button>

      {/* Show Challenge */}
      {challenge && (
        <p className="text-center font-semibold text-gray-700">
          Please say:
          <br />
          <span className="text-blue-600">"{challenge}"</span>
        </p>
      )}

      {/* Audio Recorder */}
      <AudioRecorder onRecordingComplete={setAudioBlob} />

      {/* Login Button */}
      <button
        onClick={authenticate}
        disabled={!email || !audioBlob || !challenge}
        className={`px-6 py-2 rounded text-white ${
          email && audioBlob && challenge
            ? "bg-green-600 hover:bg-green-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        Login
      </button>

      {/* Result */}
      {result && (
        <div className="text-center">
          <p>Similarity Score: {result.similarity_score}</p>
          <p>Variance Score: {result.variance_score}</p>
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
