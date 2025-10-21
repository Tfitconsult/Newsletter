import os
import uuid
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DB_URL = os.getenv("DATABASE_URL") or (
    f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}?ssl=true"
)

engine = create_async_engine(DB_URL, pool_pre_ping=True, pool_size=5, max_overflow=5)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with SessionLocal() as session:
        yield session


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS notes (
  id CHAR(36) PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  source_url TEXT,
  raw_text MEDIUMTEXT NOT NULL,
  asset_url TEXT,
  status ENUM('inbox','selected','archived') DEFAULT 'inbox',
  tags JSON NULL,
  auto_category ENUM('policy','tech','experiences','tips') DEFAULT NULL,
  score FLOAT DEFAULT 0,
  ai_title VARCHAR(255),
  ai_blurb MEDIUMTEXT,
  INDEX notes_created_idx (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS issues (
  id CHAR(36) PRIMARY KEY,
  issue_date DATE NOT NULL,
  subject VARCHAR(255),
  preface MEDIUMTEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS issue_items (
  issue_id CHAR(36) NOT NULL,
  note_id CHAR(36) NOT NULL,
  position INT,
  PRIMARY KEY (issue_id, note_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


async def init_db():
    async with engine.begin() as conn:
        for stmt in SCHEMA_SQL.strip().split(";\n\n"):
            s = stmt.strip()
            if s:
                await conn.execute(text(s))


async def insert_note_db(
    session: AsyncSession, raw_text, source_url, cat, score, title, blurb, tags
):
    rid = str(uuid.uuid4())
    await session.execute(
        text(
            """INSERT INTO notes(id, raw_text, source_url, auto_category, score, ai_title, ai_blurb, tags)
                VALUES (:id,:raw_text,:source_url,:cat,:score,:title,:blurb,:tags)"""
        ),
        {
            "id": rid,
            "raw_text": raw_text,
            "source_url": source_url,
            "cat": cat,
            "score": score,
            "title": title,
            "blurb": blurb,
            "tags": json.dumps(tags) if tags else None,
        },
    )
    await session.commit()
    return rid


async def list_notes_db(session: AsyncSession, limit: int = 200):
    rs = await session.execute(
        text("SELECT * FROM notes ORDER BY created_at DESC LIMIT :lim"), {"lim": limit}
    )
    return [dict(r) for r in rs.mappings()]
