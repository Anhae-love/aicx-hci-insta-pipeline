# 노션 「YYYY-MM-DD · 측정 기록」 페이지 양식

예약 작업이 이 양식대로 노션 페이지를 만든다. 숫자는 전부 `data/metrics/measure_summary.json`에서 가져오고,
지어내지 않는다. 값이 없으면 "확인 전"이라고 쓴다.

- 위치: AICX 수업 페이지(3fe5908cd71680d68d16c68e07cbe63c)의 하위 페이지
- 제목: `YYYY-MM-DD · 측정 기록` (업데이트한 날짜, 한국 시간)
- 같은 날짜 페이지가 이미 있으면 새로 만들지 않고 그 페이지를 고친다(맨 위 "마지막 갱신" 줄도 바꾼다).
- 지난 날짜 페이지는 절대 고치지 않는다.
- 개인정보·비밀키·논문 원문·AI 대화 전체는 넣지 않는다.

---

마지막 갱신: {KST 시각} · 자동 생성(예약 작업) · 근거: 저장소 `data/metrics/measure_summary.json`

## 1. 이번에 실제로 해본 작업
- 목적: 매일 새벽 자동으로 만든 카드뉴스 초안을 사람이 빠짐없이 검토할 수 있게 준비한다.
- 이번 범위: {latest.date} 새벽 실행 1회분 + {period.start}~{period.end} 누적({period.days}일)
- 도구: 기획·카피 Claude Code / 교차검증 Codex(GPT) / 렌더 render.py / 업로드 07:10 예약 작업 / 가드레일 21:00 / 지표 measure_summary.py

## 2. 무엇을 보고 잘됐는지 판단하나요?
- 지표: 정상적으로 열리는 이미지 수 / 만들기로 한 이미지 수 (하루 6장)
- 보조: 카드가 나온 날 수 / 전체 날짜 수, 사람 결정(승인·반려·보류)

## 3. 어떻게 세나요?
- PNG를 Pillow로 끝까지 열어 오류가 없으면 '열림'. 로그·STATUS 문구는 세지 않는다.
- 분모 두 가지: 달력 날짜 기준(날짜 수×6) / 게이트 통과 기준(카드를 만들기로 한 날만)
- 명령: `python code/tools/measure_summary.py data`

## 4. 결과와 근거
- 오늘({latest.date}): STATUS {latest.status} · 열린 카드 {latest.opened}/6 · 사람 결정 {latest.decision 또는 "아직 없음"}
- 누적 달력 기준: {calendar.opened}/{calendar.planned} ({calendar.rate %})
- 누적 게이트 기준: {gate_passed.opened}/{gate_passed.planned} ({gate_passed.rate %})
- 카드가 나온 날: {days_with_cards}/{period.days}일 · 상태별: {status_counts}
- 누락된 날짜: {missing_dates 또는 "없음"}
- 사람 결정: 승인 {decisions.approved} · 반려 {decisions.rejected} · 자동 보류 {decisions.expired} · 결정 대기 {decisions.undecided_awaiting}
- 최근 반려 사유: {recent_rejects 또는 "없음"}
- 최근 7일 표: 날짜 / STATUS / 열린 장 수 / 사람 결정 (last_7_days)
- 근거 링크: 저장소 https://github.com/Anhae-love/aicx-hci-insta-pipeline , 대시보드 https://anhae-love.github.io/aicx-hci-insta-pipeline/

## 5. 이 값만으로는 알 수 없는 것
- 이미지가 열려도 내용이 맞는지는 모른다(내용 판단은 사람 결정·반려 사유로 따로 본다).
- 게시 후 반응(조회·저장·공유)은 아직 재지 않는다.
- {이번 갱신에서 새로 드러난 한계가 있으면 한 줄, 없으면 이 줄 생략}

## 6. 다음에 바꾸거나 더 확인할 것
- {지난 측정 기록과 비교해 달라진 점 한 줄: 예) 누락 날짜 증가, 반려 사유 반복, 보류 증가}
- {그래서 다음에 확인할 것 한 줄}
