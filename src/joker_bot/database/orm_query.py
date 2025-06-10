from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Joke, UserRating

########## АДМИНКА #################################

async def orm_add_joke(session: AsyncSession, data: dict):
    obj = Joke(
        name=data["name"],
        text=data["text"],
        rating=data["rating"]
    )
    session.add(obj)
    await session.commit()


async def orm_get_jokes(session: AsyncSession):
    query = select(Joke)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_joke(session: AsyncSession, joke_id: int):
    query = select(Joke).where(Joke.id == joke_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_random_joke(session: AsyncSession):
    query = select(Joke).order_by(func.random().limit(1))
    result = await session.execute(query)
    return result.scalar()


async def orm_update_joke(session: AsyncSession, joke_id: int, data):
    query = (
        update(Joke)
        .where(Joke.id == joke_id)
        .values(
            name=data["name"],
            text=data["text"],
            rating=data["rating"]
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_joke(session: AsyncSession, joke_id: int):
    query = delete(Joke).where(Joke.id == joke_id)
    await session.execute(query)
    await session.commit()


####### Рейтинг для анекдота ######################################


async def orm_rating_joke(
    session: AsyncSession, 
    user_id: int, 
    joke_id: int, 
    score: float
):
    query = select(UserRating).where(UserRating.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            UserRating(user_id=user_id, joke_id=joke_id, score=score)
        )

