from sqlalchemy import Column, Integer, Boolean, DateTime, func

from app.models.constants import DEFAULT_INVESTED


class CharityMixin:
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, server_default=func.now())
    close_date = Column(DateTime, nullable=True)
