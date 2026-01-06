import AudioRecorder from "../components/AudioRecorder";

export default function Login() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center gap-6">
      <h1 className="text-2xl font-bold text-gray-800">
        Voice Login
      </h1>

      <p className="text-gray-600 text-sm">
        Record your voice to authenticate.
      </p>

      <AudioRecorder />

      <button
        className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Authenticate
      </button>
    </div>
  );
}
