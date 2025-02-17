from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.models import db_helper
from views import router as api_router


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(router=api_router)


@app.get("/")
def read_root():
    if settings.run.domain:
        return {"Welcome to": f"https://{settings.run.domain}/docs"}
    if settings.run.debug:
        return {"Welcome to": f"http://localhost:{settings.run.port}/docs"}
    if settings.run.https:
        if settings.run.port == 443:
            return {"Welcome to": f"https://{settings.run.host}/docs"}
        else:
            return {"Welcome to": f"https://{settings.run.host}:{settings.run.port}/docs"}
    else:
        return {"Welcome to": f"http://{settings.run.host}:{settings.run.port}/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=settings.run.reload)
