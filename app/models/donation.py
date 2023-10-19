from sqlalchemy import Column, Integer, ForeignKey, Text

from app.core.db import Base
from app.models.mixins import CharityMixin


class Donation(Base, CharityMixin):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
