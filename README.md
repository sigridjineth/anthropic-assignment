# Technical Sales Interview Copilot

A demo application showcasing Claude's **Skills** feature for Technical Sales teams. This copilot observes sales call transcripts in real-time and dynamically invokes specialized Skills to provide accurate, context-aware answers.

## Demo Value

**"Without Skills vs With Skills"** - The demo shows how the same question gets better answers when Claude has access to organized, domain-specific knowledge through Skills.

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the application

```bash
uv run uvicorn src.main:app --reload
```

Then open http://localhost:8000 in your browser.

## Usage

1. Click **Start Session** to create a new session
2. Click **Play Demo** to start the simulated sales call transcript
3. Click **Next** to advance through the conversation
4. Watch the **Copilot panel** as it:
   - Detects when Skills are needed
   - Shows which Skills are active
   - Provides suggested answers with sources
5. Use **Ask Copilot** to ask questions directly
6. Toggle **Compare Mode** to see "Without Skills" vs "With Skills" side-by-side

## Architecture

### 3-Agent System

1. **Router Agent** - Analyzes transcript, decides which Skills are needed
2. **Summarizer Agent** - Maintains conversation context (P1)
3. **Answerer Agent** - Generates answers using selected Skills

### Skills (8 domains)

- `roadmap` - Product timelines, feature availability
- `architecture` - Technical implementation details
- `security` - Compliance, encryption, data handling
- `pricing` - Plans, costs, enterprise options
- `case_studies` - Customer success stories
- `competitive` - Positioning vs alternatives
- `integration` - SDKs, APIs, webhooks
- `deployment` - Cloud/on-prem options

## Project Structure

```
├── src/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── agents/              # Router, Answerer agents
│   ├── models/              # Pydantic models
│   ├── services/            # Orchestrator, TranscriptStore
│   ├── skills/              # SkillManager, Registry
│   └── api/                 # API routes
├── skills/                  # Skill packages (uploaded to Claude)
│   ├── roadmap/
│   ├── architecture/
│   ├── security/
│   └── pricing/
├── templates/               # HTML templates
├── static/                  # CSS, JS
└── scenarios/               # Demo transcript scenarios
```

## How Skills Work

This demo uses **prompt-based skill injection** - skill content is loaded from local markdown files and injected into the system prompt. This approach:

- Demonstrates the "curated knowledge" concept without requiring Skills API access
- Skills are stored in `skills/` directory as markdown files
- Each skill has a `SKILL.md` with instructions and `references/` for supporting docs
- The Router decides which skills to activate, then content is injected into the Answerer's prompt

## API Endpoints

- `POST /api/session` - Create new session
- `POST /api/session/{id}/transcript` - Add transcript entry
- `GET /api/session/{id}/state` - Get current copilot state
- `POST /api/session/{id}/ask` - Ask the copilot
- `POST /api/session/{id}/compare` - Compare with/without skills
- `POST /api/session/{id}/simulation/start` - Start demo playback
- `POST /api/session/{id}/simulation/step` - Step through demo

## License

MIT
