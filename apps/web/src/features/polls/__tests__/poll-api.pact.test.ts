import path from "node:path";
import { MatchersV3, PactV3 } from "@pact-foundation/pact";
import { describe, expect, it } from "vitest";

// Consumer-driven contract test. This records what the frontend expects
// from the API into a pact file, which apps/api/tests/contract then
// replays against the real FastAPI app to verify the provider honours it.
const provider = new PactV3({
  consumer: "pulse-web",
  provider: "pulse-api",
  dir: path.resolve(__dirname, "../../../../../../pacts"),
});

const { like, eachLike, uuid, regex, integer, boolean } = MatchersV3;

describe("Poll API contract", () => {
  it("returns a poll by id", async () => {
    const pollId = "9c858901-8a57-4791-81fe-4c455b099bc9";

    provider
      .given("a poll exists")
      .uponReceiving("a request for an existing poll")
      .withRequest({ method: "GET", path: `/api/v1/polls/${pollId}` })
      .willRespondWith({
        status: 200,
        headers: { "Content-Type": "application/json" },
        body: like({
          id: uuid(pollId),
          question: "Tabs or spaces?",
          isClosed: boolean(false),
          createdAt: regex(
            /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/,
            "2026-09-20T00:00:00.000000Z",
          ),
          totalVotes: integer(0),
          options: eachLike({
            id: uuid(),
            label: "Tabs",
            votes: integer(0),
          }),
        }),
      });

    await provider.executeTest(async (mockServer) => {
      const response = await fetch(`${mockServer.url}/api/v1/polls/${pollId}`);
      const body = await response.json();

      expect(response.status).toBe(200);
      expect(body.question).toBe("Tabs or spaces?");
    });
  });
});
