"use client";

import { useState } from "react";
import { usePoll, useCastVote } from "@/features/polls/hooks/use-poll";
import { PollResults } from "@/features/polls/components/poll-results";

export function PollVotingCard({ pollId }: { pollId: string }) {
  const { data: poll, isLoading, isError } = usePoll(pollId);
  const castVote = useCastVote(pollId);
  const [votedOptionId, setVotedOptionId] = useState<string | null>(null);

  if (isLoading) return <p role="status">Loading poll...</p>;
  if (isError || !poll) return <p role="alert">Could not load this poll.</p>;

  const hasVoted = votedOptionId !== null;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">{poll.question}</h1>

      {hasVoted || poll.isClosed ? (
        <PollResults poll={poll} />
      ) : (
        <div className="space-y-2">
          {poll.options.map((option) => (
            <button
              key={option.id}
              type="button"
              disabled={castVote.isPending}
              onClick={() => {
                setVotedOptionId(option.id);
                castVote.mutate(option.id);
              }}
              className="w-full rounded border border-slate-300 p-3 text-left hover:border-slate-900 disabled:opacity-50"
            >
              {option.label}
            </button>
          ))}
        </div>
      )}

      {castVote.isError && (
        <p role="alert" className="text-sm text-red-600">
          Your vote could not be recorded. Please try again.
        </p>
      )}
    </div>
  );
}
