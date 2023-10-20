from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, CharityProject
from app.crud import charity_project_crud
from app.api.validators import (
    check_project_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
)
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investing import InvestingRoutine


class CharityProjectHandler:
    def __init__(self, session: AsyncSession, user: User = None) -> None:
        self.session = session
        self.user = user

    async def get_all_charity_projects(self) -> list[CharityProject]:
        all_projects = await charity_project_crud.get_multi(self.session)
        return all_projects

    async def create_charity_project(
        self, charity_project: CharityProjectCreate
    ) -> CharityProject:
        await check_project_name_duplicate(charity_project.name, self.session)
        new_charity_project = await charity_project_crud.create(
            charity_project, self.session
        )
        investing_routine = InvestingRoutine(new_charity_project, self.session)
        new_charity_project = await investing_routine.dictribute_money()
        return new_charity_project

    async def delete_charity_project(self, project_id: int) -> CharityProject:
        charity_project = await check_project_before_delete(
            project_id, self.session
        )
        charity_project = await charity_project_crud.remove(
            charity_project, self.session
        )
        return charity_project

    async def update_charity_project(
        self, project_id: int, project: CharityProjectUpdate
    ) -> CharityProject:
        charity_project = await check_project_before_update(
            project_id, self.session, project
        )
        charity_project = await charity_project_crud.update(
            charity_project, project, self.session
        )
        investing_routine = InvestingRoutine(charity_project, self.session)
        charity_project = await investing_routine.dictribute_money()
        return charity_project
