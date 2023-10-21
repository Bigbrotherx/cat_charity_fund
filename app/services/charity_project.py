from app.models import CharityProject
from app.crud import charity_project_crud
from app.crud.validators import (
    check_project_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
)
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investing import InvestingRoutine
from app.services.base_handler import BaseHandler


class CharityProjectHandler(BaseHandler):

    CRUD = charity_project_crud

    async def create_charity_project(
        self, charity_project: CharityProjectCreate
    ) -> CharityProject:
        await check_project_name_duplicate(charity_project.name, self.session)
        new_charity_project = await super().create_object(charity_project)
        return new_charity_project

    async def delete_charity_project(self, project_id: int) -> CharityProject:
        charity_project = await check_project_before_delete(
            project_id, self.session
        )
        charity_project = await self.CRUD.remove(
            charity_project, self.session
        )
        return charity_project

    async def update_charity_project(
        self, project_id: int, project: CharityProjectUpdate
    ) -> CharityProject:
        charity_project = await check_project_before_update(
            project_id, self.session, project
        )
        charity_project = await self.CRUD.update(
            charity_project, project, self.session
        )
        investing_routine = InvestingRoutine(charity_project, self.session)
        charity_project = await investing_routine.dictribute_money()
        return charity_project
