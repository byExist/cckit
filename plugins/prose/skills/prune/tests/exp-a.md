# cckit 온보딩 가이드

## 이 저장소는 무엇인가

`cckit`은 Claude Code 플러그인 마켓플레이스다.
애플리케이션이나 라이브러리 코드가 아니라, Claude Code 세션에 설치해서 쓰는 동작 확장 패키지(훅, 스킬, 서브에이전트)를 모아 배포하는 곳이다.
`.claude-plugin/marketplace.json`이 마켓플레이스 정의 파일이고, 소유자는 `byExist`다.
설계 원칙은 "독립적으로 켜고 끌 수 있는 동작마다 플러그인 하나"다.
저장소는 순수 마크다운 문서, JSON 설정, 소규모 훅 스크립트로만 구성되어 있고, 빌드 과정이나 CI가 없다.

## 디렉토리 구조

```text
cckit
├── .claude-plugin/
│   └── marketplace.json      # 마켓플레이스 정의: 플러그인 목록/메타데이터
├── README.md                 # 설치 방법, 자동 업데이트 안내
└── plugins/
    ├── mdlint/                # 플러그인: markdown lint 훅
    └── prose/                 # 플러그인: 글 다듬기 스킬 모음
```

새 플러그인을 추가할 때는 `plugins/<이름>/` 디렉토리를 만들고 `marketplace.json`에 항목을 등록하는 구조다.

## 설치와 사용

README에 안내된 설치 절차는 다음과 같다.

```text
/plugin marketplace add byExist/cckit
/plugin install mdlint@cckit
```

자동 업데이트는 기본적으로 꺼져 있다.
`/plugin` UI에서 켜거나, `settings.json`에 `extraKnownMarketplaces.cckit.autoUpdate: true`를 설정하면 된다.
저장소 단위로 `.claude/settings.json`에 `extraKnownMarketplaces`와 `enabledPlugins`(예: `"mdlint@cckit": true`)를 커밋해 두면 세션을 열 때 자동으로 등록·설치되며, 클라우드 세션(claude.ai/code)에도 동일하게 적용된다.
개인적으로 특정 플러그인을 끄고 싶다면 프로젝트 설정보다 우선순위가 높은 `.claude/settings.local.json`에서 opt-out하면 된다.

## 플러그인 소개

### mdlint — markdown lint 훅

`.md` 파일을 편집한 직후 `markdownlint-cli2`를 실행해 결과를 에이전트에게 알려주는 report-only 훅이다.
파일을 직접 고치지는 않는다.

- 위반이 발견되면 "이번 편집이 만든 위반만 고치고 기존 위반은 건드리지 말라"는 지침을 함께 전달한다.
- 도구 자체가 실패한 경우(설정 오류, 크래시 등)에는 "파일 문제가 아니니 고치지 말고 사용자에게 한 줄로만 알려라"는 지침을 전달한다.
- 그 외 상황(비-md 파일, 임시 디렉터리, 파일 없음, `markdownlint-cli2` 미설치, 타임아웃)에는 아무 동작도 하지 않는다.

설정은 다음 순서로 해석된다.

1. `MARKDOWNLINT_HOOK_CONFIG` 환경 변수 (테스트용)
2. `~/.claude/.markdownlint-cli2.jsonc` (개인 취향)
3. 플러그인 번들 기본값 `plugins/mdlint/.markdownlint-cli2.jsonc` (팀 기본값)

번들 기본값은 모든 규칙을 켜되 `MD013`(줄 길이 제한)과 `MD041`(첫 줄 최상위 헤딩)만 끈다.
`MD013`을 끈 이유는 CLAUDE.md에 명시된 "문단은 한 줄로 쓴다" 스타일과 충돌하기 때문이다.

이 훅은 사용자가 `markdownlint-cli2`를 직접 설치해 두어야 동작한다(`brew install markdownlint-cli2` 또는 `npm i -g markdownlint-cli2`).
미설치 상태에서는 조용히 아무 일도 하지 않는다.

### prose — 글 다듬기 스킬 모음

`/korean`, `/prune` 두 슬래시 커맨드를 제공한다.
두 스킬 모두 frontmatter에 `disable-model-invocation: true`가 설정되어 있어, 모델이 자율적으로 판단해 호출하지 않고 사용자가 명시적으로 슬래시 커맨드를 입력해야만 실행된다.

**`/korean [대상]`**
산출물의 한국어를 처음부터 한국어로 쓴 글처럼 다시 쓴다.
"자기가 쓴 문장은 자기 눈에 자연스러워 보인다"는 이유로, 현재 세션이 직접 고치지 않고 `prose:rewriter` 서브에이전트(새 컨텍스트)에 위임한다.
위임이 끝나면 호출 세션이 diff를 검토해 의미, 식별자, 프로젝트 용어가 훼손된 부분만 되돌린다.
대상을 생략하면 현재 세션의 한국어 산출물이 대상이 된다.

**`/prune [대상] [독자]`**
이미 쓴 글에서 독자가 필요로 하지 않는 내용을 덜어낸다.
판단 기준은 "독자가 쓰는 문장은 남기고, 글쓴이를 위한 문장은 덜어낸다"이며, 애매할 때는 "그 문장 없이 읽어도 독자가 똑같이 판단하고 행동하는가"로 테스트한다.
대상이나 독자가 불분명하면 사용자에게 먼저 질문한다.

각 스킬은 `SKILL.md`(영문)와 `SKILL.ko.md`(한글) 두 버전을 병행 관리한다.

## 스킬 작성 컨벤션

스킬은 `plugins/<플러그인명>/skills/<스킬명>/SKILL.md` 경로 규칙을 따르며, 필요하면 `SKILL.ko.md`처럼 언어별 버전을 나란히 둔다.

frontmatter에서 공통으로 쓰는 필드는 다음과 같다.

- `name`: 스킬 이름 (슬래시 커맨드 이름과 일치)
- `description`: 한 줄 설명
- `argument-hint`: 인자 힌트 문자열, 예: `"[target] [reader] (each optional)"`
- `disable-model-invocation: true`: 모델이 자율적으로 호출하지 못하게 막고, 사용자가 슬래시 커맨드를 직접 입력해야만 발동하게 한다

본문은 `# 스킬이름` 헤딩과 `## Dispatch`, `## Review` 같은 하위 섹션으로 구성되며, 서술형 자연어 지침으로 작성한다.
스킬이 서브에이전트에 위임하는 패턴도 있다(`/korean` → `prose:rewriter`).
에이전트 정의는 `plugins/<플러그인>/agents/<에이전트명>.md`에 두고, frontmatter에 `name`, `description`, `tools`, `model`을 지정한다.

`plugins/prose/skills/korean/tests/`에는 고정 시료(`exp-a.md`, `exp-b.md`)와 절차·판정 기준을 담은 `README.md`가 있다.
에이전트 프롬프트 문구를 고친 뒤 행동이 회귀했는지 수동으로 검증하는 절차이며, 판정 기준을 "반드시 잡아야 하는 것", "지켜야 하는 것(위반 시 회귀)", "계약 밖(보너스)" 세 단계로 나눈다.

## 이 저장소에서 하게 될 작업

커밋 이력을 보면 전형적인 작업 패턴은 코드 리팩토링이 아니라 스킬 지침 문서를 리뷰 피드백에 맞춰 반복적으로 다듬는 것이다.
새 플러그인이나 스킬을 추가한 뒤, 이어지는 여러 커밋이 그 `SKILL.md` 본문의 규칙 문구를 좁히거나("Scope prune rewrites to swollen paragraphs"), 판정 기준을 다시 세우거나("Rebuild prune body around the reader-serving criterion"), 서술을 관찰 가능한 증상 중심으로 바꾸는("Rephrase prune's both-sides item as observable symptom") 식이다.
즉 이 저장소에서 일하는 감각은 프롬프트 엔지니어링에 가깝다: 지침 한 줄이 실제로 어떤 행동 변화를 낳는지 테스트 시료로 확인하고, 리뷰에서 나온 반례를 규칙에 반영해 좁혀 나가는 작업이다.

## 참고 사항

- `LICENSE`, `CONTRIBUTING.md`, `package.json`, CI 설정은 저장소에 없다.
- 저장소는 2026년 9월 2일 하루에 시작되어 빠르게 발전 중이다.
- 새 플러그인을 만들 때는 `mdlint`(훅 중심)와 `prose`(스킬 중심) 두 플러그인의 디렉토리 구조를 참고하면 된다.
