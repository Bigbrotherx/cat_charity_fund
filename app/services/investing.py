from typing import Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.crud.charity_project import CharityProjectCRUD
from app.crud.donation import DonationCRUD


class InvestingRoutine:
    """Класс распределения инвестиций"""

    def __init__(
        self,
        created_object: Union[CharityProject, Donation],
        session: AsyncSession,
    ) -> None:
        self.created_object = created_object
        self.session = session

    def __close_object(
        self, obj: Union[CharityProject, Donation]
    ) -> Union[CharityProject, Donation]:
        obj.fully_invested = True
        obj.close_date = datetime.now()
        obj.invested_amount = obj.full_amount
        return obj

    def __get_crud_for_related(
        self,
    ) -> Union[CharityProjectCRUD, DonationCRUD]:
        if isinstance(self.created_object, Donation):
            return CharityProjectCRUD(CharityProject)
        elif isinstance(self.created_object, CharityProject):
            return DonationCRUD(Donation)

    async def dictribute_money(self) -> Union[CharityProject, Donation]:
        crud = self.__get_crud_for_related()
        objects_to_change = await crud.get_not_invested_instances(self.session)
        for changing_object in objects_to_change:
            changing_object_free_amount = (
                changing_object.full_amount - changing_object.invested_amount
            )
            if self.created_object.full_amount > changing_object_free_amount:
                self.created_object.invested_amount += (
                    changing_object_free_amount
                )
                changing_object = self.__close_object(changing_object)
                self.session.add(changing_object)
            else:
                changing_object.invested_amount += (
                    self.created_object.full_amount
                )
                if (
                    changing_object.full_amount == changing_object.invested_amount
                ):
                    changing_object = self.__close_object(changing_object)
                    self.session.add(changing_object)
                self.created_object = self.__close_object(self.created_object)
                self.session.add(self.created_object)
                break

        await self.session.commit()
        await self.session.refresh(self.created_object)
        return self.created_object
