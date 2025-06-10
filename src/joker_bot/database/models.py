from sqlalchemy import BigInteger, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    ...


class Joke(Base):
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float(precision=2), default=3.0)


class UserRating(Base):
    __tablename__ = "ratings"

    user_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    joke_id: Mapped[int] = mapped_column(ForeignKey("jokes.id"), primary_key=True)
    score: Mapped[int] = mapped_column(Integer)