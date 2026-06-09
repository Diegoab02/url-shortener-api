from fastapi import FastAPI
from app.database import engine, Base
from app.routes.urls import router as urls_router
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="Acortador de URLs construido con FastAPI y PostgreSQL",
    version="1.0.0"
)

app.include_router(urls_router)

@app.get("/")
def root():
    return {"message": "URL Shortener API funcionando"}