#!/usr/bin/env python3
"""
Claude Skills API Demo — Developer Walkthrough

This script shows the exact API calls for building a multi-agent system with Skills.
Run with: uv run python scripts/demo_skills_api.py

Flow: SKILL.md → Upload → Router (tool_choice) → Answerer (container.skills) → Postmortem
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

BETAS = ["code-execution-2025-08-25", "skills-2025-10-02"]
SKILLS_DIR = Path(__file__).parent.parent / "skills"

# ANSI colors
C = "\033[96m"   # Cyan
G = "\033[92m"   # Green
Y = "\033[93m"   # Yellow
M = "\033[95m"   # Magenta
B = "\033[1m"    # Bold
D = "\033[2m"    # Dim
R = "\033[0m"    # Reset


def pp(obj, title=None):
    """Pretty print JSON with optional title."""
    if title:
        print(f"\n{B}{C}{title}{R}")
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def section(num, title):
    print(f"\n{B}{G}{'─' * 60}{R}")
    print(f"{B}{G}[{num}] {title}{R}")
    print(f"{B}{G}{'─' * 60}{R}")


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL DEFINITIONS (this is what you copy)
# ═══════════════════════════════════════════════════════════════════════════════

ROUTER_TOOL = {
    "name": "route_skills",
    "description": "Decide which skills to attach based on user input",
    "input_schema": {
        "type": "object",
        "properties": {
            "needs_skill": {"type": "boolean"},
            "suggested_skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "required": ["domain", "confidence"]
                }
            },
            "trigger_reason": {"type": "string"}
        },
        "required": ["needs_skill", "suggested_skills", "trigger_reason"]
    }
}

POSTMORTEM_TOOL = {
    "name": "analyze_and_propose",
    "description": "Analyze conversation and propose skill updates",
    "input_schema": {
        "type": "object",
        "properties": {
            "new_pattern_detected": {"type": "boolean"},
            "pattern_name": {"type": "string"},
            "skill_update": {
                "type": "object",
                "properties": {
                    "target_skill": {"type": "string"},
                    "content_to_add": {"type": "string"}
                }
            }
        },
        "required": ["new_pattern_detected", "pattern_name"]
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN DEMO
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    client = anthropic.Anthropic()

    print(f"\n{B}{M}═══════════════════════════════════════════════════════════════{R}")
    print(f"{B}{M}  CLAUDE SKILLS API — DEVELOPER WALKTHROUGH{R}")
    print(f"{B}{M}═══════════════════════════════════════════════════════════════{R}")

    # ───────────────────────────────────────────────────────────────────────────
    section(1, "SKILL.md — Your knowledge as code")
    # ───────────────────────────────────────────────────────────────────────────

    skill_path = SKILLS_DIR / "cdp_memory" / "SKILL.md"
    skill_content = skill_path.read_text()

    print(f"\n{D}# File: skills/cdp_memory/SKILL.md{R}")
    print(f"{D}# YAML frontmatter + markdown body = one skill{R}\n")

    # Show first 20 lines
    for i, line in enumerate(skill_content.split("\n")[:20]):
        if line.startswith("---"):
            print(f"{M}{line}{R}")
        elif ":" in line and i < 5:
            print(f"{Y}{line}{R}")
        elif line.startswith("#"):
            print(f"{C}{line}{R}")
        else:
            print(line)
    print(f"{D}...{R}")

    # ───────────────────────────────────────────────────────────────────────────
    section(2, "skills.create() — Upload once, reuse forever")
    # ───────────────────────────────────────────────────────────────────────────

    print(f"\n{D}# Check if skill exists, create if not{R}")
    print(f"""
{Y}existing = client.beta.skills.list(source="custom", betas=BETAS){R}
{Y}skill = client.beta.skills.create({R}
{Y}    display_title="Memory Playbook",{R}
{Y}    files=[("memory_playbook/SKILL.md", content, "text/markdown")],{R}
{Y}    betas=BETAS{R}
{Y}){R}
""")

    # Actually do it
    existing_skills = client.beta.skills.list(source="custom", betas=BETAS)
    existing_map = {s.display_title: s for s in existing_skills.data}

    display_title = "Demo - Memory Playbook"
    if display_title in existing_map:
        skill = existing_map[display_title]
        print(f"{G}✓ Reusing: skill_id={skill.id}{R}")
    else:
        skill = client.beta.skills.create(
            display_title=display_title,
            files=[("memory-playbook/SKILL.md", skill_path.read_bytes(), "text/markdown")],
            betas=BETAS
        )
        print(f"{G}✓ Created: skill_id={skill.id}{R}")

    # ───────────────────────────────────────────────────────────────────────────
    section(3, "Router Agent — tool_choice forces structured JSON")
    # ───────────────────────────────────────────────────────────────────────────

    transcript = "Customer: We're a fintech startup. Users expect Claude to remember preferences across sessions, but we have strict compliance requirements."

    print(f"\n{D}# Input transcript{R}")
    print(f'"{transcript}"')

    print(f"\n{D}# Key: tool_choice forces the model to use this exact tool{R}")
    print(f"""
{Y}response = client.messages.create({R}
{Y}    model="claude-haiku-4-5-20251001",{R}
{Y}    tools=[ROUTER_TOOL],{R}
{Y}    {B}tool_choice={{"type": "tool", "name": "route_skills"}},{R}  {D}# ← Forces JSON{R}
{Y}    messages=[{{"role": "user", "content": transcript}}]{R}
{Y}){R}
""")

    # Actually call
    router_resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="Available skills: cdp_memory, cdp_context_editing, fintech_patterns, pricing_guidance",
        tools=[ROUTER_TOOL],
        tool_choice={"type": "tool", "name": "route_skills"},
        messages=[{"role": "user", "content": transcript}],
    )

    router_decision = None
    for block in router_resp.content:
        if block.type == "tool_use":
            router_decision = block.input

    pp(router_decision, "Router Decision (structured JSON):")

    # ───────────────────────────────────────────────────────────────────────────
    section(4, "Answer Agent — container.skills attaches knowledge")
    # ───────────────────────────────────────────────────────────────────────────

    skills_config = [{"type": "custom", "skill_id": skill.id, "version": "latest"}]

    print(f"\n{D}# Key: container.skills tells Claude which skills to load{R}")
    print(f"""
{Y}response = client.beta.messages.create({R}
{Y}    model="claude-sonnet-4-5-20250929",{R}
{Y}    betas=BETAS,{R}
{Y}    {B}container={{"skills": [{{"type": "custom", "skill_id": "{skill.id}", "version": "latest"}}]}},{R}
{Y}    messages=[...]{R}
{Y}){R}
""")

    # Actually call (code_execution tool required for skills beta)
    answer_resp = client.beta.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        betas=BETAS,
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        container={"skills": skills_config},
        messages=[{"role": "user", "content": f"{transcript}\n\nAnswer in 2-3 sentences."}]
    )

    answer_text = ""
    for block in answer_resp.content:
        if hasattr(block, "text"):
            answer_text = block.text

    print(f"\n{G}Answer (grounded in skill):{R}")
    print(answer_text[:600])

    # ───────────────────────────────────────────────────────────────────────────
    section(5, "Postmortem Agent — The Flywheel")
    # ───────────────────────────────────────────────────────────────────────────

    print(f"\n{D}# Analyze call, detect new patterns, propose skill updates{R}")
    print(f"""
{Y}response = client.messages.create({R}
{Y}    model="claude-haiku-4-5-20251001",{R}
{Y}    tools=[POSTMORTEM_TOOL],{R}
{Y}    tool_choice={{"type": "tool", "name": "analyze_and_propose"}},{R}
{Y}    messages=[{{"role": "user", "content": call_summary}}]{R}
{Y}){R}
""")

    postmortem_resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system="Analyze this fintech call. The customer mentioned compliance + memory. Propose a skill update if you detect a new pattern.",
        tools=[POSTMORTEM_TOOL],
        tool_choice={"type": "tool", "name": "analyze_and_propose"},
        messages=[{"role": "user", "content": f"Transcript: {transcript}\n\nAnswer given: {answer_text}"}],
    )

    postmortem_result = None
    for block in postmortem_resp.content:
        if block.type == "tool_use":
            postmortem_result = block.input

    pp(postmortem_result, "Postmortem Analysis:")

    print(f"\n{Y}→ New pattern detected. This becomes a PR.{R}")
    print(f"{Y}→ Approve it, and the next fintech call benefits.{R}")
    print(f"{Y}→ That's the flywheel.{R}")

    # ───────────────────────────────────────────────────────────────────────────
    section("✓", "Summary — The Pattern")
    # ───────────────────────────────────────────────────────────────────────────

    print(f"""
{B}1. SKILL.md{R}           → YAML frontmatter + markdown = plugin
{B}2. skills.create(){R}    → Upload once, get skill_id
{B}3. Router + tool_choice{R} → Structured JSON decision (no parsing)
{B}4. container.skills{R}   → Attach knowledge at runtime
{B}5. Postmortem{R}         → Detect patterns → propose updates → evolve

{C}Router DECIDES. Your code ATTACHES. Platform EXECUTES.{R}
{C}Postmortem LEARNS. Skills EVOLVE.{R}

{D}Copy this pattern: github.com/anthropics/interview-copilot-skills{R}
""")


if __name__ == "__main__":
    main()
