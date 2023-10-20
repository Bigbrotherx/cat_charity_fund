from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Donation
from app.crud import donation_crud
from app.schemas.donation import DonationBase
from app.services.investing import InvestingRoutine


class DonationHandler:
    def __init__(self, session: AsyncSession, user: User = None) -> None:
        self.session = session
        self.user = user

    async def get_all_donations(self) -> list[Donation]:
        all_donations = await donation_crud.get_multi(self.session)
        return all_donations

    async def get_user_donations(self) -> list[Donation]:
        user_donations = await donation_crud.get_user_donations(
            self.user, self.session
        )
        return user_donations

    async def create_donation(self, donation: DonationBase) -> Donation:
        new_donation = await donation_crud.create(
            donation, self.session, self.user
        )
        investing_routine = InvestingRoutine(new_donation, self.session)
        new_donation = await investing_routine.dictribute_money()
        return new_donation
