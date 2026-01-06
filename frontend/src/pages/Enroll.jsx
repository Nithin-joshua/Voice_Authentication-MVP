import AudioRecorder from "../components/AudioRecorder";

export default function Enroll() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-6">
      <h1 className="text-2xl font-bold text-gray-800">
        Voice Enrollment
      </h1>

      <p className="text-gray-600 text-sm">
        Please record your voice to enroll.
      </p>

      <AudioRecorder />

      <button
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Submit Enrollment
      </button>
    </div>
  );
}
