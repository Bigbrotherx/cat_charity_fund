from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):
    async def get_project_id_by_name(self, name: str, session: AsyncSession):
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CharityProjectCRUD(CharityProject)
