from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from pulse_api.domain.entities import Poll


class CamelModel(BaseModel):
    """Base for schemas exposed over HTTP: wire format is camelCase, matching
    @pulse/contracts on the frontend, while Python code keeps snake_case."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class CreatePollRequest(CamelModel):
    question: str = Field(min_length=3, max_length=280)
    options: list[str] = Field(min_length=2, max_length=10)


class PollOptionResponse(CamelModel):
    id: UUID
    label: str
    votes: int


class PollResponse(CamelModel):
    id: UUID
    question: str
    is_closed: bool
    created_at: datetime
    total_votes: int
    options: list[PollOptionResponse]

    @staticmethod
    def from_domain(poll: Poll) -> PollResponse:
        return PollResponse(
            id=poll.id,
            question=poll.question,
            is_closed=poll.is_closed,
            created_at=poll.created_at,
            total_votes=poll.total_votes,
            options=[
                PollOptionResponse(id=o.id, label=o.label, votes=o.votes) for o in poll.options
            ],
        )


class CastVoteRequest(CamelModel):
    option_id: UUID
