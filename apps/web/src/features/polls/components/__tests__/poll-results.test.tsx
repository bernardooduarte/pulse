import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PollResults } from "@/features/polls/components/poll-results";
import type { Poll } from "@pulse/contracts";

const poll: Poll = {
  id: "9c858901-8a57-4791-81fe-4c455b099bc9",
  question: "Tabs or spaces?",
  isClosed: false,
  createdAt: new Date().toISOString(),
  totalVotes: 4,
  options: [
    { id: "1", label: "Tabs", votes: 1 },
    { id: "2", label: "Spaces", votes: 3 },
  ],
};

describe("PollResults", () => {
  it("renders each option with its vote count and percentage", () => {
    render(<PollResults poll={poll} />);

    expect(screen.getByText(/Tabs/)).toBeInTheDocument();
    expect(screen.getByText(/1 votes \(25%\)/)).toBeInTheDocument();
    expect(screen.getByText(/Spaces/)).toBeInTheDocument();
    expect(screen.getByText(/3 votes \(75%\)/)).toBeInTheDocument();
  });

  it("renders 0% for every option when there are no votes yet", () => {
    render(<PollResults poll={{ ...poll, totalVotes: 0, options: poll.options.map((o) => ({ ...o, votes: 0 })) }} />);

    expect(screen.getAllByText(/0 votes \(0%\)/)).toHaveLength(2);
  });
});
