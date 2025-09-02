import { ReactNode } from "react";
import { NavLink } from "react-router-dom";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="flex items-center gap-6 px-6 py-4 border-b border-border bg-bg">
        <div className="font-extrabold text-lg">🧠 AI Tutor</div>
        <nav className="flex gap-3">
          <NavLink
            to="/teacher"
            className={({ isActive }) =>
              `px-3 py-2 rounded-xl ${isActive ? "bg-card text-text" : "text-muted hover:bg-card"}`
            }
          >
            Teacher Upload
          </NavLink>
          <NavLink
            to="/student"
            className={({ isActive }) =>
              `px-3 py-2 rounded-xl ${isActive ? "bg-card text-text" : "text-muted hover:bg-card"}`
            }
          >
            Student Chat
          </NavLink>
        </nav>
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto p-6">
        <div className="bg-card border border-border rounded-2xl shadow-lg p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
