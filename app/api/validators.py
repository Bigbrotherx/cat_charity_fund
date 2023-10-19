from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return project


async def check_project_name_duplicate(
    name: str,
    session: AsyncSession,
):
    project_id = await charity_project_crud.get_project_id_by_name(
        name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def check_project_before_delete(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка проекта перед удалением"""
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    return project


async def check_project_if_close(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """
    Проверка не закрыт ли проект
    """
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )

    return project


async def check_project_before_update(
    project_id: int, session: AsyncSession, obj_in: CharityProjectUpdate
) -> CharityProject:
    """Прверка проекта перед обновлением"""
    project = await check_project_exists(project_id, session)
    if obj_in.name:
        await check_project_name_duplicate(obj_in.name, session)
    project = await check_project_if_close(project_id, session)
    if obj_in.full_amount:
        if project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=400,
                detail="Конечная сумма должна быть больше чем уже инвестированная",
            )

    return project
