# prose

쓴 글을 고치는 스킬 모음입니다.

## korean

`/korean [대상]`으로 호출합니다. 산출물의 한국어를 `prose:rewriter` 에이전트(새 컨텍스트)가 처음부터 한국어로 쓴 글처럼 다시 쓰고, 호출한 세션이 diff를 검토해 의미·식별자·용어 파손만 되돌립니다.

- 대상을 생략하면 세션의 한국어 산출물이 대상입니다.
- 다시 쓰기 전 원본을 확보해(git 또는 사본) diff 검토가 가능해야 합니다.
- 회귀 시료와 검증 절차는 [skills/korean/tests/](skills/korean/tests/README.md)에 있습니다.

## prune

`/prune [대상] [독자]`로 호출합니다. 산출물에서 독자와 그의 목적에 쓰이지 않는 내용을 `prose:pruner` 에이전트(새 컨텍스트, opus)가 걷어내고, 호출한 세션이 diff를 검토해 세션만 아는 근거로 필요한 내용만 되돌립니다. 무엇을 제거했는지, 무엇을 고민했는지 보고합니다.

- 독자를 생략하면 대화에서 유추하고, 확실하지 않으면 묻습니다.
- 회귀 시료와 검증 절차는 [skills/prune/tests/](skills/prune/tests/README.md)에 있습니다.
