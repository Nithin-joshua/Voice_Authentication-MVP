const API_BASE = "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("admin_token");
}

export async function adminLogin(email, password) {
  const res = await fetch(`${API_BASE}/admin/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

export async function fetchUsers() {
  return fetch(`${API_BASE}/admin/users`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  }).then((r) => r.json());
}

export async function toggleUser(userId, enable) {
  const action = enable ? "enable" : "disable";
  return fetch(`${API_BASE}/admin/users/${userId}/${action}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });
}

export async function fetchLogs() {
  return fetch(`${API_BASE}/admin/logs`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  }).then((r) => r.json());
}
