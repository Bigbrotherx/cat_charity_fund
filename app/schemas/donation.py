from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.mixins import CharityDbMixin
from app.schemas import constants


class DonationBase(BaseModel):
    full_amount: int = Field(gt=constants.AMOUNT_MIN_VAL)
    comment: Optional[str]
    create_date: datetime = Field(default_factory=datetime.now)


class DonationDBShort(DonationBase):
    id: int

    class Config:
        orm_mode = True


class DonationDBFull(DonationDBShort, CharityDbMixin):
    user_id: int
