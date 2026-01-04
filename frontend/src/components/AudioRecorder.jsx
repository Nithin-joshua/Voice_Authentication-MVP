import { useRef, useState } from "react";

export default function AudioRecorder() {
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstop = async () => {
  const audioBlob = new Blob(audioChunksRef.current, {
    type: "audio/webm",
  });

  const formData = new FormData();
  formData.append("file", audioBlob, "voice.webm");

  try {
    const response = await fetch("http://127.0.0.1:8000/upload-test", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Backend response:", data);
  } catch (error) {
    console.error("Upload failed:", error);
  }
};


    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4 text-center">
        Voice Recorder
      </h2>

      <div className="flex justify-center gap-4 mb-4">
        {!recording ? (
          <button
            onClick={startRecording}
            className="px-4 py-2 bg-green-600 text-white rounded"
          >
            Start Recording
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="px-4 py-2 bg-red-600 text-white rounded"
          >
            Stop Recording
          </button>
        )}
      </div>

      {audioURL && (
        <div className="mt-4">
          <p className="text-sm text-gray-600 mb-2">Recorded Audio:</p>
          <audio controls src={audioURL} className="w-full" />
        </div>
      )}
    </div>
  );
}
