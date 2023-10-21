from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CharityDbMixin(BaseModel):
    """
    Миксин наследуется от BaseModel,
    в ином случае поля миксина не учавствуют в pydantic схемме
    """

    id: int
    fully_invested: bool
    invested_amount: int
    close_date: Optional[datetime]
