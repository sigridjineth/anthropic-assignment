# Claude Skills Use Case: Technical Sales Copilot — 5분 데모 스크립트 (Final v2)

---

## 타임라인

| 시간 | 섹션 | 내용 |
|------|------|------|
| 0:00-0:35 | **Hook + Skills 개념** | 사일로 문제 → Skills = curated playbooks |
| 0:35-1:05 | **Landing** | Session Brief + 일부 Skills 미리 attach |
| 1:05-2:35 | **Live Session** | 3개 질문 시연 (맥락 유추 + 동적 Skill attach) |
| 2:35-2:55 | **Post-call** | 10초 — Call note + 업데이트 제안 |
| 2:55-4:25 | **How to Build + Architecture** | 코드 + 3-Agent 구조 통합 |
| 4:25-5:00 | **Takeaway** | 핵심 메시지 |

---

## [0:00-0:35] Hook + Skills 개념

### 화면 1 (0:00-0:15): Hook

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   You're on a sales call.                                           │
│                                                                     │
│   Customer: "When is that feature shipping?"                        │
│   You: "Um... let me get back to you on that."                      │
│                                                                     │
│   The information EXISTS — in Eng docs, Product roadmaps.           │
│   It just doesn't FLOW to where it's needed.                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "You're on a sales call. Customer asks: 'When is that feature shipping?'
> 
> You don't know. The information exists — in engineering docs, product roadmaps.
> It just doesn't flow to where it's needed."

---

### 화면 2 (0:15-0:35): Skills = Curated Playbooks

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Claude Skills                                                     │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   📦 Curated, Versioned Playbooks                                   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  skills/                                                    │   │
│   │  ├─ architecture/   ← Eng team maintains                    │   │
│   │  ├─ roadmap/        ← Product team maintains                │   │
│   │  └─ security/       ← Compliance team maintains             │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│   Agent attaches the right playbook at the right time               │
│   → Verified, policy-safe knowledge flows to the field              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "Claude Skills lets you package org knowledge as **curated, versioned playbooks**.
> 
> Your agent attaches the right playbook at the right time — verified, policy-safe knowledge that flows to the field.
> 
> Let me show you."

---

## [0:35-1:05] Landing — Session Brief

### 화면 3 (0:35-1:05): Session Ready (결과 중심)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Session Ready: Acme Payments                                      │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   📋 Brief                                                          │
│   ───────────────────────────────────────────────────────────────   │
│   Fintech (Series B) • Head of Engineering • Technical Discovery    │
│   Flagged: On-premise, Compliance                                   │
│                                                                     │
│   🔮 Likely Topics                                                  │
│   ───────────────────────────────────────────────────────────────   │
│   1. System architecture (90%)                                      │
│   2. On-premise options (85%)                                       │
│   3. Security certifications (80%)                                  │
│                                                                     │
│   📦 Skills                                                         │
│   ───────────────────────────────────────────────────────────────   │
│   ✅ architecture   (pre-attached — likely needed)                  │
│   ✅ security       (pre-attached — flagged topic)                  │
│   ○  roadmap        (recommended — attach if needed)                │
│   ○  case_studies   (available)                                     │
│                                                                     │
│   [Enter Session →]                                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "I've set up a session for Acme Payments — fintech, Head of Engineering.
> 
> The copilot generates a brief: likely topics based on the profile and what I flagged.
> 
> And here's the key: **some skills are pre-attached** — architecture and security, because they're highly likely.
> 
> Roadmap is **recommended but not attached yet**. The agent will attach it dynamically if the conversation goes there.
> 
> Let's enter."

---

## [1:05-2:35] Live Session — 3개 질문

# Live Session 페르소나 구체화: Anthropic DevRel 세일즈

---

## 페르소나 설정

### 인터뷰어 (You): Anthropic DevRel

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   👤 You: Anthropic Developer Relations                             │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   Role: Developer Relations IC                                      │
│   Mission: Help developers build better with Claude                 │
│                                                                     │
│   Today's call:                                                     │
│   • Technical discovery with potential enterprise customer          │
│   • They're evaluating Claude for their AI product                  │
│   • Need to understand their use case, recommend CDP features       │
│                                                                     │
│   Your tools:                                                       │
│   • Skills: CDP feature docs, pricing, case studies, best practices │
│   • Goal: Match their problem to the right platform feature         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 인터뷰이 (Customer): FinBot의 Head of Engineering

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   🏢 Customer: FinBot                                               │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   Company: FinBot (Series B fintech startup)                        │
│   Product: AI-powered financial advisor chatbot                     │
│   Users: 50K+ retail investors                                      │
│                                                                     │
│   Attendee: Sarah Chen, Head of Engineering                         │
│   Background: Ex-Stripe, 8 years building payment systems           │
│                                                                     │
│   Current situation:                                                │
│   • Using Claude API for 6 months                                   │
│   • Chatbot handles portfolio questions, market analysis            │
│   • Conversations get LONG (users ask follow-ups for 20+ turns)     │
│                                                                     │
│   Pain points:                                                      │
│   • Token costs exploding as conversations grow                     │
│   • Context window filling up, losing early context                 │
│   • "Claude forgets what we discussed 10 messages ago"              │
│   • Tried naive truncation → bad user experience                    │
│                                                                     │
│   What she's looking for:                                           │
│   • Better way to manage long conversations                         │
│   • Keep costs reasonable                                           │
│   • Maintain conversation quality                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Skills 구성 (DevRel용)

```
skills-registry.json (Anthropic DevRel)
┌─────────────────────────────────────────────────────────────────────┐
│  {                                                                  │
│    "skills": [                                                      │
│      {                                                              │
│        "id": "cdp_context_editing",                                 │
│        "name": "Context Editing",                                   │
│        "owner": "platform-docs",                                    │
│        "description": "Managing context window, token optimization" │
│      },                                                             │
│      {                                                              │
│        "id": "cdp_memory",                                          │
│        "name": "Memory",                                            │
│        "owner": "platform-docs",                                    │
│        "description": "Persistent memory across conversations"      │
│      },                                                             │
│      {                                                              │
│        "id": "cdp_skills",                                          │
│        "name": "Skills",                                            │
│        "owner": "platform-docs",                                    │
│        "description": "Custom knowledge packages for agents"        │
│      },                                                             │
│      {                                                              │
│        "id": "fintech_patterns",                                    │
│        "name": "Fintech Customer Patterns",                         │
│        "owner": "devrel-learnings",                                 │
│        "description": "Common fintech use cases, objections, wins"  │
│      },                                                             │
│      {                                                              │
│        "id": "pricing_guidance",                                    │
│        "name": "Pricing & Tiers",                                   │
│        "owner": "sales-enablement",                                 │
│        "description": "Token pricing, tier recommendations"         │
│      }                                                              │
│    ]                                                                │
│  }                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 대화 시나리오 (상세)

### 화면: Session Ready

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Session Ready: FinBot                                             │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   📋 Brief                                                          │
│   Fintech (Series B) • Head of Engineering • Technical Discovery    │
│   Current Claude user (6 months) • Scaling issues                   │
│                                                                     │
│   🔮 Likely Topics                                                  │
│   1. Context window management (95%) ← flagged: "long conversations"│
│   2. Token cost optimization (90%)                                  │
│   3. Memory / state persistence (75%)                               │
│                                                                     │
│   📦 Skills                                                         │
│   ✅ cdp_context_editing   (pre-attached — likely needed)           │
│   ✅ fintech_patterns      (pre-attached — fintech customer)        │
│   ○  cdp_memory            (ready if needed)                        │
│   ○  pricing_guidance      (ready if needed)                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 질문 1: 애매한 문제 설명 → 맥락 유추

**Transcript:**
```
[00:30] Sarah (Customer):
"So yeah, we've been using Claude for about six months now, and it's 
been great for the most part. But we're running into this... thing.

Like, our users have these really long conversations — they'll ask 
about their portfolio, then follow up with market questions, then 
circle back to something they asked earlier.

And Claude just... kind of loses track? Like, by message 15, it's 
forgotten what we talked about in message 3. And we're burning 
through tokens like crazy.

We tried just cutting off the old messages but then users complain 
that 'the AI doesn't remember anything.' [laughs nervously]

I don't know, is there a... better way to handle this?"
```

**Copilot 분석:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  🧠 Context Analysis                                                │
│  ───────────────────────────────────────────────────────────────    │
│                                                                     │
│  Signals detected:                                                  │
│  • "long conversations" + "loses track" + "message 15"              │
│  • "burning through tokens"                                         │
│  • "tried cutting off old messages" = naive truncation              │
│  • "doesn't remember anything" = user experience issue              │
│                                                                     │
│  🎯 Inferred problem:                                               │
│  Context window management + token optimization                     │
│  Current approach (truncation) not working                          │
│                                                                     │
│  ⚡ Using: cdp_context_editing (pre-attached)                       │
│                                                                     │
│  💡 Suggested Response                                              │
│  ───────────────────────────────────────────────────────────────    │
│                                                                     │
│  "This is exactly what Context Editing is designed for.             │
│                                                                     │
│   Instead of naive truncation, you can:                             │
│   1. Summarize older turns (keep meaning, reduce tokens)            │
│   2. Extract key facts to preserve (portfolio preferences, etc.)    │
│   3. Dynamically manage what stays in context                       │
│                                                                     │
│   Pattern we've seen with fintech:                                  │
│   • Keep last 5 turns verbatim                                      │
│   • Summarize turns 6-15                                            │
│   • Extract persistent facts (risk tolerance, holdings)             │
│   → 60-70% token reduction, better continuity"                      │
│                                                                     │
│  📄 Sources:                                                        │
│  • cdp_context_editing/strategies.md                                │
│  • fintech_patterns/long_conversation_handling.md                   │
│                                                                     │
│  💡 Follow-up to ask:                                               │
│  "What's your average conversation length in turns?"                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**DevRel 응답:**
> "Ah, this is a really common challenge — actually, we just shipped something specifically for this.
> 
> It's called **Context Editing**. Instead of just cutting off old messages, you can intelligently manage what stays in the context window.
> 
> So for your case: keep the last 5 turns verbatim, summarize turns 6 through 15, and extract key facts — like the user's risk tolerance or what stocks they mentioned — as persistent context.
> 
> We've seen fintech companies get 60-70% token reduction without losing conversation quality.
> 
> Quick question: what's your average conversation length? Like, how many turns typically?"

---

### 질문 2: 구체적 기술 질문 + 숨겨진 우려

**Transcript:**
```
[02:00] Sarah:
"Oh wow, that's interesting. So it's like... programmable summarization?

Average is probably 15-20 turns, but power users go way longer.
Like 40, 50 messages.

[pause]

Um, one thing though — we're in fintech, so there's compliance stuff.
Like, we can't just... lose information? If a user said 'don't invest 
in oil companies' in message 3, and we summarize that away, and then 
Claude recommends Exxon in message 30... that's a problem.

[nervous laugh]

Our compliance team would kill me."
```

**Copilot 분석:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  🧠 Context Analysis                                                │
│  ───────────────────────────────────────────────────────────────    │
│                                                                     │
│  Signals:                                                           │
│  • "programmable summarization" = understanding the feature         │
│  • "40, 50 messages" = heavy usage, token costs significant         │
│  • [pause] + "compliance stuff" + "can't lose information"          │
│  • "compliance team would kill me" = real blocker                   │
│                                                                     │
│  ⚠️ Pattern matched! (fintech_patterns)                             │
│  "Compliance concern + data loss fear"                              │
│  85% of fintech customers raise this                                │
│                                                                     │
│  🎯 Hidden concern:                                                 │
│  Not just token cost — compliance risk of losing user preferences   │
│                                                                     │
│  ⚡ Using:                                                          │
│  • cdp_context_editing (attached)                                   │
│  • fintech_patterns (compliance handling)                           │
│                                                                     │
│  💡 Suggested Response                                              │
│  ───────────────────────────────────────────────────────────────    │
│                                                                     │
│  "This is the exact concern we hear from every fintech customer.    │
│   Here's how Context Editing handles it:                            │
│                                                                     │
│   You define what MUST be preserved — 'user constraints' bucket:    │
│   • 'no oil companies' → extracted, never summarized away           │
│   • Risk tolerance, restricted securities, preferences              │
│                                                                     │
│   These go into a 'persistent facts' section that always stays.     │
│   Only the conversational fluff gets summarized.                    │
│                                                                     │
│   Pattern from similar fintech (Acme Wealth):                       │
│   • They tag compliance-critical statements                         │
│   • Those get extracted to persistent context automatically         │
│   • Passed their SOC2 audit with this approach"                     │
│                                                                     │
│  📄 Sources:                                                        │
│  • cdp_context_editing/persistent_facts.md                          │
│  • fintech_patterns/compliance_handling.md                          │
│  • case_studies/acme_wealth.md                                      │
│                                                                     │
│  💡 Proactive: Address compliance before she asks directly          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**DevRel 응답:**
> "This is the exact concern we hear from every fintech customer. You're not alone.
> 
> Here's how Context Editing handles it: you define what **must** be preserved. We call it the 'persistent facts' bucket.
> 
> So 'don't invest in oil companies' — that gets **extracted**, not summarized. It stays in context permanently until the user changes it. Risk tolerance, restricted securities, any compliance-critical preferences — same thing.
> 
> Only the conversational parts get compressed. 'How was your weekend?' — that can be summarized. 'Never recommend fossil fuels' — that's sacred.
> 
> Actually, we have another fintech customer — Acme Wealth — who implemented exactly this pattern. They tag compliance-critical statements, extract them automatically, and they **passed their SOC2 audit** with this approach.
> 
> Would it help if I connected you with their engineering lead?"

---

### 질문 3 (Optional): 직접 Ask Copilot

**DevRel types in Ask Copilot:**
```
"What's the token cost comparison for a 50-turn conversation 
with vs without context editing?"
```

**Copilot Response:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  💡 Token Cost Comparison                                           │
│  ───────────────────────────────────────────────────────────────    │
│                                                                     │
│  50-turn conversation (avg 200 tokens/turn):                        │
│                                                                     │
│  WITHOUT Context Editing:                                           │
│  • Turn 50 context: ~10,000 tokens (full history)                   │
│  • Total API calls: ~250,000 tokens (cumulative)                    │
│  • Estimated cost: $7.50 (at Sonnet pricing)                        │
│                                                                     │
│  WITH Context Editing:                                              │
│  • Turn 50 context: ~3,000 tokens (summarized + persistent)         │
│  • Total API calls: ~85,000 tokens                                  │
│  • Estimated cost: $2.55                                            │
│  • Savings: ~66%                                                    │
│                                                                     │
│  ⚠️ Note: Actual savings vary by conversation type.                 │
│  Financial conversations with many numbers may compress less.       │
│                                                                     │
│  📄 Source: pricing_guidance/context_editing_roi.md                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**DevRel:**
> "Just pulled the numbers. For a 50-turn conversation, you're looking at roughly 66% token savings. That's $7.50 down to $2.55 per conversation at Sonnet pricing.
> 
> For 50,000 monthly active users with, let's say, 10 conversations each — that's real money."

---

## Post-call: META-SKILL 학습

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   META-SKILL: Suggested Updates                                     │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   📝 Update 1: fintech_patterns/compliance_handling.md              │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  + "Compliance concern always comes with nervous laugh"     │   │
│   │  + Phrase "compliance team would kill me" = serious blocker │   │
│   │  + Lead with SOC2 audit success story (Acme Wealth)         │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   [Review] [Approve]                                                │
│                                                                     │
│   📝 Update 2: cdp_context_editing/use_cases.md                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  + Fintech: 40-50 turn conversations common for power users │   │
│   │  + Key requirement: compliance-critical fact preservation   │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   [Review] [Approve]                                                │
│                                                                     │
│   📝 Signal to Product: cdp_memory                                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Customer showed interest in cross-conversation persistence │   │
│   │  "What if user comes back tomorrow?"                        │   │
│   │  → Memory feature may be natural upsell                     │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   [Flag to Product]                                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## [2:35-2:55] Post-call (10초)

### 화면 8: Call Note + 업데이트 제안

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Post-call                                                         │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   📋 Call Note (auto-generated)                                     │
│   Topics: Architecture ✓, Roadmap ✓, Compliance ✓                   │
│   Outcome: Deep-dive scheduled                                      │
│                                                                     │
│   🔄 Suggested Skill Update                                         │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  patterns/fintech.md                                        │   │
│   │  + "compliance + pause" → on-prem concern (NEW pattern)     │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   [Review] [Approve] [Dismiss]                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "Call ends. Auto-generated note. And a **suggested skill update** — new pattern detected.
> 
> Human reviews, approves or dismisses. The playbook evolves."

---

## [2:55-4:25] How to Build + Architecture (통합)

### 화면 9 (2:55-3:25): Skill 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Building Skills: File Structure                                   │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   skills/                                                           │
│   ├── architecture/                                                 │
│   │   ├── SKILL.md           ← Entry point (name, description)     │
│   │   ├── dataflow.md        ← Technical content                   │
│   │   └── faq.md                                                   │
│   │                                                                 │
│   ├── roadmap/                                                      │
│   │   ├── SKILL.md                                                 │
│   │   ├── streaming.md       ← Feature timelines                   │
│   │   └── policy.md          ← "Dates subject to change" template  │
│   │                                                                 │
│   └── security/                                                     │
│       ├── SKILL.md                                                 │
│       ├── compliance.md      ← SOC2, GDPR, etc.                    │
│       └── onprem.md          ← Hybrid architecture details         │
│                                                                     │
│   Each skill = curated knowledge + policy guidelines                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "How do you build this?
> 
> Each skill is a folder. SKILL.md is the entry point — name and description.
> Inside: your curated content plus policy guidelines.
> 
> Roadmap skill includes a policy template: 'dates subject to change.' That caveat comes from here."

---

### 화면 10 (3:25-3:55): API — Pre-attach + Dynamic attach

```python
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   API: Attaching Skills                                             │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   # Session start: pre-attach likely skills                         │
│   response = client.messages.create(                                │
│       model="claude-sonnet-4-5-20250514",                           │
│       container={                                                   │
│           "skills": [                                               │
│               {"type": "custom", "skill_id": "skill_arch_xxx"},     │
│               {"type": "custom", "skill_id": "skill_security_xxx"}, │
│           ]                                                         │
│       },                                                            │
│       messages=[{"role": "user", "content": transcript}]            │
│   )                                                                 │
│                                                                     │
│   # Mid-session: Router decides to attach roadmap                   │
│   container["skills"].append(                                       │
│       {"type": "custom", "skill_id": "skill_roadmap_xxx"}           │
│   )                                                                 │
│                                                                     │
│   Progressive disclosure: Claude loads skill files only as needed   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "At the API level: you attach skills via `container.skills`.
> 
> At session start, you **pre-attach** the likely ones — architecture, security.
> 
> Mid-session, when the Router detects a roadmap question, it **dynamically adds** the roadmap skill.
> 
> Claude uses **progressive disclosure** — loads skill files only as needed, not everything upfront."

---

### 화면 11 (3:55-4:25): 3-Agent 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Architecture: 3-Agent System                                      │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                                                             │   │
│   │   📝 SUMMARIZER                                             │   │
│   │   • Tracks conversation state                               │   │
│   │   • Extracts customer needs, predicts questions             │   │
│   │                                                             │   │
│   │              ↓                                              │   │
│   │                                                             │   │
│   │   🔍 ROUTER                                                 │   │
│   │   • Analyzes transcript context (not keywords)              │   │
│   │   • Decides: which skill to attach NOW?                     │   │
│   │   • Pre-attach (session start) vs Dynamic (mid-call)        │   │
│   │                                                             │   │
│   │              ↓                                              │   │
│   │                                                             │   │
│   │   💡 ANSWERER                                               │   │
│   │   • Calls Claude with attached skills                       │   │
│   │   • Returns: answer + source + confidence + caveats         │   │
│   │                                                             │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│   Skills attached dynamically based on conversation flow            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "The system uses three agents.
> 
> **Summarizer** tracks conversation state.
> 
> **Router** analyzes context — not keywords — and decides which skill to attach. It handles both pre-attachment at session start and dynamic attachment mid-call.
> 
> **Answerer** calls Claude with the attached skills, returns answers with sources and caveats.
> 
> Skills flow in based on conversation — that's the key architectural pattern."

---

### 화면 12 (4:10-4:25): Skills vs RAG (간단히)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Skills vs RAG                                                     │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   RAG:    Retrieval                                                 │
│   Skills: Retrieval + Policy + Procedures + Version Control         │
│                                                                     │
│   RAG returns doc chunks.                                           │
│   Skills return verified, policy-safe answers.                      │
│                                                                     │
│   (You can use RAG inside a skill — they're complementary)          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "Quick comparison: RAG is retrieval. Skills are retrieval **plus** policy, procedures, and version control.
> 
> They're complementary — you can use RAG inside a skill if needed."

---

## [4:25-5:00] Takeaway

### 화면 13: 마무리

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Building with Claude Skills                                       │
│   ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│   1. 📦 Package org knowledge as versioned playbooks                │
│      skills/roadmap/SKILL.md + content + policy                     │
│                                                                     │
│   2. 🔍 Route intelligently                                         │
│      Pre-attach likely skills, dynamic attach as needed             │
│                                                                     │
│   3. ✅ Get verified answers                                        │
│      Sources cited, caveats included, policy-safe                   │
│                                                                     │
│   4. 🔄 Evolve with human review                                    │
│      Suggested updates → approve → version bump                     │
│                                                                     │
│   ─────────────────────────────────────────────────────────────     │
│                                                                     │
│   container.skills → right knowledge, right time, right way         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**내레이션**:
> "To build this yourself:
> 
> **One** — Package your org knowledge as versioned playbooks. Content plus policy.
> 
> **Two** — Route intelligently. Pre-attach likely skills, dynamically attach as the conversation flows.
> 
> **Three** — Get verified answers. Sources cited, caveats built in.
> 
> **Four** — Evolve with human review. The playbooks get better over time.
> 
> `container.skills` — right knowledge, right time, right way.
> 
> That's Claude Skills.
> 
> Thanks for watching."

---

## 요약: 변경 사항

| 항목 | 이전 | 최종 |
|------|------|------|
| **Skills attach 방식** | "추천만, 세션 중 attach" | **Pre-attach (likely) + Dynamic attach (as needed)** |
| **Post-call** | 35초 | **20초로 축소** |
| **How to Build** | 별도 없음 | **Architecture와 통합 (코드 포함)** |
| **코드 스니펫** | 없음 | **Skill 구조 + API 호출 예시** |
| **총 시간 배분** | 설명 heavy | **데모 + 빌드 방법 균형** |

---
