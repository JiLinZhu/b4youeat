"""
Parse Markdown reviews and seed the database.

Each *.md file must follow this shape (heading, metadata lines, then body):

    # Koba

    Rating: *****
    To Post: Yes

    The rest of the file is free-form review text …

• Heading (“# …”)  → restaurant name
• Rating line      → either stars (***** = 5) *or* an int (Rating: 4)
• To Post: Yes/No  → only “Yes” records are inserted (case-insensitive)
"""

import asyncio
import datetime
from pathlib import Path
from typing import Dict, Final, Union

from sqlalchemy import select
from db import async_session
from models.models import Review, Restaurant, User


SAMPLE_DIR: Final = Path(__file__).resolve().parent.parent.parent / "reviews"

def _parse_markdown(md_text: str) -> Dict[str, Union[str, int]]:
    """
    Return a dict ready for Review(**dict)  **or**  None (skip file).

    Expected fields in result:
        restaurant_name, rating, content
    """
    lines = [ln.rstrip() for ln in md_text.strip().splitlines() if ln.strip()]

    # Heading ─ first non-blank line must start with '# '
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Missing '# <Restaurant name>' heading")
    restaurant_name = lines[0][2:].strip()

    # Metadata lines (Rating:, To Post:)
    meta: dict[str, str] = {}
    body_start_idx = 0
    for i, ln in enumerate(lines[1:], start=1):
        if ":" in ln:  # still in metadata
            key, _, value = ln.partition(":")
            meta[key.lower().strip()] = value.strip()
        else:
            body_start_idx = i
            break

    # Parse rating (either stars or int)
    rating_raw = meta.get("rating", "")
    if rating_raw.strip("*").isdigit():
        rating = int(rating_raw.strip("*"))
    else:  # stars like '*****'
        rating = len(rating_raw.strip())
    rating = max(1, min(rating, 10))  # clamp 1-10 just in case

    # Body
    content = "\n".join(lines[body_start_idx:]).strip()

    return {
        "restaurant_name": restaurant_name,
        "rating": rating,
        "content": content,
    }


async def _get_or_create_restaurant(session, name: str) -> Restaurant:
    """Fetch a Restaurant by name or create it on the fly."""
    res = await session.execute(select(Restaurant).where(Restaurant.name == name))
    restaurant = res.scalar_one_or_none()
    if restaurant is None:
        restaurant = Restaurant(name=name)
        session.add(restaurant)
        await session.commit()
        await session.refresh(restaurant)
    return restaurant


async def _get_or_create_user(session) -> User:
    EMAIL = "jilin.zhu99@gmail.com"
    NAME = "Ji Lin"

    result = await session.execute(
        select(User).where(User.email == EMAIL)
    )
    user = result.scalar_one_or_none()
    if user is None:
        user = User(email=EMAIL, name=NAME)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def insert_markdown_reviews() -> None:
    md_files = sorted(SAMPLE_DIR.glob("*.md"))
    if not md_files:
        print(f"No reviews found in {SAMPLE_DIR}")
        return

    inserted, updated = 0, 0
    async with async_session() as session:
        user = await _get_or_create_user(session)
        for path in md_files:
            parsed = _parse_markdown(path.read_text(encoding="utf-8"))

            restaurant = await _get_or_create_restaurant(
                session, parsed["restaurant_name"]
            )

            stmt = select(Review).where(
                Review.user_id == user.id,
                Review.restaurant_id == restaurant.id,
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                existing.content = parsed["content"]
                existing.rating = parsed["rating"]
                updated += 1
            else:
                review = Review(
                    restaurant_id=restaurant.id,
                    user_id=user.id,
                    visit_date=datetime.datetime.now(datetime.timezone.utc),
                    content=parsed["content"],
                    rating=parsed["rating"],
                )
                session.add(review)
                inserted += 1

        await session.commit()
        print(
            f"{inserted} inserted, {updated} updated "
            f"for user {user.email} across {len(md_files)} markdown files."
        )


if __name__ == "__main__":
    asyncio.run(insert_markdown_reviews())
