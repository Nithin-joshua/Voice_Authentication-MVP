import { useState } from "react";
import AudioRecorder from "../components/AudioRecorder";

export default function Enroll() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [audioBlob, setAudioBlob] = useState(null);
  const [message, setMessage] = useState("");

  const submitEnrollment = async () => {
    if (!name || !email || !audioBlob) {
      setMessage("Please fill all fields and record your voice.");
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("file", audioBlob);

    try {
      const res = await fetch("http://127.0.0.1:8000/enroll", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setMessage(data.message || "Enrollment successful");
    } catch (err) {
      console.error(err);
      setMessage("Enrollment failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-5">
      <h1 className="text-2xl font-bold">Voice Enrollment</h1>

      <input
        type="text"
        placeholder="Full Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="px-4 py-2 border rounded w-80"
      />

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="px-4 py-2 border rounded w-80"
      />

      <AudioRecorder onRecordingComplete={setAudioBlob} />

      <button
        onClick={submitEnrollment}
        disabled={!name || !email || !audioBlob}
        className={`px-6 py-2 rounded text-white ${
          name && email && audioBlob
            ? "bg-blue-600 hover:bg-blue-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        Enroll
      </button>

      {message && <p className="text-gray-700">{message}</p>}
    </div>
  );
}
