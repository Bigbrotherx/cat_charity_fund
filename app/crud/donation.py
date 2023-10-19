from sqlalchemy import select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import Donation, User


class DonationCRUD(CRUDBase):
    async def get_user_donations(self, user: User, session: AsyncSession):
        """Получить все донаты пользователя"""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        donations = donations.scalars().all()
        return donations


donation_crud = DonationCRUD(Donation)
