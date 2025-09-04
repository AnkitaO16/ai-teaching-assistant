// import { useState } from "react";
// import { motion } from "framer-motion";
//
// type AnswerResponse = {
//   answer: string;
//   sources: string[];
// };
//
// export default function StudentChat() {
//   const [question, setQuestion] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [chats, setChats] = useState<
//     { type: "student" | "assistant"; text: string; sources?: string[] }[]
//   >([]);
//
//   // dynamic fields
//   const [className, setClassName] = useState("");
//   const [subject, setSubject] = useState("");
//   const [topic, setTopic] = useState("");
//
//   const handleAsk = async (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!question.trim()) return;
//
//     // push student message
//     setChats((prev) => [...prev, { type: "student", text: question }]);
//
//     setLoading(true);
//
//     const formData = new FormData();
//     formData.append("class_name", className);
//     formData.append("subject", subject);
//     formData.append("topic", topic);
//     formData.append("question", question);
//
//     try {
//       const res = await fetch("/api/ask", {
//         method: "POST",
//         body: formData,
//       });
//       const data: AnswerResponse = await res.json();
//
//       // push assistant response
//       setChats((prev) => [
//         ...prev,
//         { type: "assistant", text: data.answer, sources: data.sources },
//       ]);
//     } catch {
//       setChats((prev) => [
//         ...prev,
//         { type: "assistant", text: "❌ Failed to get answer." },
//       ]);
//     } finally {
//       setLoading(false);
//       setQuestion("");
//     }
//   };
//
//   return (
//     <div className="max-w-3xl mx-auto h-[80vh] flex flex-col rounded-2xl shadow-lg bg-background border border-border">
//       {/* Header */}
//       <header className="p-4 border-b border-border text-center font-bold text-xl text-accent">
//         🎓 Student Q&A Assistant
//       </header>
//
//       {/* Chat area */}
//       <div className="flex-1 overflow-y-auto p-6 space-y-4">
//         {chats.map((chat, idx) => (
//           <motion.div
//             key={idx}
//             initial={{ opacity: 0, y: 5 }}
//             animate={{ opacity: 1, y: 0 }}
//             className={`max-w-[75%] p-3 rounded-2xl ${
//               chat.type === "student"
//                 ? "ml-auto bg-accent text-white"
//                 : "mr-auto bg-input border border-border"
//             }`}
//           >
//             <p>{chat.text}</p>
//             {chat.sources && chat.sources.length > 0 && (
//               <p className="text-xs text-muted mt-2">
//                 📚 Sources: {chat.sources.join(", ")}
//               </p>
//             )}
//           </motion.div>
//         ))}
//         {loading && (
//           <p className="text-sm text-muted italic">🤖 Thinking...</p>
//         )}
//       </div>
//
//       {/* Input bar */}
//       <form
//         onSubmit={handleAsk}
//         className="p-4 border-t border-border flex gap-2 bg-background"
//       >
//         <input
//           type="text"
//           placeholder="Class"
//           value={className}
//           onChange={(e) => setClassName(e.target.value)}
//           className="w-24 p-2 rounded-xl bg-input border border-border text-sm"
//           required
//         />
//         <input
//           type="text"
//           placeholder="Subject"
//           value={subject}
//           onChange={(e) => setSubject(e.target.value)}
//           className="w-28 p-2 rounded-xl bg-input border border-border text-sm"
//           required
//         />
//         <input
//           type="text"
//           placeholder="Topic"
//           value={topic}
//           onChange={(e) => setTopic(e.target.value)}
//           className="w-28 p-2 rounded-xl bg-input border border-border text-sm"
//           required
//         />
//         <input
//           type="text"
//           value={question}
//           onChange={(e) => setQuestion(e.target.value)}
//           placeholder="Ask a question..."
//           className="flex-1 p-2 rounded-xl bg-input border border-border"
//           required
//         />
//         <motion.button
//           type="submit"
//           disabled={loading}
//           whileTap={{ scale: 0.95 }}
//           className="px-5 py-2 rounded-xl font-semibold bg-accent text-white hover:brightness-110 transition"
//         >
//           Ask
//         </motion.button>
//       </form>
//     </div>
//   );
// }
import { useState } from "react";
import styled from "styled-components";
import { motion } from "framer-motion";

type AnswerResponse = {
  answer: string;
  sources: string[];
};

// 🎨 Styled Components
const Container = styled.div`
  max-width: max-content;
  height: 80vh;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
`;

const Header = styled.header`
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: center;
  font-weight: bold;
  font-size: 1.25rem;
  color: #2563eb;
`;

const ChatArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const Message = styled(motion.div)<{ type: "student" | "assistant" }>`
  max-width: 75%;
  padding: 12px;
  border-radius: 16px;
  font-size: 0.95rem;
  line-height: 1.4;

  ${({ type }) =>
    type === "student"
      ? `
        margin-left: auto;
        background: #2563eb;
        color: white;
      `
      : `
        margin-right: auto;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
      `}
`;

const Sources = styled.p`
  font-size: 0.75rem;
  margin-top: 6px;
  color: #6b7280;
`;

const InputBar = styled.form`
  display: flex;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid #e5e7eb;
  background: #ffffff;
`;

const Input = styled.input`
  padding: 8px 12px;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  font-size: 0.875rem;
  flex-shrink: 0;

  &:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
  }
`;

const QuestionInput = styled(Input)`
  flex: 1;
`;

const Button = styled(motion.button)`
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 600;
  background: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  transition: filter 0.2s;

  &:hover {
    filter: brightness(1.1);
  }

  &:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
`;

export default function StudentChat() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [chats, setChats] = useState<
    { type: "student" | "assistant"; text: string; sources?: string[] }[]
  >([]);

  const [className, setClassName] = useState("");
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setChats((prev) => [...prev, { type: "student", text: question }]);
    setLoading(true);

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
      const data: AnswerResponse = await res.json();
      setChats((prev) => [
        ...prev,
        { type: "assistant", text: data.answer, sources: data.sources },
      ]);
    } catch {
      setChats((prev) => [
        ...prev,
        { type: "assistant", text: "❌ Failed to get answer." },
      ]);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <Container>
      <Header>🎓 Student Q&A Assistant</Header>

      <ChatArea>
        {chats.map((chat, idx) => (
          <Message
            key={idx}
            type={chat.type}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {chat.text}
            {chat.sources && chat.sources.length > 0 && (
              <Sources>📚 Sources: {chat.sources.join(", ")}</Sources>
            )}
          </Message>
        ))}
        {loading && <p style={{ fontStyle: "italic", color: "#6b7280" }}>🤖 Thinking...</p>}
      </ChatArea>

      <InputBar onSubmit={handleAsk}>
        <Input
          type="text"
          placeholder="Class"
          value={className}
          onChange={(e) => setClassName(e.target.value)}
          required
        />
        <Input
          type="text"
          placeholder="Subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          required
        />
        <Input
          type="text"
          placeholder="Topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          required
        />
        <QuestionInput
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          required
        />
        <Button type="submit" disabled={loading} whileTap={{ scale: 0.95 }}>
          Ask
        </Button>
      </InputBar>
    </Container>
  );
}
