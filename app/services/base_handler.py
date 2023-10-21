from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import User, CharityProject, Donation
from app.crud.donation import DonationCRUD
from app.crud.charity_project import CharityProjectCRUD
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationBase
from app.services.investing import InvestingRoutine


class BaseHandler:

    CRUD: Union[CharityProjectCRUD, DonationCRUD] = None

    def __init__(self, session: AsyncSession, user: User = None) -> None:
        self.session = session
        self.user = user

    async def get_all_objects_from_db(self) -> list[Union[CharityProject, Donation]]:
        if self.CRUD is None:
            raise NotImplementedError("Определите константу CRUD в классе")
        all_projects = await self.CRUD.get_multi(self.session)
        return all_projects

    async def create_object(
        self, object_in: Union[CharityProjectCreate, DonationBase]
    ) -> Union[CharityProject, Donation]:
        if self.CRUD is None:
            raise NotImplementedError("Определите константу CRUD в классе")
        new_object = await self.CRUD.create(
            object_in, self.session
        )
        investing_routine = InvestingRoutine(new_object, self.session)
        new_object = await investing_routine.dictribute_money()
        return new_object
