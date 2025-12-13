# Context Editing Strategies

## Strategy 1: Rolling Summarization

**Best for**: General chat applications, customer support

```
Window Structure:
├── Recent (5 turns): Full verbatim text
├── Mid-range (10 turns): Summarized to ~20% of original
└── Persistent: Extracted key facts
```

**Implementation**:
- After every 5 turns, summarize the oldest batch
- Use Claude to generate summaries
- Keep summaries in a separate "context summary" section

## Strategy 2: Fact-First Extraction

**Best for**: Fintech, healthcare, compliance-heavy apps

```
Window Structure:
├── Recent (3 turns): Full verbatim
├── Facts bucket: All extracted constraints/preferences
└── Summary: Compressed conversation overview
```

**Key facts to extract**:
- User preferences ("I don't want X")
- Constraints ("Must be under $1000")
- Decisions made ("We agreed on Y")
- Compliance-critical statements

## Strategy 3: Topic-Based Segmentation

**Best for**: Technical support, complex multi-topic conversations

```
Window Structure:
├── Current topic: Full context
├── Previous topics: One-line summaries
└── Cross-topic facts: Persistent
```

## Token Savings Benchmarks

| Conversation Length | Without CE | With CE | Savings |
|---------------------|-----------|---------|---------|
| 10 turns | 4,000 tokens | 2,800 tokens | 30% |
| 20 turns | 10,000 tokens | 4,500 tokens | 55% |
| 50 turns | 25,000 tokens | 7,500 tokens | 70% |

## API Pattern

```python
# Before calling Claude, manage context
managed_context = context_manager.prepare(
    recent_turns=conversation[-5:],
    summary=summarize_turns(conversation[5:-5]),
    facts=extract_facts(conversation)
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=managed_context.to_messages()
)
```
