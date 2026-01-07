import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Enroll from "./pages/Enroll";
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      {/* Navigation Bar */}
      <nav className="w-full bg-white shadow-md py-4 flex justify-center gap-8">
        <Link
          to="/enroll"
          className="text-blue-600 font-semibold hover:underline"
        >
          Enroll
        </Link>
        <Link
          to="/login"
          className="text-green-600 font-semibold hover:underline"
        >
          Login
        </Link>
      </nav>

      {/* Routes */}
      <Routes>
        <Route path="/enroll" element={<Enroll />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
