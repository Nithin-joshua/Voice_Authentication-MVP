import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Enroll from "./pages/Enroll";
import Login from "./pages/Login";

// Admin imports
import AdminLogin from "./admin/AdminLogin";
import AdminLayout from "./admin/AdminLayout";
import Users from "./admin/Users";
import Logs from "./admin/Logs";

// Simple admin auth guard
const AdminRoute = ({ children }) => {
  const token = localStorage.getItem("admin_token");
  return token ? children : <Navigate to="/admin/login" />;
};

function App() {
  return (
    <Router>
      {/* ================= USER NAVBAR ================= */}
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
        <Link
          to="/admin"
          className="text-red-600 font-semibold hover:underline"
        >
          Admin
        </Link>
      </nav>

      {/* ================= ROUTES ================= */}
      <Routes>
        {/* User Routes */}
        <Route path="/enroll" element={<Enroll />} />
        <Route path="/login" element={<Login />} />

        {/* ================= ADMIN ROUTES ================= */}
        <Route path="/admin/login" element={<AdminLogin onLogin={() => window.location.href = "/admin"} />} />

        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminLayout>
                <Users />
              </AdminLayout>
            </AdminRoute>
          }
        />

        <Route
          path="/admin/logs"
          element={
            <AdminRoute>
              <AdminLayout>
                <Logs />
              </AdminLayout>
            </AdminRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
