from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from nanoid import generate
from app.database import get_db
from app.models import URL
from app.schemas import URLCreate, URLResponse, URLStats
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

router = APIRouter(prefix="/urls", tags=["URLs"])


def generate_unique_code(db: Session) -> str:
    while True:
        code = generate(size=6)
        exists = db.query(URL).filter(URL.code == code).first()
        if not exists:
            return code


@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    code = generate_unique_code(db)

    new_url = URL(
        code=code,
        original=str(payload.original)
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return URLResponse(
        code=new_url.code,
        original=new_url.original,
        short_url=f"{BASE_URL}/{new_url.code}",
        clicks=new_url.clicks,
        created_at=new_url.created_at
    )


@router.get("/stats/{code}", response_model=URLStats)
def get_stats(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.code == code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL no encontrada")

    return url

@router.get("/", response_model=list[URLResponse])
def list_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).order_by(URL.created_at.desc()).all()

    return [
        URLResponse(
            code=url.code,
            original=url.original,
            short_url=f"{BASE_URL}/{url.code}",
            clicks=url.clicks,
            created_at=url.created_at
        )
        for url in urls
    ]


@router.delete("/{code}", status_code=204)
def delete_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.code == code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL no encontrada")

    db.delete(url)
    db.commit()

@router.get("/{code}", status_code=302)
def redirect_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.code == code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL no encontrada")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url=url.original)