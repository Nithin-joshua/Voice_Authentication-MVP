export default function AdminLayout({ children }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-60 bg-black text-white p-4">
        <h2 className="text-lg font-bold mb-6">Admin Panel</h2>
        <ul className="space-y-3">
          <li>Dashboard</li>
          <li>Users</li>
          <li>Logs</li>
        </ul>
      </aside>

      <main className="flex-1 p-6 bg-gray-100">{children}</main>
    </div>
  );
}
