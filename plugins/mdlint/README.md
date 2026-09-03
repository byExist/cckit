# mdlint

md 파일 편집 직후 markdownlint-cli2로 lint하고, 결과를 프레이밍된 컨텍스트로 에이전트에게 전달하는 Claude Code 플러그인입니다. report-only로 동작하며 파일을 절대 수정하지 않습니다.

## 동작 방식

PostToolUse(`Edit|Write|MultiEdit`) 훅이 md 파일 편집을 감지해 markdownlint-cli2를 실행합니다.

- 위반 발견 시: "위반은 파일 전체 대상이니 이번 편집이 만든 것만 고치고, 기존 위반은 사용자 요청 없이 두라"는 지침과 함께 위반 목록을 주입합니다.
- 도구 자체 장애 시: "파일 문제가 아니니 파일을 고치지 말고 사용자에게 한 줄로 알려라"는 지침과 함께 에러 요지만 주입합니다.
- 그 외에는 침묵합니다: 비-md 파일, 임시 디렉터리 아래의 파일, 존재하지 않는 파일, markdownlint-cli2 미설치, 내부 타임아웃.

## 의존성

markdownlint-cli2를 직접 설치해야 합니다. 미설치 상태에서는 훅이 조용히 아무 일도 하지 않으므로, 설치 전까지는 lint가 동작하지 않는다는 점에 유의하세요.

```bash
brew install markdownlint-cli2
```

```bash
npm i -g markdownlint-cli2
```

## 설정 해석 순서

`--config`로 전달되는 base 설정은 다음 순서로 결정됩니다.

1. `MARKDOWNLINT_HOOK_CONFIG` 환경변수 (테스트용)
2. `~/.claude/.markdownlint-cli2.jsonc` (개인 취향, 존재할 때)
3. 플러그인에 번들된 `.markdownlint-cli2.jsonc` (기본값)

프로젝트의 `.markdownlint*` 설정 파일은 markdownlint-cli2의 자체 디스커버리로 base 위에 겹쳐지므로, 어느 경우든 프로젝트 설정이 우선합니다.

## 번들 기본값

모든 규칙을 켜되 두 가지만 끕니다.

- `MD013` (줄 길이 제한): 한 문단을 한 줄로 쓰는 스타일과 충돌
- `MD041` (첫 줄 최상위 헤딩): 헤딩 없이 시작하는 문서 허용
