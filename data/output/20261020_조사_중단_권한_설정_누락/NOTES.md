# 2026-10-20 (화) — 조사 단계에서 중단 (권한 설정 누락)

**상태: `needs_human`** · 오늘은 카드가 없다. facts.json·content.json·검증·렌더를 하지 않았다. `data/state/index.jsonl`도 건드리지 않았다.

## 무슨 일이 있었나

1단계 조사에서 `WebSearch`와 `WebFetch`가 둘 다 **권한 거부**됐다. 원문을 열 수 없으면 카드를 만들 수 없다(pipeline_prompt.md 1단계, '절대 하지 않을 것'). 그래서 바로 멈췄다.
`curl` 같은 우회 수단은 쓰지 않았다. 무인 설정이 일부러 막아 둔 수단이고, 권한 경계를 피해 가는 일이기 때문이다.

## 원인 (확인함)

10-19 코드/데이터 분리 작업 때 설정 파일 두 개가 `code/config/`로 옮겨졌다. 그런데 이 파일들을 읽는 쪽이 여전히 옛 위치를 찾는다.

| 파일 | 지금 있는 곳 | 찾는 곳 | 결과 |
|---|---|---|---|
| 프로젝트 기본 권한 (WebSearch·WebFetch·python 허용) | `code/config/claude_settings.json` | `.claude/settings.json` (**없음**) | 허용 목록이 아예 안 실렸다 → 웹 도구 거부 |
| 무인 실행 제약 (인스타 발행 차단·원본 보호) | `code/config/unattended_settings.json` | `code/automation/unattended_settings.json` (`run_daily.ps1:152`) | 로그 `data/logs/2026-10-20.log` 04:26:25 WARN: "unattended_settings.json 이 없다 — 발행 차단 규칙 없이 실행된다" |

참고로 `python`을 `Bash`로 부르는 것도 이번 세션에서는 허용 목록에 없었다. 조사가 통과됐더라도 4단계 `render.py`와 5단계 `verify.py`에서 같은 이유로 막혔을 가능성이 크다.

## 사람이 할 일 (아침)

1. `code/config/claude_settings.json`을 `.claude/settings.json`으로 복사한다. 아니면 `run_daily.ps1`이 `--settings`로 이 파일도 함께 넘기게 한다.
2. `run_daily.ps1:152`의 경로를 `code/config/unattended_settings.json`으로 고친다(예: `Join-Path $Here '..\config\unattended_settings.json'`).
3. `unattended_settings.json`의 deny 경로가 옛 구조 기준이다: `Edit(automation/**)`, `Edit(HCI_인스타그램_콘텐츠_프롬프트_v3.md)`. 이대로면 원본 보호가 실제로는 걸리지 않는다. `code/**` 기준으로 바꿔야 한다.
4. (경미) `config.json`의 `claude_path`·`codex_path`가 옛 버전 폴더를 가리킨다. 자동 탐색이 성공했으니 오늘 문제와는 무관하다. 비워 두거나 새 경로로 갱신하면 된다.
5. 고친 뒤 `run_daily.ps1 -DryRun`으로 한 번 돌려 본다. 웹 검색과 python 호출이 통과되는지 확인한다.

이 문제들은 `data/output/` 밖의 파일이라 파이프라인이 직접 고치지 않았다.

## 오늘 기획에 쓰려던 것 (다음 실행 참고)

- 요일 주제: 화 — 챗봇, 의인화, 감정, 사회적 상호작용
- 반려 사유 반영: 최근 30일 `rejected` 0건이다. decisions.jsonl 2건(10-18, 10-19)은 모두 `expired`(21시 미검토 자동 보류)라 반영할 사유가 없다.
- 14일 내 강조색 피하기: #B03A2E #B23A7A #5B3F8C #6B7F1E #16878C #B07D1A #2E5EAA #3D7A45 #C4581A
- 후보 메모: 10-13 실행의 2순위였던 *Mind Perception Influences Perceived AI Companionability* (arXiv 2610.06681)가 아직 쓰이지 않았다. 다만 그때 "효과가 약하고 쉽게 설명하기 어렵다"는 이유로 밀렸다.
