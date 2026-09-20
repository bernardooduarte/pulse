"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { createPoll } from "@/features/polls/api";

export function CreatePollForm() {
  const router = useRouter();
  const [question, setQuestion] = useState("");
  const [options, setOptions] = useState(["", ""]);

  const mutation = useMutation({
    mutationFn: () =>
      createPoll({ question, options: options.filter((o) => o.trim().length > 0) }),
    onSuccess: (poll) => router.push(`/polls/${poll.id}`),
  });

  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        mutation.mutate();
      }}
    >
      <label className="block">
        <span className="text-sm font-medium">Question</span>
        <input
          className="mt-1 w-full rounded border border-slate-300 p-2"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
          minLength={3}
        />
      </label>

      {options.map((value, index) => (
        <label key={index} className="block">
          <span className="text-sm font-medium">Option {index + 1}</span>
          <input
            className="mt-1 w-full rounded border border-slate-300 p-2"
            value={value}
            onChange={(e) => {
              const next = [...options];
              next[index] = e.target.value;
              setOptions(next);
            }}
          />
        </label>
      ))}

      <button
        type="button"
        onClick={() => setOptions([...options, ""])}
        className="text-sm text-slate-600 underline"
      >
        Add option
      </button>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="w-full rounded bg-slate-900 p-2 text-white disabled:opacity-50"
      >
        {mutation.isPending ? "Creating..." : "Create poll"}
      </button>

      {mutation.isError && (
        <p role="alert" className="text-sm text-red-600">
          Could not create the poll. Check the question and options and try again.
        </p>
      )}
    </form>
  );
}
