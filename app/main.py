from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from .routers import locations, categories, recomendations
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic_settings import SettingsConfigDict, BaseSettings
from .database import engine, Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


import os

load_dotenv()

class Settings(BaseSettings):
    allowed_origins: str
    allowed_methods: str
    allowed_headers: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
env_allowed_origins = settings.allowed_origins.split(",")
env_allowed_methods = settings.allowed_methods.split(",")
env_allowed_headers = settings.allowed_headers.split(",")

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=env_allowed_origins,
    allow_credentials=True,
    allow_methods=env_allowed_methods,
    allow_headers=env_allowed_headers,
)

app.include_router(locations.router)
app.include_router(categories.router)
app.include_router(recomendations.router)

@app.get("/")
def read_root():
    return {"Hello": "World FCP"}

@app.get("/check-db/")
def check_db():
    try:
        with engine.connect() as connection:
            return {"status": "Connected"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
