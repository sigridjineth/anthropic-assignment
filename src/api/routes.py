from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import PrepInput, PrepResult, TranscriptEntry
from ..agents import PrepAgent
from ..services.session import session_store
from ..services.orchestrator import Orchestrator

router = APIRouter()
prep_agent = PrepAgent()
orchestrator = Orchestrator()


class CreateSessionRequest(BaseModel):
    raw_context: str | None = None
    prep_result: dict | None = None  # Pre-computed prep result from landing page


class TranscriptRequest(BaseModel):
    speaker: str
    text: str


class AskRequest(BaseModel):
    question: str


@router.post("/api/prep")
async def generate_prep(input_data: PrepInput):
    """Generate session preparation materials."""
    result = await prep_agent.prepare(input_data)
    return result.model_dump()


@router.post("/api/session")
async def create_session(request: CreateSessionRequest):
    """Create a new session."""
    # Use pre-computed prep result if available
    prep_result = None
    if request.prep_result:
        prep_result = PrepResult(**request.prep_result)

    # Infer company from prep result or raw context
    company = "Customer Session"
    if prep_result and prep_result.session_brief:
        # Extract company from brief (first sentence usually mentions it)
        company = prep_result.session_brief.split(".")[0][:50]
    elif request.raw_context:
        company = request.raw_context[:50]

    session = session_store.create(
        company=company,
        prep_result=prep_result,
    )

    return {
        "session_id": session.id,
        "company": session.company,
        "prep_result": prep_result.model_dump() if prep_result else None,
    }


@router.get("/api/session/{session_id}/state")
async def get_session_state(session_id: str):
    """Get the current session state."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.id,
        "company": session.company,
        "transcript": [
            {"speaker": e.speaker, "text": e.text, "timestamp": e.timestamp.isoformat()}
            for e in session.transcript
        ],
        "router_decision": session.router_decision.model_dump() if session.router_decision else None,
        "summarizer_state": session.summarizer_state.model_dump() if session.summarizer_state else None,
        "current_answer": session.current_answer.model_dump() if session.current_answer else None,
        "active_skills": session.active_skills,
        "recommended_skills": session.recommended_skills,
        "skill_fired_log": [
            {
                "timestamp": e.timestamp.isoformat(),
                "domains": e.domains,
                "trigger_reason": e.trigger_reason,
                "confidence": e.confidence,
                "detected_question": e.detected_question,
            }
            for e in session.skill_fired_log
        ],
    }


@router.post("/api/session/{session_id}/transcript")
async def add_transcript(session_id: str, request: TranscriptRequest):
    """Add a transcript entry and process through agents."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    entry = TranscriptEntry(speaker=request.speaker, text=request.text)
    session.transcript.append(entry)

    # Process through agent pipeline
    await orchestrator.process_transcript(session, entry)

    return await get_session_state(session_id)


@router.post("/api/session/{session_id}/ask")
async def ask_copilot(session_id: str, request: AskRequest):
    """Ask a direct question to the copilot."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answer = await orchestrator.ask_question(session, request.question)

    return {
        "answer": answer.model_dump(),
        "state": await get_session_state(session_id),
    }
