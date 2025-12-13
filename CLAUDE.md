# Important
- Don't use mock. This is real, production-grade app. **IMPORTANT**
- Read https://platform.claude.com/docs/en/home for each implementation.
- Use the latest features like Skills, Context Editing, Memory and etc.
- Implement Plan correctly.
- I love minimality. Write the code if and only if they are needed. otherwise, consider removing it or simplifying it.
- Write in Python using `uv` package manager.

# Plan

---

# PLAN vNext — Technical Sales Copilot w/ Claude Skills

## 1) 목표와 원칙

### 목표

* Technical Sales 콜에서 **조직 정보가 흐르지 않아** 즉답을 못하는 문제를,

  * **Skills로 "검증된 지식/표현/절차(playbook)를 배포 단위로 패키징"**하고
  * 대화 흐름을 관찰하다가 **필요할 때만 Skill을 발동(attach)**해서 해결하는 데모 완성
* "에이전트다운 에이전트"를 보여주기 위해 **Observe → Decide → Act** 구조를 분명히 드러낸다.

### 핵심 메시지(용어/톤)

* "Single Point of Truth" 단정 표현 대신:

  * **"Curated, versioned playbooks"**
  * **"A single interface to verified org knowledge"**
  * **"Knowledge that flows to the field"**
* "Skills = consolidate + inject" 프레이밍 유지:

  * 조직의 지식(eng/product/sales)을 **패키징**
  * 콜 중에는 **관련된 것만 주입(inject)**

### 비교 프레이밍(공정성)

* "RAG를 깎아내리기" 금지.
* 대신 역할 분담으로 설명:

  * RAG: retrieval/breadth
  * Skills: correctness/policy/consistency + procedures
  * "RAG inside a Skill" 가능성은 확장 포인트로 언급 가능(선택)

---

## 2) 범위/스코프 업데이트

### P0 (반드시 구현)

1. **3-Agent 아키텍처**

   * Router(의도/트리거 감지 → skill 선택)
   * Summarizer(상황 요약/중요 포인트/예측 질문)
   * Answerer(선택된 skills attach → 답변/근거/후속 질문)
2. **Dynamic Skill Activation UI 시각화**

   * "⚡ Skill Fired: roadmap / architecture / security"
   * "Why: trigger evidence"
   * "Active Skills" 목록(Attached vs Recommended 구분)
3. **Ask Copilot 입력창**

   * 사용자가 직접 타이핑한 질문 → Answerer 실행
4. **데모 안정성**

   * 시뮬레이션 transcript(프리셋) 기반
   * API 실패 시 mock replay/fallback
   * JSON 파싱 실패 대비: Raw JSON 보기 + 최소 렌더 fallback
5. **Without/With Skills 비교**

   * 동일 모델/프롬프트/포맷/툴
   * **container.skills만 차이** (공정성 강조)

### P1 (있으면 강력)

* Summarizer에서:

  * Key Moments(중요 발언 + 이유)
  * Predicted Questions(확률 + 도메인)
  * Suggested Asks(세일즈가 물어볼 discovery 질문)

### P2 (시간 남으면)

* TTS(추천 질문/답변 읽기)
* Diff View(Without vs With 결과 차이 하이라이트)
* STT(실시간 음성 인식 → Transcript 변환, Web Speech API 또는 Whisper)

---

## 3) Skills 패키징 계획(내용/구조)

### Skills 구성(최소 3개)

* `roadmap` skill

  * ETA/상태/조건부 표현 가이드("변경 가능성 caveat 자동 포함")
  * 안전한 답변 템플릿 + "확실/불확실" 구분
* `architecture` skill

  * "how it works" 설명 템플릿(고수준 3단계/데이터 플로우)
  * 성능/제약/전제조건(예: latency는 케이스별)
* `security` skill

  * SOC2/암호화/데이터 보관/레지던시/온프레미스 질문 대응 템플릿
* (선택) `case_studies` / `competitive` / `pricing`

### Skill 내부 설계 원칙

* "언제 이 Skill을 쓰는지" 트리거를 **SKILL.md에 명시**
* 출력은 UI에 바로 넣을 수 있도록 구조화(AnswerDraft 스키마)
* 숫자/벤치마크 등 "검증 불가한 구체값"은:

  * 데모용이면 "example/illustrative"로 명시하거나
  * "공유 가능한 범위의 문구"로 완화(오버클레임 방지)

---

## 4) META-SKILL 계획(리스크 조정 버전)

### 변경 사항(중요)

* "회의 끝나면 Skill 파일이 자동 업데이트" **오버클레임 위험**
* 따라서 META-SKILL은 아래로 수정:

**META-SKILL = Update Proposal Generator**

* Post-call에:

  1. 요약/케이스 노트 생성(`past_interviews/...md`)
  2. 패턴/승리 답변 업데이트를 **바로 반영하지 않고**

     * **Diff/PR 초안** 형태로 제안
     * "Needs review" 상태로 남김
* 데모에서는:

  * "✅ Draft PR created" / "Suggested update"로 보여주고
  * "Human review → merge → version bump" 한 문장으로 마무리

---

## 5) 에이전트 오케스트레이션 계획(구현 디테일)

### Router

* 입력: 최근 30~60초 transcript chunk + 현재 active skills + (optional) customer profile
* 출력: needs_skill, suggested_skills(top3), trigger_reason, confidence, urgency, detected_question
* 스로틀링:

  * 같은 도메인으로 연속 발동 방지(예: 20초 쿨다운)
  * confidence 낮으면 "clarifying question" 추천만(Answerer 호출 X)

### Summarizer

* 입력: 누적 transcript(전부가 아니라 prev_summary + recent chunk 방식 권장)
* 출력: live summary, key moments, predicted questions, suggested asks, (optional) similar cases
* 업데이트 주기:

  * 45~60초 또는 topic shift 시

### Answerer

* 트리거:

  * Router가 urgency=high로 질문 감지했을 때
  * Ask Copilot 입력 시
* 동작:

  * 선택된 skills만 attach(container.skills)
  * answer + sources + confidence + caveats + followups + escalation_action 생성
* 불확실성 처리:

  * "확인 필요"를 명시하고 Slack draft(또는 follow-up) 제시

---

## 6) UI/UX 업데이트 계획

### 화면 요소(필수)

* Transcript 패널(좌측): 시뮬레이션 재생 + 최근 chunk 강조 + 질문 후보 표시
* Copilot 패널(우측):

  * Live Summary
  * Key Moments
  * Predicted Questions
  * Active Skills(Attached/Recommended)
  * ⚡ Skill Fired 로그(시간/이유/스킬)
  * Suggested Answer 카드(근거/확신도/카피 버튼)
* Ask Copilot 입력(우측 하단): 직접 타이핑 → Answerer 호출

### 시각 연출 포인트(데모 설득력)

* 질문이 "깔끔하지 않음(um… like…)" → Router가 의도 재구성 → Skill Fired
* "조직에 있던 정보가 지금 이 순간 흐른다(flow)"를 한 줄로 반복

---

## 7) 데이터/시뮬레이션 계획

### 프리셋 transcript(필수 트리거 3개)

* 애매한 아키텍처 질문("how data flows / technical part")
* 로드맵/ETA 질문("when shipping / GA")
* 컴플라이언스/보안 질문("SOC2 / data residency / on-prem")
* 간접 social proof 요청("we've talked to vendors doing this for banks…")

### 데모 데이터 원칙

* 실존 고객/실존 로드맵/실존 수치 금지(또는 철저히 익명화/가상화)
* "예시 문구"로 처리하거나, "공유 가능한 범위"만 사용

---

## 8) 리스크/대응(업데이트)

### 기술 리스크

* API 실패 → mock replay + "Demo mode"
* JSON 파싱 → Raw JSON 탭 + 최소 렌더 fallback
* Skill selection thrash → Router 쿨다운 + confidence threshold

### 메시지 리스크

* "Single point of truth" 오해 → "curated playbooks / verified interface"로 표현
* "RAG 폄하" → 역할 분담으로 비교
* "META가 자동 수정?" → PR/diff 제안으로 조정

---

## 9) 구현 체크리스트(P0 중심)

### P0 구현 순서(권장)

1. transcript simulation + UI skeleton
2. Router agent(주기 호출) + Skill Fired UI
3. Answerer(동적 skills attach) + Suggested Answer 카드
4. Ask Copilot 입력 → Answerer 연결
5. Without/With 비교 모드(동일 입력, skills만 차이)
6. Summarizer(요약/예측 질문)
7. META-SKILL(케이스 노트 + diff/PR 초안 화면)

---

## 10) 산출물 정의(PLAN 관점)

* Demo App(React UI + backend orchestrator)
* Skills 패키지(roadmap/architecture/security + optional)
* Preset transcript 시나리오(3~4개 트리거)
* Mock fallback 데이터
* 데모 안정성 체크리스트(오프라인 재생 가능)

---

## Reference Links

[1]: https://platform.claude.com/docs/en/build-with-claude/skills-guide "Using Agent Skills with the API - Claude Docs"
[2]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool "Code execution tool - Claude Docs"
[3]: https://platform.claude.com/docs/en/build-with-claude/structured-outputs "Structured outputs - Claude Docs"
[4]: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills "Equipping agents for the real world with Agent Skills \ Anthropic"
[5]: https://platform.claude.com/docs/en/build-with-claude/context-editing?utm_source=chatgpt.com "Context editing - Claude Docs"
[6]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool?utm_source=chatgpt.com "Memory tool - Claude Docs"

