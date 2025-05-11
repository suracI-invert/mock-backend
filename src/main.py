import httpx

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.routers import auth_router
from api.routers import lesson_router
from api.routers import user_router
from api.routers import exercise_router
from api.routers import resources_router
from settings import get_settings

app = FastAPI()
app.include_router(auth_router)
app.include_router(lesson_router)
app.include_router(user_router)
app.include_router(exercise_router)
app.include_router(resources_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
