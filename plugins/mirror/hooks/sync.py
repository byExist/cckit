#!/usr/bin/env python3
"""PostToolUse hook: when an instruction file the harness discovers by a fixed
basename is edited, remind the agent to keep its user-language mirror
(<stem>.<code>.md) in sync, and vice versa.
The language code is derived from the "language" field in ~/.claude/settings.json.

The mirror is opt-in per directory: the reminder fires only where one already
exists, so instructions already written in the user's language never get a
duplicate, and a repo opts in by creating the file.

Only fixed-basename sources belong in ORIGINALS. Directory-keyed sources
(.claude/rules|agents|commands|output-styles/*.md) take any filename, so a
mirror dropped beside them would itself be loaded as a rule/agent/command.
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

LANG_CODES = {
    "한국어": "ko", "korean": "ko",
    "日本語": "ja", "japanese": "ja",
    "中文": "zh", "简体中文": "zh", "繁體中文": "zh-tw", "chinese": "zh",
    "español": "es", "spanish": "es",
    "français": "fr", "french": "fr",
    "deutsch": "de", "german": "de",
    "português": "pt", "portuguese": "pt",
    "italiano": "it", "italian": "it",
    "русский": "ru", "russian": "ru",
    "tiếng việt": "vi", "vietnamese": "vi",
    "ไทย": "th", "thai": "th",
    "bahasa indonesia": "id", "indonesian": "id",
    "türkçe": "tr", "turkish": "tr",
    "polski": "pl", "polish": "pl",
    "nederlands": "nl", "dutch": "nl",
    "العربية": "ar", "arabic": "ar",
    "हिन्दी": "hi", "hindi": "hi",
    "українська": "uk", "ukrainian": "uk",
    "čeština": "cs", "czech": "cs",
    "svenska": "sv", "swedish": "sv",
}

# MEMORY.md is deliberately absent: it is the agent's own auto-memory, not
# instructions the user authors and reviews.
ORIGINALS = ["CLAUDE.md", "CLAUDE.local.md", "SKILL.md"]


def lang_code() -> Optional[str]:
    try:
        settings = json.loads((Path.home() / ".claude" / "settings.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None
    language = str(settings.get("language", "")).strip().lower()
    if re.fullmatch(r"[a-z]{2,3}(-[a-z]{2,4})?", language):
        code = language
    else:
        code = LANG_CODES.get(language)
    return None if code in (None, "en") else code


def main() -> None:
    code = lang_code()
    if code is None:
        return
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    path = data.get("tool_input", {}).get("file_path", "")
    if not path:
        return
    name = Path(path).name
    originals = {o: o.replace(".md", f".{code}.md") for o in ORIGINALS}
    mirrors = {v: k for k, v in originals.items()}
    if name in originals:
        if not Path(path).with_name(originals[name]).exists():
            return
        context = (
            f"{name} was edited. {originals[name]} in the same directory is its "
            "user-language translation mirror. Apply the same change there, "
            "translated — not copied verbatim. If the mirror already reflects "
            "this change, do nothing."
        )
    elif name in mirrors:
        context = (
            f"{name} was edited. It is a user-language translation mirror; the "
            f"harness loads only the original {mirrors[name]}, so a change made "
            "only in the mirror has no effect. Apply the same change to "
            f"{mirrors[name]} in the original's language. If the original "
            "already reflects this change, do nothing."
        )
    else:
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
