import asyncio
from api.classify import classify, propose_title_blurb
from api.service import get_session, init_db
from sqlalchemy import text


async def run():
    await init_db()
    async for session in get_session():
        rs = await session.execute(
            text(
                "SELECT id, raw_text FROM notes WHERE auto_category IS NULL OR ai_title IS NULL LIMIT 100"
            )
        )
        rows = list(rs.mappings())
        for r in rows:
            cat, score = classify(r["raw_text"])
            title, blurb = propose_title_blurb(r["raw_text"])
            await session.execute(
                text(
                    "UPDATE notes SET auto_category=:cat, score=:score, ai_title=:title, ai_blurb=:blurb WHERE id=:id"
                ),
                {"cat": cat, "score": score, "title": title, "blurb": blurb, "id": r["id"]},
            )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(run())
