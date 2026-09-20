import { z } from "zod";

// Mirrors apps/api/src/pulse_api/interface/v1/schemas.py.
// This is the single source of truth for the web <-> api contract; the
// consumer pact test (apps/web) and provider verification test (apps/api)
// both assert against shapes derived from it.

export const pollOptionSchema = z.object({
  id: z.string().uuid(),
  label: z.string(),
  votes: z.number().int().nonnegative(),
});

export const pollSchema = z.object({
  id: z.string().uuid(),
  question: z.string(),
  isClosed: z.boolean(),
  createdAt: z.string(),
  totalVotes: z.number().int().nonnegative(),
  options: z.array(pollOptionSchema),
});

export const createPollRequestSchema = z.object({
  question: z.string().min(3).max(280),
  options: z.array(z.string()).min(2).max(10),
});

export const castVoteRequestSchema = z.object({
  optionId: z.string().uuid(),
});

export type PollOption = z.infer<typeof pollOptionSchema>;
export type Poll = z.infer<typeof pollSchema>;
export type CreatePollRequest = z.infer<typeof createPollRequestSchema>;
export type CastVoteRequest = z.infer<typeof castVoteRequestSchema>;
