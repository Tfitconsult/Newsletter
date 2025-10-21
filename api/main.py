from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import date
from api.service import get_session, init_db, list_notes_db, insert_note_db
from api.classify import classify, propose_title_blurb
from api.renderer import render_issue

app = FastAPI(title="Newsletter API (multi-topic)")


@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/notes")
async def create_note(payload: dict, session=Depends(get_session)):
    text = (payload or {}).get("raw_text", "").strip()
    source_url = (payload or {}).get("source_url")
    tags = (payload or {}).get("tags")
    cat, score = classify(text)
    title, blurb = propose_title_blurb(text)
    rid = await insert_note_db(session, text, source_url, cat, score, title, blurb, tags)
    return {"id": rid, "category": cat, "score": score, "title": title}


@app.get("/notes")
async def list_notes(session=Depends(get_session)):
    rows = await list_notes_db(session)
    return rows


@app.post("/issues/compile")
async def compile_issue(payload: dict = None, session=Depends(get_session)):
    issue_date = (payload or {}).get("issue_date") or str(date.today())
    subject = (payload or {}).get("subject") or f"Weekly — {issue_date}"
    preface = (payload or {}).get("preface") or ""
    rows = await list_notes_db(session, limit=20)
    sections = {"policy": [], "tech": [], "experiences": [], "tips": []}
    for n in rows:
        cat = n.get("auto_category") or "tech"
        sections.setdefault(cat, []).append(
            {
                "title": n.get("ai_title"),
                "blurb": n.get("ai_blurb"),
                "source_url": n.get("source_url"),
            }
        )
    html, plaintext = render_issue(sections, subject, preface)
    return JSONResponse({"subject": subject, "html": html, "text": plaintext})
