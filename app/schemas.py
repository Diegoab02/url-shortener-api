from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original: HttpUrl

class URLResponse(BaseModel):
    code: str
    original: str
    short_url: str
    clicks: int
    created_at: datetime

    model_config = {"from_attributes": True}

class URLStats(BaseModel):
    code: str
    original: str
    clicks: int
    created_at: datetime

    model_config = {"from_attributes": True}