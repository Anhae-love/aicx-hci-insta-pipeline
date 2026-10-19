# 2026-09-22 (화) — AI의 위로 메시지와 구체적인 대처법

**상태: `awaiting_human_review`** · 카드 6장 · 자가검사 오류 0 경고 0 · GPT attempt 1 revise → attempt 2 pass

> **먼저 읽을 것:** GPT는 두 번 모두 `source_url`(DOI)을 **직접 열지 못했다**(`url_reachable: unverified`).
> - attempt 1: 원문 대조를 못 하고 facts.json ↔ content.json의 **내적 정합성**만 확인했다(`title_matches`, `claims_traceable`도 `unverified`).
> - attempt 2: 맨체스터대 출판 기록과 ResearchGate의 **최종 논문 전문 미리보기**로 제목·Emotion 게재·표본 수·설계·주요 결과를 대조해
>   `title_matches: yes`, `claims_traceable: yes`를 냈다. 다만 이건 GPT가 찾은 **미리보기 페이지**이고, 나는 그 페이지를 열어 보지 못했다.
> - 내가 직접 한 원문 대조는 **OSF 원고(v5) 전문**이다(아래). **최종 출판 PDF를 사람이 열어 본 적은 아직 없다.**

## 오늘의 선택

- **주제:** 화 — 챗봇, 의인화, 감정, 사회적 상호작용
- **논문:** *A Digital Shoulder to Cry On: Understanding Why Large Language Models Can Be Effective in Extrinsic Interpersonal Emotion Regulation*
  Chen, Walker & López-Pérez · **Emotion 2026** (DOI 10.1037/emo0001712) · 무작위 배정 온라인 실험 5건
- **선정 문장:** 이 연구는 상상한 속상한 상황에서 AI와 사람이 쓴 위로 쪽지를 읽은 반응을 살펴봤고, 구체적인 대처법이 담긴 쪽지가 더 위로가 된다고 평가되는 경향을 발견했다. 하지만 실제 대화나 시간이 지난 뒤의 효과까지 확인한 것은 아니다.
- **이유:** 동료평가 게재 논문이고 원문 전문을 열 수 있었다. 헤드라인("AI 위로가 더 낫다")보다 재미있는 결과가 뒤에 있다. AI 우위의 이유가 공감 표현이 아니라 구체적인 대처법이었고, 그 대처법은 사람이 쓴 메시지에도 통했다. 집단 비교를 쓰지 않아도 된다.
- **오브젝트:** 위로 쪽지(직사각형+선). 과거 "두 개의 점", "시간 막대"와 겹치지 않는다. **강조색** `#2F5D8A`(최근 14일 안에 쓴 `#B5462A`, `#2E6F5E`와 다름).

## 원문 접근 — 사람이 알아야 할 것

- 본문은 **OSF 프리프린트 v5(2nd Revision 원고, 2026-05-19 등록)** 전문을 내려받아 대조했다. 5개 연구 구성과 표본 합계(279+390+196+188+180 = 1,233)가 Manchester 대학 보도자료와 맞는다.
- `facts.json`의 `source_quote` 15건은 **원문 텍스트와 스크립트로 자동 대조**했고 전부 일치했다.
- **최종 출판본(Emotion)은 열지 못했다.** doi.org → PsycNet은 "Loading…" 화면만 돌아왔다. 출판 과정에서 수치나 문구가 바뀌었을 수 있다.
- `source_url`은 내가 실제로 연 **OSF v5 DOI**(`https://doi.org/10.31234/osf.io/nt5d8_v5`)다. 게재 사실과 출판 DOI는 `facts.json`의 `venue_checked`에 있다. `is_preprint`는 `false`(게재됨).
- 시도 중 `curl` 직접 호출은 권한이 거부돼 쓰지 않았다. 대신 WebFetch가 받아 둔 docx를 python으로 풀어 텍스트를 뽑았다.

## 탈락한 후보 (10건 검토, 사유는 `content.json`의 `candidates`)

| 후보 | 사유 |
|---|---|
| Anthropomorphism in AI Companion Communities (arXiv 2606.30942) | 프리프린트, 핵심이 연령·성별 비교라 1장 훅 불가 |
| Teens' Overreliance on Companion AI Chatbots (arXiv 2609.14843) | CHI 2027 심사 중 프리프린트, 10대·의존 주제라 낙인 우려 |
| When Chatbots Accommodate (EMNLP 2026 Findings) | 사람의 행동이 아니라 챗봇 응답 감사 |
| Does My Chatbot Have an Agenda? (CHI 2026) | 22명 질적 연구, 카드에 놓을 반전이 약함 |
| Emotional Manipulation by AI Companions (2025) | 프리프린트, 최근성 밀림, 의존 주장 |
| Longitudinal RCT of Companion Chatbot Use (2025) | 핵심이 매개효과라 용어 없이 설명 어려움 |
| Sycophantic AI decreases prosocial intentions (Science) | **403으로 원문 못 엶.** 월요일 주제에 더 가까움 |
| Chatbot Anthropomorphism & Prosocial Behavior (PACM HCI) | **403으로 원문 못 엶** |
| Affective Use and Emotional Well-being on ChatGPT (2025) | 최근성 밀림, 검색 요약만 확인 |

> 정직하게 밝힘: 위 목록 중 앞의 6건은 초록 페이지까지 열었고, 마지막 3건은 검색 결과 요약이나 접근 거부로 **초록 수준도 못 봤다**. 탈락 사유는 그 범위 안에서 쓴 것이다.
> 접근이 막힌 Science 논문은 원문을 열 수 있게 되면 월요일 후보로 다시 볼 만하다(3개 사전등록 실험, N = 2405로 검색 결과에 나옴).

## GPT가 지적했고 내가 고친 것

**attempt 1 — revise (blocker 2, major 1, 474초)**

1. **[blocker] 2장: 같은 참가자가 두 쪽지를 나란히 읽은 것처럼 보임.** 메시지 출처는 참가자 간 요인이다.
   → hero를 "서로 다른 참가자가 읽고 느낌을 매겼다"로, support·footnote·object_state를 GPT가 준 `fix`대로 교체.
   그림에는 두 쪽지 사이에 **점선 구분선**을 넣어 서로 다른 집단임을 그렸다(GPT 제안에 없는 내 보완).
2. **[blocker] 캡션: 1,233명 전원이 쪽지를 읽은 것처럼 씀.** 1,233명에는 위로 글을 쓴 연구 1a 참가자 279명이 포함된다.
   → GPT의 `fix` 문단으로 교체("첫 연구의 참가자들은 위로 문구를 작성했고…", "연구 1b에서는 쪽지 출처를 알리지 않았다").
3. **[major] 4장: "더 위로가 됐다"가 실제 감정 효과처럼 읽힘.** 측정값은 '위로가 된다고 평정한 것'이다.
   → hero를 "구체적인 방법이 담긴 / 쪽지가 더 위로로 느껴졌다"로 교체.

**attempt 2 — pass (minor 1, 568초)**

4. **[minor] 5장 footnote: "연구 3b는 출처 차이가 뚜렷하지 않았다"가 3b 전체 결과로 읽힘.** 원문상 유의하지 않은 것은 지지감 평정이고,
   슬픔 상황의 감정 변화에는 출처×대처법 상호작용이 있었다(대처법의 이득 중 행복 증가·분노 감소는 LLM 메시지에서만 나타남).
   → "연구 3b의 **지지감 평가는** 출처 차이가 뚜렷하지 않았다"로 범위를 좁힘.
   **이 수정은 attempt 2 pass 이후에 했고 재검증은 하지 않았다.** 뜻을 넓히는 게 아니라 좁히는 수정이고 GPT 제안 방향이라 판단했다.

## 자체 검사가 먼저 잡은 것

- 첫 자가검사에서 "뚜렷한 **차이가 없었다**"가 3장 support와 캡션에서 `null_result` 게이트에 걸렸다. "차이를 확인하지 못했다"로 교체.
  `facts.json`에 `null_result`가 5건 있어서 걸린 것이다(슬픔 상황, 감정 인정 표현, 출처 효과, 출처 판단, 저자 서술).

## 지적받았지만 고치지 않은 것

없다. 4건 모두 반영했다. 다만 **GPT가 확인하지 못한 것**이 있다:

- DOI 페이지 접근 실패(`url_reachable: unverified`)는 내가 고칠 수 있는 지적이 아니라 환경 한계다. `source_url`을 바꿔도 같은 결과일 가능성이 크다.

## 게시 전 사람이 반드시 확인할 것

- [ ] **최종 출판본을 열어 표본(1b 390, 2 196, 3b 180)과 결과 방향이 원고와 같은지** — 가장 중요. 특히 5장 footnote의 "연구 3b 지지감 평가" 문장
- [ ] 캡션 마지막 줄 "출처: Chen, Walker & López-Pérez (2026), Emotion" — 링크가 없다. 필요하면 출판 DOI(10.1037/emo0001712)를 붙일지 결정
- [ ] **4장 "기분 변화" 문구.** 연구 2에서 감정 인정 표현은 *기분 변화*에는 유의한 영향이 없었지만, 분노 시나리오의 '지지받는 느낌' 평정에는 영향이 있었다.
      카드는 '기분 변화'로 한정했으나, 독자가 "공감은 소용없다"로 읽지 않는지 확인
- [ ] **3장에서 AI 쪽지를 파랗게 채운 것이 '우월'로 읽히지 않는지.** 5장이 이 오해를 막도록 설계했지만 눈으로 재확인
- [ ] 5장 그림은 **개념도**다(라벨에 표기). 점선 글줄은 "길이를 맞추면 줄어드는 부분"의 뜻이고 실제 단어 수 비율이 아니다
- [ ] 1장 훅("누가 썼을까")이 연구 초점을 오해시키지 않는지. 이 연구의 초점은 작성자 맞히기가 아니라 위로 평가다
- [ ] 6장 질문은 편집자의 것임이 footnote에 표기돼 있다
- [ ] 해시태그(#HCI #인간과AI #챗봇 #AI위로 #감정 #UX리서치 #디지털행동 #인터랙션디자인 #연구노트 #AI심리)
- [ ] 3장 support가 두 줄로 넘어가 "못했다."가 한 줄에 홀로 남는다. 문구 수정은 재검증 범위라 그대로 뒀다. 거슬리면 손으로 줄이기

## 기록상 어긋난 것 (사소함)

- `PROGRESS.log`의 2단계 줄에 "findings 14건"이라 적혀 있으나, 3장 그림 근거를 위해 **F15를 추가해 최종은 15건**이다(facts.json이 맞다).
- `PROGRESS.log`의 0·3단계 시각은 시계를 다시 확인하지 않고 쓴 근사값이다(1단계 이후 시각은 실제 시계 기준).
- `state/last_run.json`은 어제 실행 값(`no_output`) 그대로다. 이 파일은 `run_daily.ps1`이 갱신하므로 손대지 않았다.
