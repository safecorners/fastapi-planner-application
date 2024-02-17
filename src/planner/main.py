from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from planner.database.connection import conn
from planner.routes.events import event_router
from planner.routes.users import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
def on_startup() -> None:
    conn()


@app.get("/")
async def home() -> RedirectResponse:
    return RedirectResponse(url="/event/")