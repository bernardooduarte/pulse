import { defineConfig } from "vitest/config";
import path from "node:path";

// Separate config: pact consumer tests spin up a real mock provider on a
// port and need Node (not jsdom) plus a longer timeout than UI unit tests.
export default defineConfig({
  test: {
    environment: "node",
    include: ["**/*.pact.test.ts"],
    testTimeout: 30_000,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
