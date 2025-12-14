from datetime import datetime
from pathlib import Path
import httpx
import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import PrepInput, PrepResult, TranscriptEntry
from ..agents import PrepAgent, PostCallAgent
from ..services.session import session_store
from ..services.orchestrator import Orchestrator
from ..config import get_settings

router = APIRouter()

# Cache skill metadata
_skill_metadata_cache: dict | None = None


def get_skill_metadata() -> dict:
    """Load skill metadata (descriptions, types) from SKILL.md files."""
    global _skill_metadata_cache
    if _skill_metadata_cache is not None:
        return _skill_metadata_cache

    skills_dir = Path(__file__).parent.parent.parent / "skills"
    metadata = {}

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_id = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        skill_info = {
            "id": skill_id,
            "name": skill_id.replace("_", " ").title(),
            "description": "",
            "is_meta": skill_id.startswith("cdp_"),  # Meta skills are CDP platform skills
        }

        if skill_md.exists():
            content = skill_md.read_text()
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    try:
                        frontmatter = yaml.safe_load(content[3:end])
                        skill_info["name"] = frontmatter.get("name", skill_info["name"])
                        skill_info["description"] = frontmatter.get("description", "")
                    except Exception:
                        pass

        metadata[skill_id] = skill_info

    _skill_metadata_cache = metadata
    return metadata


prep_agent = PrepAgent()
postcall_agent = PostCallAgent()
orchestrator = Orchestrator()
settings = get_settings()


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

    # Get skill metadata for UI display
    skill_metadata = get_skill_metadata()

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
        "skill_metadata": skill_metadata,  # Include skill descriptions and types
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


@router.post("/api/session/{session_id}/end")
async def end_session(session_id: str):
    """End the session and generate post-call analysis."""
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.ended_at:
        # Already ended, return existing result
        return {
            "session_id": session_id,
            "post_call_result": session.post_call_result.model_dump() if session.post_call_result else None,
        }

    # Mark session as ended
    session.ended_at = datetime.now()

    # Generate post-call analysis
    if session.transcript:
        session.post_call_result = await postcall_agent.analyze(session)

        # Archive interview record to interview_records skill
        session.archive_path = await _archive_interview_record(session)

    return {
        "session_id": session_id,
        "post_call_result": session.post_call_result.model_dump() if session.post_call_result else None,
        "interview_archived": session.archive_path is not None,
        "archive_path": session.archive_path,
    }


async def _archive_interview_record(session) -> str | None:
    """Archive the complete interview record to interview_records skill."""
    from pathlib import Path

    if not session.transcript or not session.post_call_result:
        return None

    # Get skills directory
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    learnings_dir = skills_dir / "interview_records" / "learnings"
    learnings_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    company_slug = session.company.lower().replace(" ", "_")[:30] if session.company else "unknown"

    # Find unique filename
    base_name = f"{date_str}_{company_slug}"
    target_file = learnings_dir / f"{base_name}.md"
    counter = 1
    while target_file.exists():
        target_file = learnings_dir / f"{base_name}_{counter}.md"
        counter += 1

    # Build interview record content
    pcr = session.post_call_result

    # Format transcript
    transcript_lines = []
    for entry in session.transcript:
        speaker = entry.speaker.capitalize()
        transcript_lines.append(f"[{speaker}] {entry.text}")
    transcript_text = "\n\n".join(transcript_lines)

    # Format skills activated
    skills_text = ""
    if session.skill_fired_log:
        skills_lines = []
        for event in session.skill_fired_log:
            skills_lines.append(f"- {', '.join(event.domains)}: {event.trigger_reason}")
        skills_text = "\n".join(skills_lines)
    else:
        skills_text = "No skills activated"

    # Format pain points
    pain_points_text = "\n".join(f"- {p}" for p in pcr.customer_pain_points) if pcr.customer_pain_points else "None identified"

    # Format requirements
    requirements_text = "\n".join(f"- {r}" for r in pcr.customer_requirements) if pcr.customer_requirements else "None identified"

    # Format follow-up actions
    followup_text = "\n".join(f"- {a}" for a in pcr.follow_up_actions) if pcr.follow_up_actions else "None"

    # Format topics as YAML list
    topics_yaml = "\n".join(f"  - {t}" for t in pcr.topics_covered) if pcr.topics_covered else "  - general"

    # Format skills used as YAML list
    skills_used_yaml = "\n".join(f"  - {s}" for s in session.active_skills) if session.active_skills else "  - none"

    # Build the complete record
    content = f"""---
type: interview_record
company: {session.company or 'Unknown'}
date: {datetime.now().isoformat()}
duration_turns: {len(session.transcript)}
outcome: {pcr.outcome}
topics:
{topics_yaml}
skills_used:
{skills_used_yaml}
---

# Interview: {session.company or 'Unknown'}

## Summary

{pcr.call_summary}

## Outcome

{pcr.outcome}

## Pain Points

{pain_points_text}

## Requirements

{requirements_text}

## Transcript

{transcript_text}

## Skills Activated

{skills_text}

## Follow-up Actions

{followup_text}
"""

    # Write the file
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Return relative path for display
    return f"interview_records/learnings/{target_file.name}"


@router.get("/api/stt/token")
async def get_stt_token():
    """Get a single-use token for ElevenLabs realtime STT."""
    if not settings.elevenlabs_api_key:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs API key not configured. Set ELEVENLABS_API_KEY in .env"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.elevenlabs.io/v1/single-use-token/realtime_scribe",
            headers={"xi-api-key": settings.elevenlabs_api_key},
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get STT token: {response.text}"
            )

        data = response.json()
        return {"token": data.get("token")}


class SkillUpdateRequest(BaseModel):
    skill_id: str
    file_path: str
    update_type: str
    content: str
    company: str | None = None  # Optional: call company for metadata


@router.post("/api/skills/update")
async def apply_skill_update(request: SkillUpdateRequest):
    """Apply a skill update proposal - saves to learnings/ subdirectory."""
    from pathlib import Path

    # Map skill_id to directory
    skills_dir = Path(__file__).parent.parent.parent / "skills"
    skill_dir = skills_dir / request.skill_id

    if not skill_dir.exists():
        raise HTTPException(status_code=404, detail=f"Skill directory not found: {request.skill_id}")

    # Create learnings directory
    learnings_dir = skill_dir / "learnings"
    learnings_dir.mkdir(exist_ok=True)

    # Generate filename with date and optional company
    date_str = datetime.now().strftime("%Y-%m-%d")
    company_slug = ""
    if request.company:
        # Sanitize company name for filename
        company_slug = "_" + request.company.lower().replace(" ", "_")[:30]

    # Find unique filename
    base_name = f"{date_str}{company_slug}"
    target_file = learnings_dir / f"{base_name}.md"
    counter = 1
    while target_file.exists():
        target_file = learnings_dir / f"{base_name}_{counter}.md"
        counter += 1

    # Write learning with metadata
    learning_content = f"""---
type: {request.update_type}
skill: {request.skill_id}
source_file: {request.file_path}
date: {datetime.now().isoformat()}
company: {request.company or 'Unknown'}
---

# {request.update_type.replace('_', ' ').title()}

{request.content}
"""

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(learning_content)

    return {
        "success": True,
        "message": f"Saved learning to {request.skill_id}/learnings/{target_file.name}",
        "file_path": str(target_file)
    }


def get_git_info(repo_path):
    """Get Git status for the repository."""
    import subprocess

    git_info = {
        "branch": None,
        "last_commit": None,
        "last_commit_date": None,
        "has_changes": False,
        "remote_url": None,
    }

    try:
        # Get current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path, capture_output=True, text=True
        )
        if result.returncode == 0:
            git_info["branch"] = result.stdout.strip()

        # Get last commit info
        result = subprocess.run(
            ["git", "log", "-1", "--format=%h|%s|%ci"],
            cwd=repo_path, capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split("|")
            if len(parts) >= 3:
                git_info["last_commit"] = f"{parts[0]}: {parts[1][:50]}"
                git_info["last_commit_date"] = parts[2]

        # Check for uncommitted changes in skills/
        result = subprocess.run(
            ["git", "status", "--porcelain", "skills/"],
            cwd=repo_path, capture_output=True, text=True
        )
        if result.returncode == 0:
            git_info["has_changes"] = bool(result.stdout.strip())

        # Get remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path, capture_output=True, text=True
        )
        if result.returncode == 0:
            git_info["remote_url"] = result.stdout.strip()

    except Exception:
        pass

    return git_info


@router.get("/api/skills")
async def list_skills():
    """List all skills with their knowledge and learnings."""
    from pathlib import Path
    import yaml

    skills_dir = Path(__file__).parent.parent.parent / "skills"
    repo_root = Path(__file__).parent.parent.parent
    result = []

    # Get Git info for the repository
    git_info = get_git_info(repo_root)

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_id = skill_dir.name
        skill_data = {
            "id": skill_id,
            "name": skill_id.replace("_", " ").title(),
            "knowledge": [],  # 전사 지식
            "learnings": [],  # 인터뷰 학습
        }

        # Load SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()
            # Parse frontmatter
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    try:
                        frontmatter = yaml.safe_load(content[3:end])
                        skill_data["name"] = frontmatter.get("name", skill_id)
                        skill_data["description"] = frontmatter.get("description", "")
                    except:
                        pass
            skill_data["knowledge"].append({
                "file": "SKILL.md",
                "type": "main",
            })

        # Load references (전사 지식)
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            for ref_file in refs_dir.glob("*.md"):
                skill_data["knowledge"].append({
                    "file": f"references/{ref_file.name}",
                    "type": "reference",
                })

        # Load learnings (인터뷰 학습)
        learnings_dir = skill_dir / "learnings"
        if learnings_dir.exists():
            for learning_file in sorted(learnings_dir.glob("*.md"), reverse=True):
                content = learning_file.read_text()
                learning_meta = {
                    "file": f"learnings/{learning_file.name}",
                    "type": "learning",
                }
                # Parse frontmatter for metadata
                if content.startswith("---"):
                    end = content.find("---", 3)
                    if end != -1:
                        try:
                            meta = yaml.safe_load(content[3:end])
                            learning_meta["date"] = meta.get("date", "")
                            learning_meta["company"] = meta.get("company", "")
                            learning_meta["update_type"] = meta.get("type", "")
                        except:
                            pass
                skill_data["learnings"].append(learning_meta)

        result.append(skill_data)

    return {"skills": result, "git": git_info}
