# HCI 인스타그램 콘텐츠 파이프라인 — 로그·결과물 저장소

AICX: AI·IT 기반 콘텐츠 자동화와 미디어 시스템(이대환 교수) 개인 프로젝트.
매일 새벽 PC에서 파이프라인이 돌아 카드뉴스 초안을 만들고, **이 저장소에 로그와 결과물이 쌓인다.**
발행(인스타 업로드)은 사람이 한다.

## 폴더 구조 — 코드와 데이터 분리 (9/28 피드백 반영)

```
code/                       ← 코드 (사람이 고칠 때만 바뀜)
  automation/               파이프라인 본체 (run_daily.ps1, engine.py, render.py, verify.py, facts.py …)
  prompts/                  기획실 프롬프트 v3
  config/                   권한·가드레일 설정 (무인 실행 시 발행·삭제·git 차단)
  tools/check_images.py     개인과제 지표 계산기
data/                       ← 데이터 (매일 자동으로 쌓임)
  logs/                     날짜별 실행 로그 (run_daily.ps1 출력)
  state/                    index.jsonl(누적 이력), last_run.json(마지막 실행 요약)
  output/<날짜_주제>/       카드 6장·캡션·NOTES·verdict·STATUS
  image_tests/<날짜>/       Figma MCP 이미지 생성 테스트
  metrics/image_open_rate.json   지표 결과
docs/                       ← 대시보드 (GitHub Pages로 발행)
  index.html                대시보드 코드
  data/manifest.json        대시보드가 읽는 데이터 인덱스
  cards/                    카드 사본
```

대시보드는 `output/`을 직접 뒤지지 않고 `docs/data/manifest.json` 하나만 읽는다.

## 올리지 않는 것 (수업 규칙 + 공개 저장소)
비밀키·토큰, 논문 원문 전문(`_source.*`), AI 대화 전체(`_codex_log.txt`), 감사실 내부 지시문.
공개 저장소이므로 내부 검토 파일(facts.json, verdict.json, GPT 원문 판정, 재시도 기록)도 올리지 않는다. `.gitignore`와 업로드 스크립트 양쪽에서 막는다.

## 지표 (개인과제)
**정상적으로 열리는 이미지 수 / 만들기로 한 이미지 수** — 로그의 성공 숫자가 아니라 PNG를 실제로 열어서(디코딩) 센다.

```
python code/tools/check_images.py data      # → data/metrics/image_open_rate.json
python code/automation/build_manifest.py data docs
```

## 자동 업로드 흐름
1. 03:00~05:00 PC 작업 스케줄러 → `run_daily.ps1` → `output/`·`logs/`·`state/` 생성 (PC 로컬)
2. 매일 아침 클라우드 예약 작업이 PC 폴더에서 새 결과만 가져와 → 금지 파일 제외 → 지표·manifest 재계산 → 이 저장소에 commit/push
3. push되면 GitHub Actions가 `docs/`를 Pages로 발행
