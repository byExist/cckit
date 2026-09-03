# cckit

Claude Code 플러그인 마켓플레이스입니다.

## 플러그인 목록

- [mdlint](plugins/mdlint/README.md): md 파일 편집 직후 markdownlint-cli2로 lint하고 결과를 에이전트에게 리포트 (report-only)
- [prose](plugins/prose/README.md): 쓴 글을 고치는 스킬 — `/korean`은 산출물의 한국어를 처음부터 한국어로 쓴 글처럼 다시 쓰고, `/prune`은 독자에게 불필요한 내용을 덜어낸다
- [lab](plugins/lab/README.md): 하네스 실험 도구 — `/bench`가 스킬·훅·에이전트·프롬프트의 변형을 요소별 플레이북에 따라 격리 실행해 크기 변화·토큰·시간·비용을 계측한다

## 설치

Claude Code 세션에서 마켓플레이스를 등록하고 원하는 플러그인을 설치합니다.

```text
/plugin marketplace add byExist/cckit
/plugin install mdlint@cckit
```

## 자동 업데이트

커스텀 마켓플레이스는 자동 업데이트가 기본으로 꺼져 있습니다. `/plugin` → Marketplaces 탭 → cckit 선택 → "Enable auto-update"로 켜거나, settings.json에 선언할 수 있습니다.

```json
{
  "extraKnownMarketplaces": {
    "cckit": {
      "source": {
        "source": "github",
        "repo": "byExist/cckit"
      },
      "autoUpdate": true
    }
  }
}
```

수동 갱신은 `/plugin marketplace update cckit`으로 합니다.

## 리포지토리 일괄 적용

리포지토리의 `.claude/settings.json`에 아래를 커밋하면, 그 리포에서 세션을 열 때 마켓플레이스 등록과 플러그인 설치가 자동으로 이루어집니다. 클라우드 세션(claude.ai/code)에서도 동일하게 적용됩니다.

```json
{
  "extraKnownMarketplaces": {
    "cckit": {
      "source": {
        "source": "github",
        "repo": "byExist/cckit"
      }
    }
  },
  "enabledPlugins": {
    "mdlint@cckit": true
  }
}
```

개인적으로 끄고 싶은 플러그인은 `.claude/settings.local.json`에서 옵트아웃합니다 (local이 project보다 우선).

```json
{
  "enabledPlugins": {
    "mdlint@cckit": false
  }
}
```
