"""Provider-side contract verification.

The frontend owns a consumer test (apps/web/src/features/polls/__tests__/
poll-api.pact.test.ts) that records the requests/responses it expects from
this API into pacts/pulse-web-pulse-api.json. This test replays those
interactions against a live instance of the real FastAPI app and fails the
build the moment the API drifts from what the frontend relies on - without
either side needing to run the other's code.

The consumer's "a poll exists" provider state is satisfied here by writing
the exact poll the pact expects directly into the same database the running
API is pointed at, via `state_handler`.
"""
from __future__ import annotations

import asyncio
import os
import uuid
from pathlib import Path

import pytest
from pact import Verifier
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from pulse_api.infrastructure.db.models import PollModel, PollOptionModel
from pulse_api.infrastructure.db.session import make_engine

PACT_FILE = Path(__file__).parents[4] / "pacts" / "pulse-web-pulse-api.json"
PROVIDER_HOST = os.environ.get("PACT_PROVIDER_HOST", "localhost")
PROVIDER_PORT = int(os.environ.get("PACT_PROVIDER_PORT", "8000"))
POLL_ID = uuid.UUID("9c858901-8a57-4791-81fe-4c455b099bc9")


def _seed_poll_exists(**_: object) -> None:
    async def seed() -> None:
        engine = make_engine()
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            # Idempotent: this state may be set up more than once across runs.
            await session.execute(delete(PollOptionModel).where(PollOptionModel.poll_id == POLL_ID))
            await session.execute(delete(PollModel).where(PollModel.id == POLL_ID))
            session.add(
                PollModel(
                    id=POLL_ID,
                    question="Tabs or spaces?",
                    is_closed=False,
                    options=[
                        PollOptionModel(id=uuid.uuid4(), poll_id=POLL_ID, label="Tabs", votes=0),
                        PollOptionModel(id=uuid.uuid4(), poll_id=POLL_ID, label="Spaces", votes=0),
                    ],
                )
            )
            await session.commit()
        await engine.dispose()

    asyncio.run(seed())


@pytest.mark.skipif(
    not PACT_FILE.exists(),
    reason="Run `pnpm --filter @pulse/web pact:consumer` first to generate the contract file.",
)
def test_api_honours_the_web_consumer_contract() -> None:
    (
        Verifier("pulse-api", PROVIDER_HOST)
        .add_transport(protocol="http", port=PROVIDER_PORT)
        .add_source(PACT_FILE)
        .state_handler({"a poll exists": _seed_poll_exists})
        .verify()
    )
