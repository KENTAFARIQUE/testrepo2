import { useParams } from "react-router-dom";

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  return (
    <div>
      <p className="text-gray-500">Job Detail Page — job id: {id}</p>
    </div>
  );
}
