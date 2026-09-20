from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pulse_api.infrastructure.config import settings
from pulse_api.infrastructure.logging import RequestLoggingMiddleware, configure_logging
from pulse_api.interface.v1.polls import router as polls_router

configure_logging()

app = FastAPI(title="Pulse API", version="0.1.0")

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(polls_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
