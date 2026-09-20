from __future__ import annotations

from uuid import uuid4

import pytest

from pulse_api.domain.entities import DomainError, OptionNotFoundError, Poll, PollClosedError


def test_create_poll_requires_at_least_two_options() -> None:
    with pytest.raises(DomainError):
        Poll.create(question="Coffee or tea?", option_labels=["Coffee"])


def test_cast_vote_increments_option_count() -> None:
    poll = Poll.create(question="Coffee or tea?", option_labels=["Coffee", "Tea"])
    target = poll.options[0]

    poll.cast_vote(target.id)

    assert target.votes == 1
    assert poll.total_votes == 1


def test_cast_vote_on_closed_poll_raises() -> None:
    poll = Poll.create(question="Coffee or tea?", option_labels=["Coffee", "Tea"])
    poll.is_closed = True

    with pytest.raises(PollClosedError):
        poll.cast_vote(poll.options[0].id)


def test_cast_vote_on_unknown_option_raises() -> None:
    poll = Poll.create(question="Coffee or tea?", option_labels=["Coffee", "Tea"])

    with pytest.raises(OptionNotFoundError):
        poll.cast_vote(option_id=uuid4())
