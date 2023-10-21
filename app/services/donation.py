from app.models import Donation
from app.crud import donation_crud
from app.services.base_handler import BaseHandler


class DonationHandler(BaseHandler):
    CRUD = donation_crud

    async def get_user_donations(self) -> list[Donation]:
        user_donations = await donation_crud.get_user_donations(
            self.user, self.session
        )
        return user_donations
