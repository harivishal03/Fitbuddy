from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBuddy")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)