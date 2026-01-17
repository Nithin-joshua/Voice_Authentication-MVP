import { useEffect, useState } from "react";
import { fetchUsers, toggleUser } from "./api";

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers().then((data) => setUsers(data.users || []));
  }, []);

  const toggle = async (id, active) => {
    await toggleUser(id, !active);
    setUsers((prev) =>
      prev.map((u) =>
        u.id === id ? { ...u, is_active: !active } : u
      )
    );
  };

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Users</h1>
      <table className="w-full bg-white shadow rounded">
        <thead>
          <tr className="border-b">
            <th className="p-2">Email</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id} className="border-b text-center">
              <td className="p-2">{u.email}</td>
              <td>{u.is_active ? "Active" : "Disabled"}</td>
              <td>
                <button
                  onClick={() => toggle(u.id, u.is_active)}
                  className="px-3 py-1 bg-gray-800 text-white rounded"
                >
                  {u.is_active ? "Disable" : "Enable"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
