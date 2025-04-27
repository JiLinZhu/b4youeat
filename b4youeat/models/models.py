from __future__ import annotations
import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column,
)

class Base(DeclarativeBase):
    pass

class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

    reviews: Mapped[list["Review"]] = relationship(back_populates="restaurant")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

    reviews: Mapped[list["Review"]] = relationship(back_populates="user")

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("restaurant_id", "user_id", name="user_review_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    visit_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

    restaurant: Mapped["Restaurant"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")
    images: Mapped[list["Image"]] = relationship(back_populates="review")

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=False)
    storage_path: Mapped[str] = mapped_column(String, nullable=False)

    review: Mapped["Review"] = relationship(back_populates="images")
