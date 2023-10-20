from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.services.donation import DonationHandler
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
    donation_handler = DonationHandler(session)
    all_donations = await donation_handler.get_all_donations()
    return all_donations


@router.get(
    "/my",
    response_model=list[DonationDBShort],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Вернуть список пожертвований пользователя, выполняющего запрос.
    """
    donation_handler = DonationHandler(session, user)
    user_donations = await donation_handler.get_user_donations()
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
    donation_handler = DonationHandler(session, user)
    new_donation = await donation_handler.create_donation(donation)
    return new_donation
