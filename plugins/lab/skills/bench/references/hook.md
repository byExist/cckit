# 검증 안내: 훅

대상: PreToolUse/PostToolUse 등 훅 스크립트와 그 등록.

## 단위 검증: 스크립트 직접 호출

훅은 stdin으로 이벤트 JSON을 받는 프로세스다. 하네스 없이 직접 넣어 exit code와 stdout을 관찰한다.

```bash
printf '{"tool_input":{"file_path":"%s"}}' "$TARGET" | python3 hook.py
```

- 침묵해야 하는 경로(비대상 파일, 없는 파일, 도구 미설치)는 "출력 없음 + exit 0"으로 확인한다.
- 환경 변형은 env로 주입한다: 설정 경로는 전용 env var로, 설정 해석 순서는 가짜 HOME으로 (`HOME=$T/homeA python3 hook.py`처럼 지정해, 개인 설정 존재/부재 케이스를 디렉터리로 구성한다).
- 훅이 임시 디렉터리를 제외한다면 시료를 tmp 밖(홈 아래 임시 디렉터리)에 둬야 한다. 다 쓰면 지운다.

## 실제 세션 검증: 트랜스크립트

등록, 매칭, 중복 발화는 단위 검증으로는 보이지 않는다. 새 `claude -p` 세션에 해당 도구를 쓰는 과제를 주고, 세션 트랜스크립트에서 발화 횟수를 직접 센다.

- 트랜스크립트: `~/.claude/projects/<cwd 슬러그>/<세션id>.jsonl`. 실행 전후 파일 목록을 비교해 새 세션 파일을 특정한다.
- 발화 1회 = attachment `hook_success` 1건 + (컨텍스트 주입 훅이면) `hook_additional_context` 1건. 문자열 grep이 아니라 attachment type을 세야 중복 발화를 정확히 잡는다.
- 권한은 `--allowedTools`로 좁혀 열고, 모델은 haiku면 충분하다.

## 함정

- 열려 있는 세션은 시작 시점의 훅 설정 스냅숏을 쓴다. 설정을 바꿨으면 반드시 새 세션으로 검증한다.
- 훅의 stdout(additionalContext)은 실행 세션의 모델 행동을 바꾼다. 과제 프롬프트에 "고치지 말고 멈춰라"를 명시해 2차 행동이 측정을 흐리지 않게 한다.

검증 기록: 2026-09-02, mdlint 이전 검증 8종 (단위 6 + 설정 우선순위 2) + 실제 세션 발화 카운트 (이전 2회 → 제거 후 1회).
