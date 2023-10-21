from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.charity_project import CharityProjectHandler

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
    project_handler = CharityProjectHandler(session)
    all_projects = await project_handler.get_all_objects_from_db()
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
    project_handler = CharityProjectHandler(session)
    new_charity_project = await project_handler.create_charity_project(
        charity_project
    )
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
    project_handler = CharityProjectHandler(session)
    charity_project = await project_handler.delete_charity_project(project_id)
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
    project_handler = CharityProjectHandler(session)
    charity_project = await project_handler.update_charity_project(
        project_id, obj_in
    )
    return charity_project
