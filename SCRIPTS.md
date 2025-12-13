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

### 화면 4 (1:05-1:15): Session UI

```
┌─────────────────────────────┬───────────────────────────────────────┐
│                             │                                       │
│  💬 TRANSCRIPT              │  🤖 COPILOT                           │
│                             │                                       │
│  [Starting...]              │  📦 Skills                            │
│                             │  ✅ architecture (attached)           │
│                             │  ✅ security (attached)               │
│                             │  ○  roadmap (ready)                   │
│                             │                                       │
│                             │  ⚡ Skill Activity                    │
│                             │  (waiting...)                         │
│                             │                                       │
└─────────────────────────────┴───────────────────────────────────────┘
```

**내레이션**:
> "Two skills pre-attached. Roadmap ready if needed."

---

### 화면 5 (1:15-1:45): 첫 번째 질문 — 애매한 표현 → 맥락 유추

```
┌─────────────────────────────┬───────────────────────────────────────┐
│                             │                                       │
│  💬 TRANSCRIPT              │  🤖 COPILOT                           │
│                             │                                       │
│  [00:15] Customer:          │  🧠 Context Analysis                  │
│  "So, um... I'm curious     │  ───────────────────────────────────  │
│  about the... you know,     │  • "technical part" + "data flows"    │
│  the technical part.        │  • Role: Head of Engineering          │
│  Like how the data          │                                       │
│  actually flows through     │  🎯 Intent: Architecture question     │
│  your system?"              │                                       │
│                             │  ⚡ Using: architecture (pre-attached)│
│  █████████████████████      │                                       │
│                             │  💡 Suggested Answer                  │
│                             │  ───────────────────────────────────  │
│                             │  "3-stage pipeline:                   │
│                             │   1. Ingestion — real-time streams    │
│                             │   2. Transform — schema mapping       │
│                             │   3. Sync — exactly-once delivery     │
│                             │   P99: <100ms"                        │
│                             │                                       │
│                             │  📄 Source: architecture/dataflow.md  │
└─────────────────────────────┴───────────────────────────────────────┘
```

**내레이션**:
> "Customer says: 'I'm curious about the technical part, like how the data flows.'
> 
> Not a clean question. But the agent infers: architecture question.
> Uses the **pre-attached** architecture skill. Answer ready, source cited."

*[세일즈 역할]*:
> "Our pipeline is three stages — ingestion, transform, sync. P99 under 100 milliseconds."

---

### 화면 6 (1:45-2:10): 두 번째 질문 — 로드맵 (동적 attach)

```
┌─────────────────────────────┬───────────────────────────────────────┐
│                             │                                       │
│  💬 TRANSCRIPT              │  🤖 COPILOT                           │
│                             │                                       │
│  [00:45] Customer:          │  🧠 Context Analysis                  │
│  "Got it. And when is       │  ───────────────────────────────────  │
│  the new streaming          │  • "when shipping" = timeline Q       │
│  feature shipping?          │  • Needs roadmap info                 │
│  We need it for Q2."        │                                       │
│                             │  ⚡ ATTACHING: roadmap                │
│  █████████████████████      │  ───────────────────────────────────  │
│                             │  Reason: Timeline question detected   │
│                             │                                       │
│                             │  📦 Skills (updated)                  │
│                             │  ✅ architecture                      │
│                             │  ✅ security                          │
│                             │  ✅ roadmap ← just attached           │
│                             │                                       │
│                             │  💡 Suggested Answer                  │
│                             │  ───────────────────────────────────  │
│                             │  "Streaming: beta now, GA late Q1.    │
│                             │   ⚠️ Dates subject to change.         │
│                             │   Can connect you with PM."           │
│                             │                                       │
│                             │  📄 Source: roadmap/streaming.md      │
│                             │  ⚠️ Policy: Forward-looking caveat    │
└─────────────────────────────┴───────────────────────────────────────┘
```

**내레이션**:
> "Customer asks: 'When is the streaming feature shipping?'
> 
> Watch — the agent **dynamically attaches** the roadmap skill. It wasn't loaded before, now it is.
> 
> And the answer includes the **policy-safe caveat**: 'dates subject to change.' That's built into the playbook."

*[세일즈 역할]*:
> "Streaming is in beta, GA targeted for late Q1. Dates can shift — I can connect you with our PM for details."

---

### 화면 7 (2:10-2:35): 세 번째 질문 — 숨겨진 우려

```
┌─────────────────────────────┬───────────────────────────────────────┐
│                             │                                       │
│  💬 TRANSCRIPT              │  🤖 COPILOT                           │
│                             │                                       │
│  [01:30] Customer:          │  🧠 Context Analysis                  │
│  "That's helpful. Um...     │  ───────────────────────────────────  │
│  [pause]                    │  • "compliance" + pause               │
│  So compliance is kind of   │  • Fintech + flagged on-prem          │
│  a big deal for us."        │  • Pattern: 85% ask on-prem next      │
│                             │                                       │
│  █████████████████████      │  🎯 Inferred: On-prem concern         │
│                             │                                       │
│                             │  ⚡ Using: security (pre-attached)    │
│                             │         + roadmap (for on-prem ETA)   │
│                             │                                       │
│                             │  💡 Suggested Answer                  │
│                             │  ───────────────────────────────────  │
│                             │  "We're SOC2 Type II certified.       │
│                             │   Hybrid arch: your data in your VPC. │
│                             │   Full on-prem: Q2 roadmap."          │
│                             │                                       │
│                             │  💡 Proactive: Address before asked   │
└─────────────────────────────┴───────────────────────────────────────┘
```

**내레이션**:
> "Customer mentions compliance, pauses. The agent connects patterns — compliance plus hesitation, plus what I flagged earlier.
> 
> It uses **both** security and roadmap skills to answer proactively."

*[세일즈 역할]*:
> "We're SOC2 Type II certified. For data residency — hybrid architecture, your sensitive data stays in your VPC. Full on-prem is Q2."

*[Customer]*:
> "Oh, that's exactly what I was going to ask."

**내레이션**:
> "Answered before they asked. That's context-aware playbook activation."

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
