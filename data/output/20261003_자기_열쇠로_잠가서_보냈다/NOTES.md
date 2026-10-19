# NOTES — 아침에 읽을 것

**상태: `verify_failed`**. GPT 교차검증을 실행하지 못했다. 그래서 카드(PNG)는 만들지 않았다.

## 무엇이 막혔나

`verify.py --attempt 1`이 3.4초 만에 종료 코드 30으로 끝났다. `_codex_log.txt`에 원인이 있다.

> ERROR: You've hit your usage limit. … try again at Oct 4th, 2026 4:42 AM.

Codex 사용량 한도다. 일시적 오류가 아니라서 재시도하지 않았다. 다시 불러도 같은 응답이 나온다.
지시서 규칙("검증 없이 카드를 만들지 마라")에 따라 6단계 렌더는 하지 않았다. `state/index.jsonl`에도 추가하지 않았다.

**이어서 하려면** (한도가 풀린 2026-10-04 04:42 이후):

```bash
python automation/verify.py --dir "output/20261003_자기_열쇠로_잠가서_보냈다" --attempt 1
```

pass가 나오면 아래를 실행한다.

```bash
python automation/render.py "output/20261003_자기_열쇠로_잠가서_보냈다/content.json"
```

이어서 `STATUS`를 `awaiting_human_review`로 바꾸고 `state/index.jsonl`에 한 줄을 추가한다.
`PROGRESS.log`가 남아 있으니, 무인 실행이 이 폴더를 만나면 5단계부터 이어받는다.

참고: **내일(10-04) 새벽 무인 실행도 같은 한도에 걸릴 수 있다.** 실행 시각이 04:42 이전이면 그렇다.
오늘 로그 시작이 04:18이었다. 실행 시각을 늦추거나 Codex 크레딧을 확인해야 한다.

## 오늘 고른 주제와 이유

- **요일 주제**: 토. 최근 자료가 아니어도 좋은 고전 또는 재발견 HCI 연구다.
- **선정 논문**: Whitten & Tygar, *Why Johnny Can't Encrypt: A Usability Evaluation of PGP 5.0*
  - USENIX Security 1999 프로시딩에 실린 동료평가 논문이다. 프리프린트가 아니다.
  - USENIX 공식 PDF 전문을 python으로 받아 확인했다. 사본은 `_source.pdf`와 `_source.txt`.
- **핵심 내용**:
  - 이메일에 익숙한 12명에게 90분을 주고, PGP 5.0으로 비밀 일정을 서명·암호화해 보내게 했다.
  - 11명은 암호화하는 방법을 찾았다.
  - 그중 7명이 팀원의 공개키가 아니라 **자기 공개키로 잠가서** 보냈다.
  - 끝까지 제대로 보낸 사람은 4명이었다.
  - 3명은 비밀을 평문으로 보냈다.
- **선정 이유**:
  - "자기 열쇠로 잠가 보냈다"는 행동은 통계 용어 없이 설명된다.
  - 열쇠라는 단일 오브젝트로 6장을 그릴 수 있다. PGP 화면도 열쇠 그림을 썼다.
  - 사용성 보안 분야의 대표 고전이다.
  - 집단 비교가 없어서 낙인 위험이 낮다.
- **선정문**: `content.json` → `selection_sentence`
- **오브젝트**: 열쇠 (과거 오브젝트와 겹치지 않는다)
- **강조색**: `#4A4FA3` 남색 (최근 14일 안에 쓴 색과 겹치지 않는다)

## 탈락한 후보 (전체 12건, 사유는 `content.json` → `candidates`)

- **2순위: Mark, Gudith, Klocke — The Cost of Interrupted Work (CHI 2008)**
  - 원문을 확인했다. "방해받으면 더 빨리 끝냈지만 더 스트레스를 받았다"는 반전이 좋다.
  - 다만 9/21 속도 착각 게시물, 9/27 알림 게시물과 주제가 겹친다.
- Sunshine 외 *Crying Wolf* (2009)
  - 원문을 확인했다. 조건이 많아 6장에 압축하기 어렵고, 오늘 선정작과 분야가 같다.
- Ophir 외 미디어 멀티태스커 (2009)
  - 원문을 확인했다. 핵심이 집단 비교라 낙인 위험이 있고, 재현 논란도 있다.
- Harrison 외 *Faster Progress Bars*: 9/26에 이미 다뤘다.
- 원문 접근 실패 7건(ACM 403, 404, SSL 오류, 연결 시간 초과):
  - Schechter *Emperor's New Security Indicators*
  - Hancock *Deception and design*
  - Kurosu & Kashimura
  - Buell & Norton *Labor Illusion*
  - Iqbal & Horvitz
  - Egelman 피싱 경고
  - Kraut *Internet Paradox*

## GPT가 지적했고 고친 것

없음. 검증을 실행하지 못했다.

## GPT가 지적했지만 고치지 않은 것

없음. 검증을 실행하지 못했다.

## 지금 폴더 상태

- `facts.json`: findings 10건.
  - findings와 design에 넣은 원문 인용 22건을 `_check_quotes.py`로 `_source.txt`와 대조했다. 모두 일치했다.
  - 한 건은 스크립트 정규식이 제목 속 아포스트로피 때문에 잘못 잘랐다. 따로 직접 대조해 일치를 확인했다.
- `content.json`: 자가검사(`render.py --check-only`)를 통과했다. 오류 0건, 경고 0건.
- 레이아웃 미리보기:
  - 임시 폴더(`%TEMP%\hci1003\preview`)에 렌더해서 6장을 직접 봤다.
  - 글자 잘림이나 겹침은 없었다.
  - 1장 열쇠가 작아 보여서 크기만 키웠다. 문구는 바꾸지 않았다.
  - 이 미리보기는 산출물이 아니다. 검증 전이라 폴더에는 PNG를 두지 않았다.

## 게시 전 사람이 반드시 확인할 것 (검증 통과 후)

1. **5장 "서툰 사람들의 이야기가 아니다".**
   - 연구진의 결론(6.1절: 일반적인 UI 설계로는 부족하다)에 기댄 문장이다.
   - 원인을 실험으로 나눠 검증한 것은 아니다. footnote에 그 점을 적었지만, 단정으로 읽히는지 본다.
2. **5장의 점선 열쇠.**
   - "화면의 열쇠 그림이 두 열쇠를 구분해 보여주지 않았다"는 그림이다.
   - 4.1절 인지적 워크스루, 곧 연구진 자신의 분석을 그렸다. 사용자 테스트 결과가 아니다.
3. **4장 "받은 쪽은 열 수 없는 메일이었다".**
   - 원문은 "자기 공개키로만 암호화했다"고 쓴다.
   - 팀원이 열 수 없었다는 것은 공개키 방식에서 따라 나오는 결과다. P2는 "팀원이 복호화할 수 없다"는 피드백도 받았다.
4. **1999년 연구라는 점.** 오늘날 메신저 이야기로 읽히지 않는지 본다. 1장 context_label과 캡션 첫 문장에 연도를 넣었다.
5. 원문 PDF 링크(usenix.org/legacy)가 열리는지 확인한다.
6. 남색 강조색과 해시태그 톤을 본다.

## 작업 파일 (지워도 됨)

`_fetch.py`, `_check_quotes.py`, `_build_content.py`, `_caption.txt`, `_candidates.json`, `_run_verify.py`, `_source.pdf`, `_source.txt`

- `content.json`은 `_build_content.py`가 만든다.
- 고칠 때는 이 스크립트나 `_caption.txt`를 고친 뒤 다시 실행하거나, `content.json`을 직접 고친다.
