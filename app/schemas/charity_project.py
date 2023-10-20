from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, Extra

from app.schemas.mixins import CharityDbMixin


class CharityProjectUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    create_date: datetime = Field(default_factory=datetime.now)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(BaseModel):
    full_amount: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    create_date: datetime = Field(default_factory=datetime.now)


class CharityProjectDB(CharityProjectCreate, CharityDbMixin):
    class Config:
        orm_mode = True
