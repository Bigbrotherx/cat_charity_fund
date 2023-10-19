from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.api.validators import (
    check_project_before_delete,
    check_project_before_update,
    check_project_name_duplicate,
)
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investing import InvestingRoutine

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех проектов.
    """
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[
        Depends(current_superuser),
    ],
    response_model_exclude_none=True,
)
async def create_charity_project(
    *,
    session: AsyncSession = Depends(get_async_session),
    charity_project: CharityProjectCreate,
):
    """
    Только для суперюзеров.
    Создаёт благотворительный проект.
    """
    await check_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    investing_routine = InvestingRoutine(new_charity_project, session)
    new_charity_project = await investing_routine()
    return new_charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[
        Depends(current_superuser),
    ],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.

    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    charity_project = await check_project_before_delete(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[
        Depends(current_superuser),
    ],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_project_before_update(
        project_id, session, obj_in
    )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    investing_routine = InvestingRoutine(charity_project, session)
    charity_project = await investing_routine()
    return charity_project
