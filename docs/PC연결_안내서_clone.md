# PC 연결 안내서 — 새 폴더로 clone (1회만)

> 목표: PC를 저장소에 연결해서, **매일 새벽 파이프라인이 끝나면 대시보드가 폰에서 자동 갱신**되게 한다.
> 방식: 저장소를 새 폴더로 clone → 기존 폴더에서 못 올라간 파일(resvg.exe)만 복사 → 스케줄러를 새 폴더로.

바탕화면 프로젝트: `C:\Users\CXlab\Desktop\개인 프로젝트 야르~\인스타 프로젝트 야르~` (이게 **기존 폴더**)

---

## 한눈에 — 왜 이렇게 하나

- 저장소엔 **완성된 code/data 분리 구조 + 오늘 고친 코드**가 다 있다. clone 하면 그게 그대로 PC에 생긴다.
- 기존 폴더는 **평면 구조 + .git 없음**이라 자동 push가 안 됐다. 그래서 새로 clone 한 폴더를 쓴다.
- 딱 하나, **`resvg.exe`(카드 렌더용 3.4MB)**는 공개 저장소라 안 올렸다. 그것만 기존 폴더에서 복사한다.
- 기존 폴더는 **지우지 말고 백업으로 남겨둔다.**

---

## STEP 1 — 새 폴더로 clone

PowerShell을 열고 (git 로그인은 이미 돼 있다고 하셨으니 그대로):

```powershell
cd "C:\Users\CXlab\Desktop\개인 프로젝트 야르~"
git clone https://github.com/Anhae-love/aicx-hci-insta-pipeline.git insta-pipeline
cd insta-pipeline
```

→ `개인 프로젝트 야르~\insta-pipeline\` 에 code/ data/ docs/ 가 생긴다.

---

## STEP 2 — resvg.exe 복사 (렌더에 필수, 저장소엔 없음)

```powershell
# 기존 폴더의 bin 을 새 폴더 code/automation/bin 으로
$old = "C:\Users\CXlab\Desktop\개인 프로젝트 야르~\인스타 프로젝트 야르~\automation\bin"
New-Item -ItemType Directory -Force -Path ".\code\automation\bin" | Out-Null
Copy-Item "$old\resvg.exe" ".\code\automation\bin\resvg.exe"
Test-Path ".\code\automation\bin\resvg.exe"   # True 나오면 성공
```

> render.py 는 `code/automation/bin/resvg.exe` 를 자기 위치 기준으로 찾으므로 이 경로면 된다.

---

## STEP 3 — config.json 경로 확인 (claude·codex 실행파일)

새 폴더의 `code\automation\config.json` 을 열어 `claude_path`, `codex_path` 가
지금 PC에 맞는지 본다. 기존 폴더에서 돌아갔다면 같은 값이라 그대로면 된다.
(버전 폴더가 바뀌었으면 비워 두면 run_daily.ps1 이 자동 탐색한다.)

---

## STEP 4 — 한 번 시험 실행 (DryRun — 카드 렌더 전까지만)

```powershell
cd "C:\Users\CXlab\Desktop\개인 프로젝트 야르~\insta-pipeline"
.\code\automation\run_daily.ps1 -DryRun
```

- 오류 없이 끝나고, `data\logs\` 에 오늘 로그가 생기면 경로 재배치가 성공한 것이다.
- `.ps1` 실행이 막히면(실행 정책): 관리자 PowerShell에서
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 한 번.

---

## STEP 5 — 스케줄러를 새 폴더로 (기존 작업 교체)

기존 작업 스케줄러(새벽 3시)는 **기존 폴더**를 가리키고 있다. 새 폴더로 바꾼다:

```powershell
cd "C:\Users\CXlab\Desktop\개인 프로젝트 야르~\insta-pipeline"
.\code\automation\setup_task.ps1   # 작업 등록/갱신 (내부에서 새 폴더 기준으로 잡음)
```

> setup_task.ps1 이 기존과 같은 작업 이름("HCI 인스타 일일 콘텐츠")을 쓰면 덮어쓴다.
> 등록 후 작업 스케줄러에서 **기존 폴더를 가리키던 옛 작업이 남아있지 않은지** 한 번 확인.
> (옛 작업이 남아 둘 다 돌면 같은 날 두 번 만들 수 있다.)

---

## STEP 6 — 자동 push가 되는지 확인

위 DryRun 이 아니라 **진짜 실행**이 한 번 끝나면(또는 내일 새벽),
run_daily.ps1 끝의 자동 push 블록이:
1. `python code/automation/build_manifest.py . docs` 로 manifest 재생성
2. `git add docs data` → commit → push
3. Pages 자동 재배포 → 폰에서 갱신

을 한다. 로그(`data\logs\<날짜>.log`)에 "대시보드 push 완료" 가 찍히면 성공.

안 되면 로그에서 git 줄을 본다:
- "`.git 이 없다`" → clone 이 아니라 복사로 가져왔을 때. STEP 1 로 clone 다시.
- git 인증 오류 → PowerShell에서 `git push` 한 번 수동 실행해 자격증명 캐시.

---

## STEP 7 — 폰에서 보기 (이미 됨)

대시보드는 이미 라이브다: https://anhae-love.github.io/aicx-hci-insta-pipeline/
이 주소를 **폰 홈화면에 추가**하면 앱처럼 열린다. 매일 새벽 뒤 열면 밤새 만든 카드가 떠 있다.

---

## 반려를 눌렀을 때 — 기획실로 전달되는 법 (오늘 새로 만든 것)

대시보드는 정적 페이지라 반려를 **자동 저장하지 못한다.** 그래서 이렇게 연결된다:

1. 대시보드에서 **반려** → 사유 입력 → "결정 복사" 누르면 결정 JSON 이 클립보드에 담긴다.
2. PowerShell에서 한 줄:
   ```powershell
   cd "C:\Users\CXlab\Desktop\개인 프로젝트 야르~\insta-pipeline"
   python code\automation\collect_decision.py --clipboard
   ```
   → `data\state\decisions.jsonl` 에 기록된다.
3. 다음 새벽 **기획실(pipeline_prompt 0단계)이 최근 30일 반려 사유를 읽고** 오늘 기획에 먼저 반영한다.
4. 대시보드 "측정 루프" 섹션에 승인율·최근 반려 사유가 쌓여 보인다.

> 더 편하게: 결정 JSON 을 `data\state\decisions.inbox\` 에 아무 이름 `.json` 으로 저장해 두면,
> 다음 새벽 run_daily 가 `--inbox` 로 자동 흡수한다. (매일 PowerShell 칠 필요 없음)

---

## 기존 폴더는?

지우지 말 것. 백업이다. 새 폴더가 며칠 잘 도는 걸 확인한 뒤,
기존 폴더를 `_백업_구버전` 등으로 이름만 바꿔 치워두면 된다.
