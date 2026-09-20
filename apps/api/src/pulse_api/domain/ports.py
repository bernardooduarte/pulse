from __future__ import annotations

from typing import Protocol
from uuid import UUID

from pulse_api.domain.entities import Poll


class PollRepository(Protocol):
    """Outbound port. Infrastructure adapters implement this contract.

    Keeping it a Protocol (not an ABC) means the application layer depends
    only on a shape, never on SQLAlchemy or any other infrastructure detail.
    """

    async def add(self, poll: Poll) -> None: ...

    async def get(self, poll_id: UUID) -> Poll | None: ...

    async def save(self, poll: Poll) -> None: ...
