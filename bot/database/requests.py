from bot.database.models import async_session
from bot.database.models import User 
from sqlalchemy import select, update


async def set_user(tg_id: int, name: str, username: str, referrer: int):


    async with async_session() as session:
        user = await get_user_by_tg_id(tg_id)

        if not user:
            session.add(User(
                tg_id=tg_id, 
                name=name, 
                username=username, 
                score=1000, 
                referrals=list(),
                referrer=referrer
                ))
            await session.commit()


async def get_user_by_tg_id(user_tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        return user


async def get_top_100_users():
    async with async_session() as session:
        users = await session.scalars(select(User).order_by(User.score.desc()).limit(100))
        return [{"tg_id": user.tg_id, "name": user.name, "username": user.username, "score": user.score} for user in users]


async def update_user_score(user_id: int, new_score: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == user_id).values(score=new_score))
        await session.commit()


async def add_referral(user_id: int, referral_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if user:
            user.referrals.append(referral_id)
            await session.commit()