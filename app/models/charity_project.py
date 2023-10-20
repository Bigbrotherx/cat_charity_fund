from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.constants import MAX_NAME_LENGTH
from app.models.mixins import CharityMixin


class CharityProject(Base, CharityMixin):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
