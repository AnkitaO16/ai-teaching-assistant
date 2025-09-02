import { useState } from "react";

export default function TeacherUpload() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);

    const form = e.currentTarget;
    const formData = new FormData(form);

    try {
      const res = await fetch("/api/ingest", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setStatus(res.ok ? "✅ Notes ingested successfully!" : `❌ ${data.detail}`);
    } catch (err) {
      console.error(err);
      setStatus("❌ Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="bg-bg text-muted">
        <label className="block text-muted text-sm">Class</label>
        <input
          type="text"
          name="class_name"
          required
          className="w-full p-3 rounded-xl bg-input border border-border"
        />
      </div>
      <div>
        <label className="block text-muted text-sm">Subject</label>
        <input
          type="text"
          name="subject"
          required
          className="w-full p-3 rounded-xl bg-input border border-border"
        />
      </div>
      <div>
        <label className="block text-muted text-sm">Topic</label>
        <input
          type="text"
          name="topic"
          required
          className="w-full p-3 rounded-xl bg-input border border-border"
        />
      </div>
      <div>
        <label className="block text-muted text-sm">Upload Notes </label>

<input type="file" name="file" accept=".pdf" required />

      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 rounded-xl font-semibold bg-accent hover:brightness-110"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {status && (
        <div
          className={`mt-3 p-2 rounded-xl text-sm ${
            status.startsWith("✅") ? "text-ok" : "text-err"
          }`}
        >
          {status}
        </div>
      )}
    </form>
  );
}
