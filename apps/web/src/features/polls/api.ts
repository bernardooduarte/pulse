import {
  castVoteRequestSchema,
  createPollRequestSchema,
  pollSchema,
  type CreatePollRequest,
  type Poll,
} from "@pulse/contracts";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function parseOrThrow<T>(response: Response, schema: { parse: (v: unknown) => T }) {
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Pulse API error ${response.status}: ${body}`);
  }
  return schema.parse(await response.json());
}

export async function createPoll(input: CreatePollRequest): Promise<Poll> {
  const body = createPollRequestSchema.parse(input);
  const response = await fetch(`${API_BASE_URL}/api/v1/polls`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseOrThrow(response, pollSchema);
}

export async function getPoll(pollId: string): Promise<Poll> {
  const response = await fetch(`${API_BASE_URL}/api/v1/polls/${pollId}`, {
    cache: "no-store",
  });
  return parseOrThrow(response, pollSchema);
}

export async function castVote(pollId: string, optionId: string): Promise<Poll> {
  const body = castVoteRequestSchema.parse({ optionId });
  const response = await fetch(`${API_BASE_URL}/api/v1/polls/${pollId}/votes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseOrThrow(response, pollSchema);
}
