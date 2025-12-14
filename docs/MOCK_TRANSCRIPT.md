# Mock Transcript for Demo

> **Use Case**: FinBot (Series B Fintech) · Head of Engineering · 6 months API user
>
> **Purpose**: Triggers `memory_playbook` skill attachment via Router

---

## Option A: 3-Turn Natural Build-up (Recommended)

Copy-paste these sequentially into the transcript input:

### Turn 1: Context Setting
```
We've been using Claude for about 6 months now for our customer support chatbot. It's handling around 2,000 conversations a day.
```

### Turn 2: Satisfaction + Transition
```
Really working well for single-session stuff. Our compliance team loves the audit trail.
```

### Turn 3: The Trigger (KEY MOMENT)
```
Here's our challenge though. Users have these long financial planning conversations. They come back the next day expecting Claude to remember what they discussed — like "remember that ETF portfolio you recommended?"

Is there a way to handle that kind of cross-session memory?
```

**Trigger phrases**:
- "come back the next day"
- "remember"
- "cross-session memory"

**Expected Router behavior**:
- Detected: cross-session topic
- Confidence: ~89%
- Action: attach `memory_playbook`

---

## Option B: Single Trigger (Quick Demo)

If you need a faster demo, use just this:

```
Our conversations get really long. And users come back the next day expecting Claude to remember what they said. Is there a way to handle that?
```

---

## Option C: With Customer Name (Sarah)

If using named customer for narration consistency:

### [Sarah - FinBot] Turn 1
```
We've been on the API for 6 months now. About 2,000 conversations daily.
```

### [Sarah - FinBot] Turn 2
```
Single-session stuff works great. Compliance team is happy with the audit trail.
```

### [Sarah - FinBot] Turn 3 (TRIGGER)
```
But here's the thing — users come back the next day expecting Claude to remember their conversation. "Remember that ETF recommendation?" they'll say.

How do we handle cross-session persistence?
```

---

## Demo Flow Checklist

1. [ ] Start session with "FinBot, fintech startup, Series B"
2. [ ] Session Ready modal shows: `context_editing_guide` + `fintech_patterns` attached
3. [ ] Paste Turn 1 → Watch copilot (no skill change yet)
4. [ ] Paste Turn 2 → Still no skill change
5. [ ] Paste Turn 3 → **KEY MOMENT**: Router attaches `memory_playbook`
6. [ ] Wait for Answer → Check SOURCES panel
7. [ ] End Call → Post-call shows interview archived + skill update proposal

---

## Post-Demo: Expected Skill Update Proposal

```markdown
### Memory + Compliance Pattern
For fintech: compliance-critical data should persist in Memory, not just summarized in Context Editing.

Rationale: FinBot conversation revealed that regulatory data requires cross-session persistence for audit purposes.
```

---

*Last updated: 2025-12-14*
