from sqlalchemy import Column, Integer, Boolean, DateTime


class CharityMixin:
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime, nullable=True)
