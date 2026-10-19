# 2026-10-05 (월) — AI 제안마다 이유를 쓰게 한 실험

**상태: awaiting_human_review** · GPT 교차검증 attempt 1에서 pass (지적 0건, checklist fail 0) · 카드 6장 렌더 완료

## 오늘 고른 주제와 이유

**Think Before You Accept: Can Written Justification Reduce Uncritical Uptake of AI Writing Suggestions?**
Tao, Meyer, Kizilcec (Cornell · Univ. of Vienna) — https://arxiv.org/abs/2609.23936 (2026-09-20, 프리프린트)

- 월요일 주제(AI 신뢰·의존·판단)에 맞고, 'AI 수정 제안을 수락 버튼으로 받는다'는 장면이 누구에게나 익숙하다.
- 무작위 배정 실험(129명)이고, 핵심 결과가 퍼센트라 통계용어 없이 설명된다. 틀린 제안 수락률이 체크만 65%, 이유 쓰기 41%였다.
- 반전과 오해 방지 재료가 원문에 분명히 있다. 이유 글은 피상적인 게 많았다. 가짜 이론을 '가짜'라고 짚은 답은 14건이었다. 효과가 시간·수고 때문인지는 가르지 못했다.
- 오브젝트는 **체크박스**(사각형·체크·이유 줄). 과거 오브젝트와 겹치지 않는다. 강조색은 **#8A5A2B**(갈색)로, 최근 14일 색과 겹치지 않는다.

선정문: 이 연구는 AI가 내놓은 좋은 수정 제안과 일부러 틀리게 만든 제안을 학생들이 얼마나 받아들이는지 살펴봤다. 그리고 제안마다 이유를 한 줄씩 쓰게 한 쪽에서 틀린 제안을 덜 받아들이는 경향을 발견했다. 하지만 그 효과가 이유를 따져서인지 쓰는 데 든 시간·수고 때문인지, 고친 글이 실제로 나아졌는지, 실제 AI 글쓰기 도구에서도 그런지까지 확인한 것은 아니다.

## 탈락한 후보 (12건, 사유는 content.json candidates에도 있음)

| 후보 | 탈락 사유 |
|---|---|
| People escalate against a competitor labelled human… (2609.21439) | **2순위.** 반전은 강하지만 '전액 지불 경매' 구조를 카드 6장에 정확히 설명하기 어렵다 |
| Referential Uncertainty in Human–AI Collaboration (2609.39518) | 결과 절반이 모델 보정 지표(ECE·AUROC) |
| Annie, Are You Okay? (2609.24644) | 10/01 후보로 검토됨. 주식 과제이고, 전문성 집단 낙인 위험 |
| Designing Against Deskilling (2609.20143) | 핵심 결과가 오즈비뿐이고 분수 과제 |
| When the AI Leaves the Tailorshop (2610.00163) | 가상 공장 시뮬레이션이고 결과가 채점 기준마다 엇갈림 |
| Available but Unclaimed (2609.16793) | 퍼즐 과제이고 단일 오브젝트화가 어려움 |
| LLMs in Peer Review at ICML 2026 (2609.19420) | 학회 심사자라는 좁은 집단이고 정책 효과는 거의 0 |
| AI-Generated Email Drafts… (2609.26403) | 일본·미국 국가 비교가 중심이라 집단 비교 규칙에 걸림 |
| Does AI Save Time on Product Design? (2609.26725) | 상용 도구 평가 성격이고 9/21 게시물과 겹침 |
| Temporal Fingerprint (2609.17883) | 탐지 기술 중심이고 위임은 시뮬레이션 |
| Ownership in AI-Assisted Everyday Tasks (2609.20658) | 탐색적 질적 설문이라 수치와 반전이 약함 |
| Confident, Not Wiser (2609.31095) | 10/04 후보로 검토됨. 능력 집단 비교 |

## GPT가 지적했고 고친 것

없음. attempt 1에서 지적 0건으로 pass했다.
GPT 요약: "가장 큰 오해 가능성은 41%를 실제 수락률로 받아들이는 것이지만, 4장 각주와 캡션이 이를 충분히 차단한다."

(자가검사 단계에서 render.py가 캡션의 '통계적으로 유의한 차이 없음'을 null_result 금칙어로 막았다. '차이는 통계적으로 유의하지 않음'으로 고쳤다.)

## GPT가 지적했지만 고치지 않은 것

없음.

## 렌더 후 수정 (재검증 불필요한 좌표 변경)

- 3장: 이유 줄이 상자 사이를 잇는 연결선처럼 보였다. 각 상자 **아래**로 옮겼다(좌표만 바꿈). 대체 텍스트의 '옆에'도 '아래에'로 고쳤다.

## 게시 전 사람이 반드시 확인할 것

1. **원문 링크**(https://arxiv.org/abs/2609.23936)가 열리는지, 그 사이 학회·저널 게재가 확인됐는지. 확인되면 캡션의 프리프린트 문구를 고친다.
2. **4장 41%**가 '실제 AI 제안의 41%가 틀리다'나 '사람들이 실제로 41%를 받아들인다'로 읽히지 않는지. footnote 두 줄이 폰에서 보이는지 확인한다. 실험은 제안 절반을 일부러 틀리게 만든 구성이었다.
3. **좋은 제안 수락 81%·86%**: 원문은 순서를 명시하지 않는다(문맥상 체크만 81, 이유 쓰기 86으로 추정). 카드에는 어느 쪽이 높았는지 쓰지 않았다. 순서를 붙이고 싶다면 원문 그림 2를 직접 확인한다.
4. **5장 예시 번역**: 'it's reasonable'은 '합리적이네', 'Not really necessary'는 '별로 필요 없음'으로 옮겼다. 뉘앙스가 맞는지 본다.
5. 캡션의 **'미국 코넬대 등 연구진'**은 저자 소속 기준이다. 실험이 이뤄진 수업은 원문에 'a U.S. university'로만 적혀 있다.
6. 1장 hook '몇 개나 받을까'는 질문형이다. 8개는 실험 설정이고 2장에서 바로 풀린다.
7. 강조색 **#8A5A2B**(갈색)가 강조로 충분히 읽히는지, 해시태그 톤.

## 파일

- `facts.json`: findings 14건, null_result 2건(F2 좋은 제안 수락, F6 전부 수락 비율 p=.068). `_check_quotes.py`로 원문 대조했고 17건 모두 일치한다.
- `_source.txt` / `_source.html`: arXiv HTML 원문
- `content.json` ← `_build_content.py`로 생성
- `verdict.json`: pass (attempt 1)
- `slide_1~6.png/svg`, `caption.txt`, `alt_texts.txt`
