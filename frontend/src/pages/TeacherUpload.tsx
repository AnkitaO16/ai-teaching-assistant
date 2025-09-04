// import { useState } from "react";
//
// export default function TeacherUpload() {
//   const [loading, setLoading] = useState(false);
//   const [status, setStatus] = useState<string | null>(null);
//
//   const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     setLoading(true);
//     setStatus(null);
//
//     const form = e.currentTarget;
//     const formData = new FormData(form);
//
//     try {
//       const res = await fetch("/api/ingest", {
//         method: "POST",
//         body: formData,
//       });
//
//       const data = await res.json();
//       setStatus(res.ok ? "✅ Notes ingested successfully!" : `❌ ${data.detail}`);
//     } catch (err) {
//       console.error(err);
//       setStatus("❌ Upload failed.");
//     } finally {
//       setLoading(false);
//     }
//   };
//
//   return (
//     <form onSubmit={handleSubmit} className="space-y-4">
//       <div className="bg-background text-muted">
//         <label className="block text-muted text-sm">Class</label>
//         <input
//           type="text"
//           name="class_name"
//           required
//           className="w-full p-3 rounded-xl bg-input border border-border"
//         />
//       </div>
//       <div>
//         <label className="block text-muted text-sm">Subject</label>
//         <input
//           type="text"
//           name="subject"
//           required
//           className="w-full p-3 rounded-xl bg-input border border-border"
//         />
//       </div>
//       <div>
//         <label className="block text-muted text-sm">Topic</label>
//         <input
//           type="text"
//           name="topic"
//           required
//           className="w-full p-3 rounded-xl bg-input border border-border"
//         />
//       </div>
//       <div>
//         <label className="block text-muted text-sm">Upload Notes </label>
//
// <input type="file" name="file" accept=".pdf" required />
//
//       </div>
//
//       <button
//         type="submit"
//         disabled={loading}
//         className="w-full py-3 rounded-xl font-semibold bg-accent hover:brightness-110"
//       >
//         {loading ? "Uploading..." : "Upload"}
//       </button>
//
//       {status && (
//         <div
//           className={`mt-3 p-2 rounded-xl text-sm ${
//             status.startsWith("✅") ? "text-ok" : "text-err"
//           }`}
//         >
//           {status}
//         </div>
//       )}
//     </form>
//   );
// }
import { useState } from "react";
import styled from "styled-components";

const Form = styled.form`
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 16px;
  background: #f9fafb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
`;

const Field = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
`;

const Input = styled.input`
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  background: white;
  font-size: 1rem;
  transition: 0.2s;

  &:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
  }
`;

const FileInput = styled(Input)`
  padding: 0.5rem;
`;

const Button = styled.button`
  padding: 0.9rem;
  border: none;
  border-radius: 12px;
  background: #6366f1;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;

  &:hover {
    background: #4f46e5;
  }

  &:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }
`;

const Status = styled.div<{ success: boolean }>`
  padding: 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
  color: ${(props) => (props.success ? "#059669" : "#dc2626")};
  background: ${(props) => (props.success ? "#d1fae5" : "#fee2e2")};
`;

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
    <Form onSubmit={handleSubmit}>
      <Field>
        <Label>Class</Label>
        <Input type="text" name="class_name" required />
      </Field>

      <Field>
        <Label>Subject</Label>
        <Input type="text" name="subject" required />
      </Field>

      <Field>
        <Label>Topic</Label>
        <Input type="text" name="topic" required />
      </Field>

      <Field>
        <Label>Upload Notes</Label>
        <FileInput type="file" name="file" accept=".pdf" required />
      </Field>

      <Button type="submit" disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </Button>

      {status && <Status success={status.startsWith("✅")}>{status}</Status>}
    </Form>
  );
}
