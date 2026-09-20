from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4


class DomainError(Exception):
    """Base class for errors raised by the domain layer."""


class PollClosedError(DomainError):
    """Raised when a vote is cast on a poll that is no longer accepting votes."""


class OptionNotFoundError(DomainError):
    """Raised when a vote targets an option that does not belong to the poll."""


@dataclass(slots=True)
class PollOption:
    id: UUID
    label: str
    votes: int = 0


@dataclass(slots=True)
class Poll:
    id: UUID
    question: str
    options: list[PollOption]
    created_at: datetime
    is_closed: bool = False

    @staticmethod
    def create(question: str, option_labels: list[str]) -> Poll:
        if len(option_labels) < 2:
            raise DomainError("A poll needs at least two options.")
        return Poll(
            id=uuid4(),
            question=question,
            options=[PollOption(id=uuid4(), label=label) for label in option_labels],
            created_at=datetime.now(UTC),
        )

    def cast_vote(self, option_id: UUID) -> PollOption:
        if self.is_closed:
            raise PollClosedError(f"Poll {self.id} is closed for voting.")
        for option in self.options:
            if option.id == option_id:
                option.votes += 1
                return option
        raise OptionNotFoundError(f"Option {option_id} does not belong to poll {self.id}.")

    @property
    def total_votes(self) -> int:
        return sum(option.votes for option in self.options)
