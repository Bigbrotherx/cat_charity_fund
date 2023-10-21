from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, Extra

from app.schemas.mixins import CharityDbMixin
from app.schemas import constants


class CharityProjectUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, gt=constants.AMOUNT_MIN_VAL)
    name: Optional[str] = Field(None, min_length=constants.STRING_MIN_LENGTH, max_length=constants.NAME_MAX_LENGTH)
    description: Optional[str] = Field(None, min_length=constants.STRING_MIN_LENGTH)
    create_date: datetime = Field(default_factory=datetime.now)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(BaseModel):
    full_amount: int = Field(gt=constants.AMOUNT_MIN_VAL)
    name: str = Field(min_length=constants.STRING_MIN_LENGTH, max_length=constants.NAME_MAX_LENGTH)
    description: str = Field(min_length=constants.STRING_MIN_LENGTH)
    create_date: datetime = Field(default_factory=datetime.now)


class CharityProjectDB(CharityDbMixin, CharityProjectCreate):
    class Config:
        orm_mode = True
