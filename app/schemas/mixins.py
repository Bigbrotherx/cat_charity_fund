from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CharityDbMixin(BaseModel):
    id: int
    fully_invested: bool
    invested_amount: int
    close_date: Optional[datetime]
