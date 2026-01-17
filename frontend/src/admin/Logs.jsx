import { useEffect, useState } from "react";
import { fetchLogs } from "./api";

export default function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetchLogs().then((data) => setLogs(data.logs || []));
  }, []);

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Authentication Logs</h1>
      <ul className="space-y-2">
        {logs.map((l, i) => (
          <li key={i} className="bg-white p-3 rounded shadow">
            <b>{l.email}</b> — {l.success ? "Success" : "Fail"}  
            <br />
            <small>{l.reason}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
