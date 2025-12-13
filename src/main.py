from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

from .api import router
from .services.session import session_store

app = FastAPI(title="Sales Copilot", version="0.1.0")

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

    return templates.TemplateResponse(
        "session.html",
        {
            "request": request,
            "session_id": session_id,
            "company": session.company,
            "prep_result": session.prep_result,
        },
    )


def run():
    """Run the application."""
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
