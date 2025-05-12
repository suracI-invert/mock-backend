from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic_ai import Agent

from api.routers import auth_router
from api.routers import lesson_router
from api.routers import user_router
from api.routers import exercise_router
from api.routers import resources_router
from api.routers import chat_router

from api.middlewares.cor_id import CorrelationIDMiddleware
from api.middlewares.trace import TraceMiddleware
from api.middlewares.metric import ConnectionCounterMiddleware

from domain.assistants.conversation_storage import InMemoryStorage

logfire.configure()

Agent.instrument_all()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.conversation_storage = InMemoryStorage()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(lesson_router)
app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(resources_router)
app.include_router(chat_router)

logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(TraceMiddleware)
app.add_middleware(ConnectionCounterMiddleware)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
