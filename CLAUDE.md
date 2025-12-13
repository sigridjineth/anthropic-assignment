# Important
- Don't use mock. This is real, production-grade app. **IMPORTANT**
- Read https://platform.claude.com/docs/en/home for each implementation.
- Use the latest features like Skills, Context Editing, Memory and etc.
- Implement Plan correctly.
- I love minimality. Write the code if and only if they are needed. otherwise, consider removing it or simplifying it.
- Write in Python using `uv` package manager.

# Plan
아래는 요청하신 방향(Technical Sales 팀용, **Skills 중심**, **대화 흐름을 보다가 필요할 때 Skill을 “발동”**하는 **3-Agent 구조**, 우측에 **직접 타이핑 Ask Copilot**, 코파일럿이 **요약/중요도/예측 질문/유사 케이스/추천 질문**까지 띄우는 형태)을 전부 반영한 **전체 테크 스펙(상세 버전)**입니다.
(명확성을 위해 “TTS로 받아적기”는 실제로는 **STT(음성→텍스트)**, “질문 읽어주기”는 **TTS(텍스트→음성)**로 구분해서 설계합니다.)

---

# Technical Sales Interview Copilot — Full Technical Spec v1.0

## 0. 문서 메타데이터

* 문서명: Technical Sales Interview Copilot — Full Technical Spec
* 버전: v1.0
* 목적: **Claude Developer Platform의 Skills 가치**를 “기술 데모로 증명”하기 위한 제품/시스템 스펙
* 1차 사용 대상:

  * Technical Sales / Sales Engineer / Solution Engineer
  * PMM(세일즈 enablement), Support, RevOps(요약/인사이트)
* 데모 형태:

  * (권장) **시뮬레이션 transcript 재생 + 특정 발화에서 Skill 발동**
  * (옵션) 실제 STT 입력
* Claude 플랫폼 기반 기술 가정:

  * Skills는 API 요청의 `container.skills`로 첨부해 사용하며, 요청당 **최대 8개 Skills**를 붙일 수 있음 ([Claude][1])
  * Skills 사용은 **code execution tool**과 함께 쓰는 흐름이 문서 예시에 포함됨 ([Claude][1])
  * code execution tool은 Bash/파일 작업을 포함한 샌드박스 실행을 제공 ([Claude][2])
  * Structured Outputs는 JSON 안정화에 유용하나, 스키마 복잡도/첫 요청 레이턴시 등 고려 필요 ([Claude][3])

---

## 1. 한 줄 요약과 핵심 가치

### 1.1 한 줄 요약

**“기술 세일즈 콜 중 실시간 transcript를 관찰하고, 질문 의도를 분류해 필요한 Skills만 그때그때 발동하여 ‘정확한 답변 + 다음 질문 + 요약 + 유사 사례’를 즉시 제시하는 멀티 에이전트 코파일럿”**

### 1.2 해결하려는 문제

Technical Sales가 자주 겪는 병목:

* 고객이 “이 기능 언제 돼요?”, “알고리즘/아키텍처 어떻게 동작해요?”라고 묻는데

  * 개발 진행상황/내부 구현/정확한 제약을 몰라서 **즉답이 어려움**
* Slack로 엔지니어에게 물어보면:

  * **응답 대기 + 맥락 전달 비용**이 커서 콜 흐름이 끊김
* 단순 RAG:

  * 문서 품질/최신성/정답 근거 관리가 어렵고 **확신도 낮아짐**
* “grep로 다 찾아보기” 스타일:

  * 범위가 넓으면 느리고, 인터뷰 중 실시간 답변에 불리

### 1.3 Skills로 해결하는 핵심

* **지식을 “Skill 패키지”로 배포/버전관리**: 팀 전체 답변 품질 표준화
* **progressive disclosure**(필요할 때만 로드)로 “큰 지식”을 효율적으로 사용 ([Anthropic][4])
* 대화 흐름을 보다가 **필요 시점에 Skill을 “발동”** → **관찰→판단→행동**이 명확한 “agentic” 데모

---

## 2. 목표와 비목표

### 2.1 목표 (Goals)

1. **실시간/준실시간 인터뷰 상황 인식**

   * transcript 누적을 요약하고, 중요한 포인트/리스크/고객 니즈를 구조화
2. **대화 중 “질문 타입”을 감지해 Skill을 동적으로 발동**

   * roadmap / architecture / security / pricing / case study / 경쟁 비교 등
3. **정확한 답변 + 근거(출처) + 확신도 + 후속 질문 제시**
4. **사용자가 직접 물어볼 수 있는 Ask Copilot** 제공
5. (데모에서) **Without Skills vs With Skills**의 결과 차이를 명확하게 보여줌

   * 동일 프롬프트/모델/포맷, `container.skills`만 차이나는 공정 비교

### 2.2 비목표 (Non-goals)

* CRM(Salesforce/HubSpot) 완전 연동
* 콜 녹취 저장/법적 컴플라이언스 완비(프로덕션 범위)
* 모든 엔지니어링 리포지토리를 실시간 검색(대규모 codebase 전체)
* 100% 자동 응답(“사실 확인/범위 밖”일 때는 정직하게 후속 액션 제시)

---

## 3. 핵심 컨셉: 멀티 에이전트(3-Agent) + 동적 Skill 발동

### 3.1 에이전트 구성

* **Agent 1: Router (Skill Selector)**

  * 최근 transcript chunk를 보고 “지금 어떤 Skill이 필요할지” 판단
* **Agent 2: Summarizer (Situation Model Builder)**

  * 전체 transcript 누적을 압축/요약 + 중요도/예측 질문/리스크/유사 케이스 후보 생성
* **Agent 3: Answerer (Skill Executor)**

  * Router가 선택한 Skill(들)을 `container.skills`로 붙여 호출
  * 답변/근거/확신도/후속 질문 생성

> 이 구조는 “처음에 다 로드”가 아니라, 대화 흐름 중 **필요할 때만 Skill을 붙여 요청**하는 점에서 RAG와 구분되는 agentic story가 생깁니다.

---

## 4. 사용자 경험(UX) 스펙

## 4.1 화면 레이아웃 (권장: 2열 + 하단 입력)

**Left: Transcript / Right: Copilot / Bottom: Ask Copilot**

### Left 패널: Transcript

* 실시간 transcript 스트림 (STT 또는 시뮬레이션)
* 발화 타임스탬프, 화자 표시(Prospect / Sales / SE)
* “최근 30초” 하이라이트 영역(= Router 입력 범위)
* Segment 선택:

  * 특정 구간을 클릭/드래그로 선택해 “이 구간 분석” 가능(데모 안정성↑)

### Right 패널: Copilot

* 상단: **Live Summary** (현재까지 한 줄/세 줄 요약)
* 중단1: **Key Moments** (중요 발언과 이유)
* 중단2: **Predicted Questions** (다음에 나올 질문 확률)
* 중단3: **Active Skills** (현재 로드/추천 Skill)
* 하단: **Suggested Answer Draft**

  * 답변 초안 + 출처 + 확신도 + caveat + follow-up 질문
  * (옵션) **TTS 버튼**으로 “답변 읽기/추천 질문 읽기”

### Bottom: Ask Copilot

* 사용자가 직접 질문 입력 → Answerer 호출
* “이 질문에 필요한 Skill 추천”도 함께(= Router를 먼저 한 번 호출하거나, Answerer가 자체적으로 부족하면 Router 요청)

---

## 5. 기능 요구사항 (Functional Requirements)

## 5.1 Transcript 입력

### FR-1: 시뮬레이션 모드(데모 기본)

* 미리 준비한 transcript 시나리오를 재생
* 특정 라인에서 “roadmap 질문”, “architecture 질문”, “security 질문”이 나오도록 설계
* 장점: STT 불안정 리스크 제거

### FR-2: 실시간 STT 모드(옵션)

* 브라우저 SpeechRecognition 또는 외부 STT 공급자
* 2~5초 단위로 partial transcript 업데이트
* 실패 시 fallback: 수동 입력

## 5.2 Router Agent

### FR-3: 주기적 라우팅

* 트리거:

  * (권장) 새 transcript entry가 추가될 때마다
  * (옵션) 10초마다 polling
* 입력:

  * 최근 N초(예: 30~60초) transcript chunk
  * 현재 Active Skill 목록
  * 고객 프로필(있으면)
* 출력:

  * `needs_skill`: boolean
  * `suggested_skills`: top-k(최대 3~5개)
  * `reason`: 트리거 패턴/의도
  * `urgency`: high/med/low
  * `detected_questions`: “방금 나온 질문” 후보(있으면)

## 5.3 Summarizer Agent

### FR-4: 상황 요약/구조화

* 트리거:

  * 60초마다 또는 “topic shift” 감지 시
* 입력:

  * 누적 transcript(원문 전체 대신 **요약 상태 + 최근 chunk**를 주는 방식 권장)
* 출력:

  * 고객/회사/도메인 요약
  * 니즈/성공 기준/리스크
  * 중요한 발언(근거 포함)
  * 예측 질문
  * 유사 케이스 후보(“케이스 스터디 Skill이 있다면” 연결)

## 5.4 Answerer Agent

### FR-5: 자동 답변 제안

* 트리거:

  * Router가 `urgency=high`로 잡은 질문이 발생했을 때
  * 또는 사용자가 Ask Copilot에 입력했을 때
* 입력:

  * current_question
  * summarizer_state (요약)
  * selected_skills (Router output)
* 출력:

  * answer(초안)
  * sources(파일 경로/섹션명 등)
  * confidence(0~1)
  * caveats(변동 가능성/전제조건)
  * followups(다음에 물어볼 질문)
  * escalation_action(불확실할 때 Slack 질문 초안 등)

## 5.5 Skills 관리/표시

### FR-6: Active Skills 패널

* “현재 Answerer 호출에 붙인 Skill”을 배지로 표시
* Router가 추천만 한 Skill은 “Recommended”로 표시(아직 미부착)

### FR-7: Without vs With 비교 모드(데모 핵심)

* 동일 질문/동일 프롬프트/동일 output_format/동일 모델
* 오직 차이: `container.skills` 유무
* UI에서 버튼 토글로 결과 비교

---

## 6. 비기능 요구사항 (Non-Functional Requirements)

* NFR-1: **낮은 지연(데모 체감)**

  * Router는 빠르게(짧은 입력, 낮은 max_tokens)
  * Answerer는 답변 품질 우선(조금 더 긴 max_tokens 가능)
* NFR-2: **정직성**

  * Skill 문서에 없는 내용은 “모른다/확인 필요” + 후속 질문 생성
* NFR-3: **프라이버시**

  * transcript 저장/공유 최소화
  * 데모는 가짜 회사/가짜 로드맵/가짜 케이스로 구성 권장
* NFR-4: **관측 가능성**

  * 어떤 질문에서 어떤 Skill이 왜 발동되었는지 로그/trace

---

## 7. 시스템 아키텍처 (High-level)

## 7.1 컴포넌트 다이어그램

```
[Audio/STT or Simulation]
          |
          v
   Transcript Store (in-memory for demo)
          |
          +-------------------+
          |                   |
          v                   v
   Router Agent Call     Summarizer Agent Call
          |                   |
          +---------+---------+
                    v
              Orchestrator State
                    |
   +----------------+----------------+
   |                                 |
   v                                 v
Answerer Agent Call (Skills attached)  UI Rendering
```

## 7.2 배포 형태(권장)

* Frontend: React (Next.js 가능)
* Backend: Node.js(Express/Fastify)

  * 이유: API Key 보호(브라우저 직접 호출은 키 노출 위험)
* Storage:

  * Demo: 메모리(Map)
  * Prod: DB + 오브젝트 스토리지(선택)
* Skills:

  * Anthropic Console/SDK로 업로드 및 버전관리(커스텀 skill_id 사용) ([Claude][1])

---

## 8. 데이터 모델 & 상태 (Data Contracts)

## 8.1 Transcript 모델

```ts
type Speaker = "prospect" | "sales" | "se";

interface TranscriptEntry {
  id: string;
  ts_ms: number;          // epoch ms
  offset_sec: number;     // call-relative time
  speaker: Speaker;
  text: string;
  confidence?: number;    // STT confidence
}
```

## 8.2 Router Output 스키마

```ts
type SkillDomain =
  | "roadmap"
  | "architecture"
  | "security"
  | "pricing"
  | "case_studies"
  | "competitive"
  | "integration"
  | "deployment";

interface RouterDecision {
  needs_skill: boolean;
  suggested_skills: Array<{
    domain: SkillDomain;
    skill_id?: string;        // 실제 커스텀 skill_01... (있다면)
    priority: number;         // 1..5
    confidence: number;       // 0..1
  }>;
  trigger_reason: string;
  urgency: "high" | "medium" | "low";
  detected_question?: string; // transcript에서 뽑은 질문
}
```

## 8.3 Summarizer Output 스키마

```ts
interface SummarizerState {
  customer_profile: {
    company?: string;
    industry?: string;
    geo?: string;
    size?: string;
    technical_maturity?: string;
  };
  goals: string[];           // "low latency", "SOC2", ...
  constraints: string[];     // "on-prem", "data residency", ...
  key_moments: Array<{
    offset_sec: number;
    quote: string;
    why_important: string;
    importance: "high" | "medium" | "low";
  }>;
  predicted_questions: Array<{
    question: string;
    probability: number; // 0..1
    domain: SkillDomain;
  }>;
  open_questions: string[];
  suggested_asks: string[]; // 우리가 물어볼 discovery 질문
  similar_cases?: Array<{
    case_name: string;
    match_score: number;   // 0..100
    takeaway: string;
    source?: string;       // case skill file
  }>;
}
```

## 8.4 Answerer Output 스키마

```ts
interface AnswerDraft {
  answer: string;
  sources: Array<{
    title: string;
    file: string;
    excerpt?: string; // 1~2줄 요약(긴 인용 X)
  }>;
  confidence: number; // 0..1
  caveats: string[];
  followups: string[];
  escalation_action?: {
    type: "ask_eng_slack" | "schedule_followup";
    draft_message: string;
  };
}
```

---

## 9. Skills 설계 (가장 중요한 파트)

## 9.1 Skill Taxonomy (세일즈 코파일럿용)

**도메인 중심으로 Skill을 쪼갭니다.** (Router가 선택하기 쉽게)

* `roadmap` — 출시 일정, 베타/GA 상태, 제한사항, “말해도 되는 표현”
* `architecture` — 고수준 아키텍처, 데이터 플로우, 알고리즘 개요, 성능 특성
* `security` — 인증/인가, 데이터 암호화, 컴플라이언스(SOC2 등), 보안 FAQ
* `pricing` — 플랜/과금 기준/엔터프라이즈 옵션/FAQ
* `case_studies` — 산업별(핀테크/헬스케어 등) 성공 사례, “어떤 상황에 어떤 스토리를 꺼낼지”
* `competitive` — 경쟁사 대비 포지셔닝(사실 기반 + 표현 가이드)
* `integration` — SDK/연동(웹훅, ETL, warehouse)
* `deployment` — SaaS/온프레미스/하이브리드, 리전, 데이터 레지던시

> API 요청당 Skills는 최대 8개만 붙일 수 있으므로 ([Claude][1]), Router는 항상 “top N”만 선택해야 합니다.

## 9.2 Skill 패키지 구조(권장)

```
sales_copilot_skills/
  roadmap/
    SKILL.md
    references/
      roadmap.md
      release_notes.md
      messaging_guidelines.md
    scripts/
      lookup_roadmap.py
  architecture/
    SKILL.md
    references/
      system_overview.md
      algorithm_faq.md
      perf_limits.md
    scripts/
      answer_arch_questions.py
  security/
    SKILL.md
    references/
      security_faq.md
      compliance_matrix.md
      data_handling.md
  case_studies/
    SKILL.md
    references/
      fintech_beta_bank.md
      saas_gamma_payments.md
      healthcare_delta_health.md
    scripts/
      find_similar_case.py
  pricing/
    SKILL.md
    references/
      pricing_faq.md
      packaging.md
  competitive/
    SKILL.md
    references/
      positioning.md
      battlecards.md
```

### 9.2.1 SKILL.md 작성 원칙

* “이 Skill이 언제 쓰이는지”를 **명확한 트리거**로 정의
* 답변 스타일 가이드 포함:

  * “확실한 것만 말하기”
  * 일정/로드맵은 “변경 가능성 caveat” 자동 포함
* 출력 포맷:

  * Answerer가 UI에 바로 렌더링할 수 있도록 **구조화된 JSON 스키마** 준수

### 9.2.2 progressive disclosure 설명(데모 메시지용)

Skills는 “필요할 때만 관련 파일을 로드”하는 식으로 설계되어 **컨텍스트 창을 과도하게 점유하지 않고도** 큰 지식베이스를 활용할 수 있는 방향으로 소개됩니다. (문서/아키텍처 설명 시 이 톤 사용) ([Anthropic][4])

---

## 10. Claude API 설계 (Messages API + Skills)

## 10.1 Skills 사용 시 필수 요소(데모 기준)

* Skills 사용 가이드 예시에서는 `betas`에 skills/code-execution 관련 헤더를 넣고, `tools`에 code execution tool을 포함합니다. ([Claude][1])
* `container.skills`에 skills 배열을 넣어 사용합니다. ([Claude][1])
* 커스텀 Skill은 `skill_01...` 형태의 ID 예시가 문서에 등장합니다. ([Claude][1])

> **중요(데모 공정성)**: Without/With 비교에서
> model, prompt, tools, output_format, betas 등은 동일하게 두고 **`container.skills`만** 다르게 합니다.

## 10.2 Output 안정화: Structured Outputs(선택)

* 데모에서 JSON 파싱이 실패하면 전체가 무너질 수 있어, `output_format: json_schema`를 고려할 수 있습니다.
* 단, 스키마가 복잡하면 오류 가능성이 있고, 첫 요청은 “grammar 컴파일”로 레이턴시가 늘 수 있으며 캐시가 24시간 유지되는 등의 제약이 문서에 안내됩니다. ([Claude][3])

---

## 11. 에이전트별 호출 설계

## 11.1 Router Agent (Skill Selector)

### 입력 구성

* 최근 30~60초 transcript (짧게)
* 현재 Active Skills
* Summarizer가 만든 customer_profile(있으면)

### 출력

* RouterDecision(JSON)

### 라우팅 로직 (하이브리드 권장)

1. **룰 기반 빠른 매칭(0차)**

* “when/ETA/roadmap/beta/GA” → roadmap
* “how does it work/architecture/algorithm” → architecture
* “SOC2/HIPAA/encryption/data residency” → security
* “pricing/cost/license” → pricing
* “reference/customer story” → case_studies

2. **LLM 분류(1차)**

* 애매한 경우 LLM이 의도 분류 + top3 skills 추천
* 결과의 confidence가 낮으면 “clarifying question”을 suggested_asks로 반환

### Router의 핵심: “Skill 발동 이벤트” 생성

* UI에 “⚡ Router: roadmap 스킬 필요(0.86)” 같이 노출 → agentic 감각 극대화

---

## 11.2 Summarizer Agent (상황모델)

### 입력 구성 전략(토큰 효율)

* 전체 transcript를 매번 보내지 말고:

  * `prev_summary` + `recent_transcript_chunk`만 보내서 “요약 업데이트” 형태로 유지
* 또는 Claude **context editing** 기능을 제품화 단계에서 검토 가능(확장 포인트) ([Claude][5])

### 출력

* SummarizerState(JSON)

### Summarizer가 해야 하는 일(정교한 체크리스트)

* customer_profile 업데이트
* goals/constraints 추출
* key_moments(인용 포함)
* predicted_questions (확률 + domain)
* suggested_asks: “세일즈가 지금 물어봐야 할” discovery 질문
* (옵션) similar_cases 후보:

  * case_studies skill이 있는 경우, “어느 케이스를 꺼내면 좋은지” 힌트 생성

---

## 11.3 Answerer Agent (Skill Executor)

### 입력

* current_question: Router가 감지한 질문 또는 Ask Copilot 입력
* summarizer_state: 현재까지 요약
* selected_skills: Router가 선택한 top N (최대 8)

### Skills 첨부 방식

* API 요청의 `container.skills`에 선택된 skills만 첨부 ([Claude][1])
* 커스텀 skill 업로드는 `client.beta.skills.create` 등으로 생성 가능 ([Claude][1])

### 출력

* AnswerDraft(JSON)
* answer는:

  * 짧고 말로 읽기 좋은 문장(세일즈 콜 톤)
  * 근거(sources)
  * caveat(변경 가능성/전제조건)
  * followups(“얼리 액세스 관심?” 같은 다음 액션)

### “모르면 어떻게?”

* Skill 내 문서에 없거나 불확실하면:

  * “확인 필요”를 명시하고,
  * `escalation_action`으로 Slack 질문 초안 생성
  * (데모에선 “이렇게 안전하게 처리한다”가 오히려 신뢰 포인트)

---

## 12. UI 상세 스펙

## 12.1 상태 머신(간단)

* IDLE (대기)
* LISTENING (STT/시뮬레이션 입력)
* ROUTING (Router 분석 중)
* SUMMARIZING (Summarizer 업데이트)
* ANSWERING (Answerer 답변 생성 중)
* ERROR (fallback)

## 12.2 핵심 UI 컴포넌트 목록

* TranscriptStream

  * 최근 60초 영역 강조
  * 질문 후보(문장 끝 “?” 등) 자동 배지
* RouterPanel

  * “Detected: roadmap(0.86)”
  * “Trigger: ‘언제 도입’”
* ActiveSkillsPanel

  * 활성 skills(배지)
  * 추천 skills(회색)
* LiveSummaryCard
* KeyMomentsList
* PredictedQuestionsList
* SuggestedAnswerCard

  * Copy / TTS Read / Expand Sources
* AskCopilotInput

  * Enter로 질문
  * “Ask” 버튼
* CompareToggle (Without/With)

  * side-by-side JSON/렌더 결과 비교

---

## 13. TTS/STT 설계

## 13.1 STT(옵션)

* 데모 안정성을 위해 기본은 시뮬레이션
* 실제 모드:

  * 브라우저 STT로 partial transcript 업데이트
  * chunk 단위로 Router 트리거

## 13.2 TTS(권장)

* “추천 질문 읽기”
* “답변 초안 읽기”
* 목적: 세일즈가 화면을 계속 보지 않아도 콜 흐름 유지

---

## 14. Observability & Debugging (데모에서도 설득력 큼)

* 이벤트 로그(타임라인):

  * Transcript appended
  * RouterDecision created
  * Skills attached (domains + skill_id)
  * AnswerDraft generated (+ confidence)
* “왜 이 Skill이 선택됐는지”는 항상 UI에 노출(black box 방지)

---

## 15. 보안/프라이버시/Responsible AI

### 15.1 Skill 콘텐츠 신뢰

* Skill은 팀이 만든 “공식 지식 패키지”로 간주
* 프로덕션에서는 “누가/어떻게 업데이트했는지” 변경 이력 필요

### 15.2 민감정보

* transcript/고객정보는 최소 수집
* 데모는 가상 고객/가상 로드맵 사용 권장

### 15.3 메모리/지속성 확장(옵션)

* 장기적으로는 Claude **memory tool**로 “고객별 요약/선호/이슈”를 지속 저장 가능(클라이언트 측에서 저장 위치/방식 통제) ([Claude][6])
* 다만 이번 데모의 주인공은 Skills로 유지하고, memory는 “확장 포인트”로만 언급 추천

---

## 16. 데모 시나리오(권장 transcript 트리거 설계)

**핵심은 “Skill 발동 순간”이 눈에 보이는 것.**

* 구간 1: Roadmap 질문

  * Prospect: “이 기능은 언제 GA 되나요?”
  * Router: roadmap 선택 → Active Skills에 roadmap 추가
  * Answerer: roadmap skill 근거로 답변 + caveat
* 구간 2: Architecture 질문

  * Prospect: “알고리즘은 어떻게 동작하죠?”
  * Router: architecture 선택
  * Answerer: system_overview.md 기반 설명 + 제한사항
* 구간 3: Security 질문

  * Prospect: “SOC2 / 데이터 레지던시는요?”
  * Router: security 선택
  * Answerer: compliance_matrix.md 인용 형태로 답변
* 구간 4: Ask Copilot 직접 입력

  * Sales: “경쟁사 대비 차별점 한 문장으로?”
  * Answerer(competitive skill)로 답변

그리고 마지막에 **Without Skills**로 동일 질문을 던져 “두루뭉술/확신 낮음”을 보여준 뒤, **With Skills**가 “출처/정확성/표현 가이드”까지 제공하는 것을 대비.

---

## 17. 구현 계획(우선순위)

### P0 (데모 필수)

* Transcript 시뮬레이션
* Router Agent(주기적)
* Answerer Agent(Skills 동적 첨부)
* Active Skills 표시
* Ask Copilot 입력
* Without/With 비교 토글

### P1 (있으면 완성도↑)

* Summarizer Agent(주기적)
* Live Summary / Predicted Questions / Key Moments

### P2 (폴리시)

* TTS
* fancy diff 뷰
* error replay / mock fallback

---

## 18. Claude 플랫폼 기능 “증명 포인트” 정리(영상/설명에 그대로 사용 가능)

1. **Skills는 지식을 프롬프트가 아니라 “배포 단위”로 만든다**

   * 팀 표준화, 버전관리, 재사용
2. **대화 흐름을 보고 필요한 순간에 Skills를 붙이는 게 에이전트다**

   * 관찰(Transcript) → 판단(Router) → 행동(Answerer with Skills)
3. **progressive disclosure**로 큰 지식도 효율적으로 쓴다 ([Anthropic][4])

   * “필요할 때만 관련 파일을 로드”하는 식으로 설명
4. **code execution tool**로 Skill 내 스크립트/파일 작업도 가능(빠른 lookup) ([Claude][2])
5. (안정성 옵션) Structured Outputs로 JSON 파싱 리스크를 줄일 수 있으나 제약도 존재 ([Claude][3])

---

## 19. 부록: Skills 생성/업로드(운영 관점)

* 커스텀 Skill은 SDK에서 `client.beta.skills.create(...)`로 업로드하는 예시가 문서에 있음 ([Claude][1])
* 업로드 후 반환되는 `skill_id`(예: `skill_01...`)를 Answerer 호출에 사용 ([Claude][1])

[1]: https://platform.claude.com/docs/en/build-with-claude/skills-guide "Using Agent Skills with the API - Claude Docs"
[2]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool "Code execution tool - Claude Docs"
[3]: https://platform.claude.com/docs/en/build-with-claude/structured-outputs "Structured outputs - Claude Docs"
[4]: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills "Equipping agents for the real world with Agent Skills \ Anthropic"
[5]: https://platform.claude.com/docs/en/build-with-claude/context-editing?utm_source=chatgpt.com "Context editing - Claude Docs"
[6]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool?utm_source=chatgpt.com "Memory tool - Claude Docs"

