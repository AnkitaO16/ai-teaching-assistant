import { useState } from "react";

type AnswerResponse = {
  answer: string;
  sources: string[];
};

export default function StudentChat() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState<AnswerResponse | null>(null);

  // dynamic fields
  const [className, setClassName] = useState("");
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);

    const formData = new FormData();
    formData.append("class_name", className);
    formData.append("subject", subject);
    formData.append("topic", topic);
    formData.append("question", question);

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setAnswer(data);
    } catch (err) {
      setAnswer({ answer: "❌ Failed to get answer.", sources: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleAsk} className="space-y-3">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Class"
            value={className}
            onChange={(e) => setClassName(e.target.value)}
            required
            className="flex-1 p-2 rounded-xl bg-input border border-border"
          />
          <input
            type="text"
            placeholder="Subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            required
            className="flex-1 p-2 rounded-xl bg-input border border-border"
          />
          <input
            type="text"
            placeholder="Topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
            className="flex-1 p-2 rounded-xl bg-input border border-border"
          />
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            required
            className="flex-1 p-3 rounded-xl bg-input border border-border"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-3 rounded-xl font-semibold bg-accent hover:brightness-110"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </form>

      {answer && (
        <div className="space-y-3">
          <div className="p-4 bg-input rounded-xl border border-border">
            <strong>Answer:</strong>
            <p className="mt-2">{answer.answer}</p>
          </div>
          {answer.sources?.length > 0 && (
            <div className="text-sm text-muted">
              Sources: {answer.sources.join(", ")}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
