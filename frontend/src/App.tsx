import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import TeacherUpload from "./pages/TeacherUpload";
import StudentChat from "./pages/StudentChat";


function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/teacher" replace />} />
          <Route path="/teacher" element={<TeacherUpload />} />
          <Route path="/student" element={<StudentChat />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
