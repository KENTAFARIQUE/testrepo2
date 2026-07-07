import SubmitForm from "../components/SubmitForm";
import JobList from "../components/JobList";

export default function HomePage() {
  return (
    <div>
      <h2 className="mb-6 text-xl font-semibold text-gray-800">
        Submit a YouTube Video
      </h2>
      <SubmitForm />
      <div className="mt-10">
        <h3 className="mb-4 text-lg font-semibold text-gray-800">Jobs</h3>
        <JobList />
      </div>
    </div>
  );
}
