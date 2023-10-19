from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.services.investing import InvestingRoutine
from app.schemas.donation import DonationDBFull, DonationDBShort, DonationBase

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBFull],
    dependencies=[
        Depends(current_superuser),
    ],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Возвращает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    "/my",
    response_model=list[DonationDBShort],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Вернуть список пожертвований пользователя, выполняющего запрос.
    """
    user_donations = await donation_crud.get_user_donations(user, session)
    return user_donations


@router.post(
    "/", response_model=DonationDBShort, response_model_exclude_none=True
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Сделать пожертвование
    """
    new_donation = await donation_crud.create(donation, session, user)
    investing_routine = InvestingRoutine(new_donation, session)
    new_donation = await investing_routine()
    return new_donation
