# Persistent Facts Pattern

## The Problem

In long conversations, important user statements get "lost" when truncating context:
- "Don't recommend oil stocks" (message 3) → forgotten by message 30
- User preferences mentioned early get overwritten
- Compliance violations from "forgotten" constraints

## The Solution: Persistent Facts Bucket

Extract compliance-critical and preference statements into a **persistent facts** section that NEVER gets summarized or truncated.

## Implementation

### 1. Identify Extractable Facts

**Constraint patterns**:
- "I don't want...", "Never recommend...", "Must have..."
- "My budget is...", "Deadline is..."
- "We can't use..." (compliance, legal)

**Preference patterns**:
- "I prefer...", "We like..."
- "Our priority is..."
- "The most important thing is..."

**Decision patterns**:
- "We've decided...", "Let's go with..."
- "Approved:", "Rejected:"

### 2. Extraction Prompt

```
Extract any user constraints, preferences, or decisions from this message.
Return as a list of facts in this format:
- [CONSTRAINT] description
- [PREFERENCE] description
- [DECISION] description

If no extractable facts, return empty list.
```

### 3. Storage Structure

```python
persistent_facts = {
    "constraints": [
        {"fact": "No fossil fuel investments", "source": "turn_3", "timestamp": "..."},
        {"fact": "Budget under $10,000/month", "source": "turn_7", "timestamp": "..."}
    ],
    "preferences": [
        {"fact": "Prefers conservative growth", "source": "turn_5", "timestamp": "..."}
    ],
    "decisions": [
        {"fact": "Will use Sonnet tier", "source": "turn_12", "timestamp": "..."}
    ]
}
```

### 4. Context Assembly

```python
system_prompt = f"""
## Persistent User Context
The following facts must ALWAYS be respected:

### Constraints (never violate these)
{format_constraints(persistent_facts["constraints"])}

### Preferences
{format_preferences(persistent_facts["preferences"])}

### Previous Decisions
{format_decisions(persistent_facts["decisions"])}

---
"""
```

## Fintech Example: Compliance Handling

**User says** (turn 3): "Just to be clear, don't invest in oil companies. We have an ESG policy."

**Extracted fact**:
```json
{
    "type": "constraint",
    "fact": "No oil company investments (ESG policy)",
    "compliance_critical": true,
    "source": "turn_3"
}
```

**Result**: Even at turn 50, Claude will never recommend Exxon.

## SOC2 Audit Note

This pattern was used by Acme Wealth to pass their SOC2 audit:
- All compliance-critical statements are logged
- Persistent facts have source attribution
- Audit trail shows when constraints were set
