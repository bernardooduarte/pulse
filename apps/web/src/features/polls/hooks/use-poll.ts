import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { castVote, getPoll } from "@/features/polls/api";

export function usePoll(pollId: string) {
  return useQuery({
    queryKey: ["poll", pollId],
    queryFn: () => getPoll(pollId),
    refetchInterval: 4_000, // simple polling refresh; good enough for a demo, swap for SSE/websockets at scale
  });
}

export function useCastVote(pollId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (optionId: string) => castVote(pollId, optionId),
    onSuccess: (poll) => {
      queryClient.setQueryData(["poll", pollId], poll);
    },
  });
}
