# Technical Sales Copilot

A production-grade AI copilot for Technical Sales teams, built with Claude.

## Features

- **Pre-call Preparation**: Generate session briefs, likely topics, and discovery questions
- **Live Call Assistance**: Real-time skill activation and answer suggestions
- **Dynamic Skills**: Architecture, Security, Roadmap, and Pricing knowledge bases
- **Clean White UI**: ChatGPT-inspired design

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

1. **Landing Page**: Enter customer details (company, industry, roles, purpose)
2. Click **Generate Session Brief** to get AI-powered preparation
3. Click **Start Session** to begin the live copilot
4. **Session Page**: Add transcript entries as the call progresses
5. Watch as the copilot activates skills and suggests answers
6. Use **Ask Copilot** to get direct answers

## Architecture

### 3-Agent System

1. **Prep Agent** (Landing) - Generates session briefs and recommendations
2. **Router Agent** (Session) - Decides which skills to activate
3. **Summarizer Agent** (Session) - Maintains live conversation summary
4. **Answerer Agent** (Session) - Generates answers using active skills

### Skills

- `roadmap` - Product timelines, feature availability
- `architecture` - System design, data flow, technical details
- `security` - Compliance, encryption, data handling
- `pricing` - Plans, costs, enterprise options

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/api/prep` | POST | Generate session brief |
| `/api/session` | POST | Create new session |
| `/session/{id}` | GET | Session page |
| `/api/session/{id}/transcript` | POST | Add transcript entry |
| `/api/session/{id}/ask` | POST | Ask copilot directly |
| `/api/session/{id}/state` | GET | Get session state |

## Development

```bash
# Run with auto-reload
make dev

# Run tests
make test

# Lint code
make lint

# Format code
make format
```

## License

MIT
