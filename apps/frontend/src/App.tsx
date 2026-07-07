import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import JobDetailPage from "./pages/JobDetailPage";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white px-6 py-4 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">TubeDigest</h1>
      </header>
      <main className="mx-auto max-w-4xl px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/jobs/:id" element={<JobDetailPage />} />
        </Routes>
      </main>
    </div>
  );
}
