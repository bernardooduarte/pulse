import type { Poll } from "@pulse/contracts";

export function PollResults({ poll }: { poll: Poll }) {
  return (
    <ul className="space-y-2" aria-label="poll results">
      {poll.options.map((option) => {
        const pct = poll.totalVotes === 0 ? 0 : Math.round((option.votes / poll.totalVotes) * 100);
        return (
          <li key={option.id} className="rounded border border-slate-200 p-3">
            <div className="flex justify-between text-sm font-medium">
              <span>{option.label}</span>
              <span>
                {option.votes} votes ({pct}%)
              </span>
            </div>
            <div className="mt-2 h-2 rounded bg-slate-100">
              <div
                className="h-2 rounded bg-slate-900 transition-all"
                style={{ width: `${pct}%` }}
              />
            </div>
          </li>
        );
      })}
    </ul>
  );
}
