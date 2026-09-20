import { PollVotingCard } from "@/features/polls/components/poll-voting-card";

export default async function PollPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <PollVotingCard pollId={id} />;
}
