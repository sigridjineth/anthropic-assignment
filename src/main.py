from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

from .api import router
from .services.session import session_store
from .services.skills import skill_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize skills on startup."""
    # Startup: Initialize skill manager (upload skills to Anthropic)
    print("Initializing skills via Anthropic Skills API...")
    try:
        await skill_manager.initialize()
        print(f"Skills initialized: {[d.value for d in skill_manager.available_domains]}")
    except Exception as e:
        print(f"Warning: Could not initialize skills: {e}")
        print("App will run without pre-uploaded skills (fallback mode)")

    yield

    # Shutdown: cleanup if needed
    print("Shutting down...")


app = FastAPI(title="Interview Copilot", version="0.1.0", lifespan=lifespan)

# Mount static files and templates
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Include API routes
app.include_router(router)


@app.get("/")
async def landing_page(request: Request):
    """Landing page for session preparation."""
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/session/{session_id}")
async def session_page(request: Request, session_id: str):
    """Session page for live copilot."""
    session = session_store.get(session_id)
    if not session:
        return RedirectResponse(url="/")

    # If session ended, redirect to summary
    if session.ended_at:
        return RedirectResponse(url=f"/session/{session_id}/summary")

    return templates.TemplateResponse(
        "session.html",
        {
            "request": request,
            "session_id": session_id,
            "company": session.company,
            "prep_result": session.prep_result,
        },
    )


@app.get("/session/{session_id}/summary")
async def summary_page(request: Request, session_id: str):
    """Post-call summary page."""
    session = session_store.get(session_id)
    if not session:
        return RedirectResponse(url="/")

    return templates.TemplateResponse(
        "summary.html",
        {
            "request": request,
            "session_id": session_id,
            "company": session.company,
            "post_call_result": session.post_call_result.model_dump() if session.post_call_result else None,
            "archive_path": session.archive_path,
        },
    )


@app.get("/skills")
async def skills_page(request: Request):
    """Skills management page - view company knowledge and interview learnings."""
    return templates.TemplateResponse("skills.html", {"request": request})


def run():
    """Run the application."""
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
