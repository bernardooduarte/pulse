from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from pulse_api.application.poll_service import PollNotFoundError, PollService
from pulse_api.domain.entities import DomainError, OptionNotFoundError, PollClosedError
from pulse_api.infrastructure.db.repository import SqlAlchemyPollRepository
from pulse_api.infrastructure.db.session import get_session
from pulse_api.interface.v1.schemas import CastVoteRequest, CreatePollRequest, PollResponse

router = APIRouter(prefix="/api/v1/polls", tags=["polls"])


async def get_poll_service(session: AsyncSession = Depends(get_session)) -> PollService:
    return PollService(SqlAlchemyPollRepository(session))


@router.post("", response_model=PollResponse, status_code=status.HTTP_201_CREATED)
async def create_poll(
    body: CreatePollRequest, service: PollService = Depends(get_poll_service)
) -> PollResponse:
    poll = await service.create_poll(question=body.question, options=body.options)
    return PollResponse.from_domain(poll)


@router.get("/{poll_id}", response_model=PollResponse)
async def get_poll(
    poll_id: UUID, service: PollService = Depends(get_poll_service)
) -> PollResponse:
    try:
        poll = await service.get_poll(poll_id)
    except PollNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return PollResponse.from_domain(poll)


@router.post("/{poll_id}/votes", response_model=PollResponse)
async def cast_vote(
    poll_id: UUID, body: CastVoteRequest, service: PollService = Depends(get_poll_service)
) -> PollResponse:
    try:
        poll = await service.cast_vote(poll_id, body.option_id)
    except PollNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PollClosedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except OptionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return PollResponse.from_domain(poll)
