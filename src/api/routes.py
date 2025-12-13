from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import (
    TranscriptEntry,
    Speaker,
    AnswerDraft,
    RouterDecision,
    SummarizerState,
    SkillFiredEvent,
)
from ..services.orchestrator import Orchestrator
from ..services.transcript import TranscriptStore
from ..services.simulation import SimulationEngine

router = APIRouter()

# In-memory stores (demo)
sessions: dict[str, dict] = {}


class CreateSessionRequest(BaseModel):
    scenario_name: str | None = None


class CreateSessionResponse(BaseModel):
    session_id: str


class AddTranscriptRequest(BaseModel):
    offset_sec: float
    speaker: Speaker
    text: str


class AskRequest(BaseModel):
    question: str
    with_skills: bool = True


class CompareRequest(BaseModel):
    question: str


class CompareResponse(BaseModel):
    with_skills: AnswerDraft
    without_skills: AnswerDraft


class CopilotState(BaseModel):
    transcript: list[TranscriptEntry]
    router_decision: RouterDecision | None
    answer_draft: AnswerDraft | None
    active_skills: list[str]
    skill_fired_log: list[SkillFiredEvent] = []
    summarizer_state: SummarizerState | None = None


@router.post("/session", response_model=CreateSessionResponse)
async def create_session(req: CreateSessionRequest):
    import uuid
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        "transcript_store": TranscriptStore(),
        "orchestrator": Orchestrator(),
        "simulation": SimulationEngine(req.scenario_name) if req.scenario_name else None,
    }
    return CreateSessionResponse(session_id=session_id)


@router.post("/session/{session_id}/transcript")
async def add_transcript(session_id: str, req: AddTranscriptRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    entry = TranscriptEntry(
        offset_sec=req.offset_sec,
        speaker=req.speaker,
        text=req.text,
    )
    session["transcript_store"].add(entry)

    # Trigger routing
    orchestrator: Orchestrator = session["orchestrator"]
    await orchestrator.on_transcript_added(entry, session["transcript_store"])

    return {"status": "ok", "entry_id": entry.id}


@router.get("/session/{session_id}/state", response_model=CopilotState)
async def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    store: TranscriptStore = session["transcript_store"]
    orchestrator: Orchestrator = session["orchestrator"]

    return CopilotState(
        transcript=store.get_all(),
        router_decision=orchestrator.last_router_decision,
        answer_draft=orchestrator.last_answer,
        active_skills=orchestrator.active_skills,
        skill_fired_log=orchestrator.skill_fired_log,
        summarizer_state=orchestrator.summarizer_state,
    )


@router.get("/session/{session_id}/events", response_model=list[SkillFiredEvent])
async def get_events(session_id: str):
    """Get skill fired event log for the session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    orchestrator: Orchestrator = session["orchestrator"]
    return orchestrator.skill_fired_log


@router.post("/session/{session_id}/ask", response_model=AnswerDraft)
async def ask_copilot(session_id: str, req: AskRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    orchestrator: Orchestrator = session["orchestrator"]
    answer = await orchestrator.ask(
        question=req.question,
        transcript_store=session["transcript_store"],
        with_skills=req.with_skills,
    )
    return answer


@router.post("/session/{session_id}/compare", response_model=CompareResponse)
async def compare_with_without(session_id: str, req: CompareRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    orchestrator: Orchestrator = session["orchestrator"]

    with_skills = await orchestrator.ask(
        question=req.question,
        transcript_store=session["transcript_store"],
        with_skills=True,
    )
    without_skills = await orchestrator.ask(
        question=req.question,
        transcript_store=session["transcript_store"],
        with_skills=False,
    )

    return CompareResponse(with_skills=with_skills, without_skills=without_skills)


@router.post("/session/{session_id}/simulation/start")
async def start_simulation(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    if not session.get("simulation"):
        raise HTTPException(status_code=400, detail="No simulation loaded")

    simulation: SimulationEngine = session["simulation"]
    simulation.reset()
    return {"status": "ok", "total_entries": len(simulation.entries)}


@router.post("/session/{session_id}/simulation/step")
async def step_simulation(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    if not session.get("simulation"):
        raise HTTPException(status_code=400, detail="No simulation loaded")

    simulation: SimulationEngine = session["simulation"]
    entry = simulation.next_entry()

    if entry is None:
        return {"status": "done", "entry": None}

    # Add to transcript store
    session["transcript_store"].add(entry)

    # Trigger orchestrator
    orchestrator: Orchestrator = session["orchestrator"]
    await orchestrator.on_transcript_added(entry, session["transcript_store"])

    return {"status": "ok", "entry": entry.model_dump()}
