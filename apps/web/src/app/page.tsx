import { CreatePollForm } from "@/features/polls/components/create-poll-form";

export default function HomePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Pulse</h1>
        <p className="text-slate-600">Create a poll and share it in seconds.</p>
      </div>
      <CreatePollForm />
    </div>
  );
}
