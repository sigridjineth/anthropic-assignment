# Cross-Conversation Memory

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                │
│                           │                                 │
│           ┌───────────────┼───────────────┐                │
│           │               │               │                │
│           ▼               ▼               ▼                │
│    [Session 1]      [Session 2]     [Session 3]           │
│           │               │               │                │
│           └───────────────┴───────────────┘                │
│                           │                                 │
│                           ▼                                 │
│                    [Memory Store]                          │
│                           │                                 │
│           ┌───────────────┼───────────────┐                │
│           ▼               ▼               ▼                │
│      Preferences     Past Actions    Relationship          │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

## Memory Categories

### 1. User Preferences
Persistent across all sessions:
- Communication style
- Technical level
- Language preferences
- Accessibility needs

### 2. Interaction History
Key moments from past sessions:
- Topics discussed
- Decisions made
- Outstanding items
- Follow-up promises

### 3. Relationship Context
Business/personal context:
- Account tier
- Team size
- Industry
- Previous purchases

## API Integration

```python
# Start session with memory retrieval
memories = memory_client.retrieve(
    user_id=user.id,
    categories=["preferences", "recent_interactions"],
    limit=10
)

# Include in system prompt
system = f"""
## User Memory
{format_memories(memories)}

## Current Conversation
[new messages will appear here]
"""

# After session, store new memories
memory_client.store(
    user_id=user.id,
    memories=[
        {"category": "interaction", "content": "Discussed pricing concerns"},
        {"category": "preference", "content": "Prefers detailed explanations"}
    ]
)
```

## Privacy & Compliance

- Users can view all stored memories
- Users can delete specific memories or all data
- Memory retention policies (auto-expire after X days)
- GDPR-compliant data handling
