#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사람이 대시보드에서 내린 승인/반려 결정을 data/state/decisions.jsonl 로 모은다.

대시보드(정적 GitHub Pages)는 서버에 쓸 수 없다. 그래서 결정은 이렇게 들어온다:

  방법 A) 클립보드:
     대시보드에서 "결정 복사"를 누르면 결정 JSON 이 클립보드에 담긴다.
     그 상태로:  python code/automation/collect_decision.py --clipboard
     → 클립보드의 JSON 을 decisions.jsonl 에 한 줄 추가한다.

  방법 B) 인박스 폴더:
     결정 JSON 을 data/state/decisions.inbox/ 에 아무 이름의 .json 으로 저장해 두면,
     다음 실행 때(또는 아래 명령으로) 자동으로 합쳐진다:
     python code/automation/collect_decision.py --inbox

  방법 C) 직접 전달:
     python code/automation/collect_decision.py --json '{"folder":"...","decision":"rejected","reason":"..."}'

run_daily.ps1 은 매일 --inbox 를 한 번 호출해, 밤새 사람이 떨어뜨려 둔 결정을 흡수한다.

중복은 (folder, decision, decided_at) 기준으로 막는다. 같은 결정을 두 번 넣어도 한 줄만 남는다.
"""
import argparse, json, os, sys, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))

def project_root():
    # code/automation → code → <root>.  평면 구조면 <root> 자신.
    code_root = os.path.dirname(HERE)
    if os.path.basename(code_root) == "code":
        return os.path.dirname(code_root)
    return code_root

def state_dir():
    root = project_root()
    new = os.path.join(root, "data", "state")
    old = os.path.join(root, "state")
    return new if os.path.isdir(new) else (old if os.path.isdir(old) else new)

def normalize(rec):
    """대시보드가 주는 결정 JSON 을 표준 형태로."""
    if not isinstance(rec, dict):
        return None
    folder = rec.get("folder")
    decision = rec.get("decision")
    if not folder or decision not in ("approved", "rejected"):
        return None
    return {
        "folder": folder,
        "date": rec.get("date", ""),
        "decision": decision,
        "reason": (rec.get("reason") or "").strip(),
        "decided_at": rec.get("decided_at") or datetime.datetime.now().isoformat(timespec="seconds"),
    }

def load_existing(path):
    keys = set()
    rows = []
    if os.path.isfile(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                rows.append(r)
                keys.add((r.get("folder"), r.get("decision"), r.get("decided_at")))
            except Exception:
                pass
    return rows, keys

def append_records(records):
    sd = state_dir()
    os.makedirs(sd, exist_ok=True)
    path = os.path.join(sd, "decisions.jsonl")
    _, seen = load_existing(path)
    added = 0
    with open(path, "a", encoding="utf-8") as f:
        for rec in records:
            r = normalize(rec)
            if not r:
                continue
            k = (r["folder"], r["decision"], r["decided_at"])
            if k in seen:
                continue
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            seen.add(k)
            added += 1
    return path, added

def from_clipboard():
    try:
        import subprocess
        # Windows: powershell Get-Clipboard
        out = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                             capture_output=True, text=True, timeout=10)
        return out.stdout
    except Exception as e:
        print(f"클립보드를 읽지 못했다: {e}", file=sys.stderr)
        return ""

def parse_any(text):
    """텍스트에서 JSON 객체(들)을 느슨하게 파싱. 한 개여도 리스트로 돌려준다."""
    text = (text or "").strip()
    if not text:
        return []
    # 통째로 JSON 이면
    try:
        v = json.loads(text)
        return v if isinstance(v, list) else [v]
    except Exception:
        pass
    # 여러 줄에 객체가 흩어져 있으면 중괄호 블록을 긁는다
    out = []
    depth = 0; start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try: out.append(json.loads(text[start:i+1]))
                except Exception: pass
                start = None
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clipboard", action="store_true", help="클립보드의 결정 JSON 을 흡수")
    ap.add_argument("--inbox", action="store_true", help="data/state/decisions.inbox/*.json 을 흡수")
    ap.add_argument("--json", help="결정 JSON 문자열을 직접 전달")
    a = ap.parse_args()

    records = []
    if a.json:
        records += parse_any(a.json)
    if a.clipboard:
        records += parse_any(from_clipboard())
    if a.inbox:
        inbox = os.path.join(state_dir(), "decisions.inbox")
        if os.path.isdir(inbox):
            for p in sorted(glob.glob(os.path.join(inbox, "*.json"))):
                try:
                    records += parse_any(open(p, encoding="utf-8").read())
                    os.remove(p)  # 흡수한 건 치운다
                except Exception as e:
                    print(f"인박스 {p} 처리 실패: {e}", file=sys.stderr)

    if not any([a.json, a.clipboard, a.inbox]):
        ap.print_help()
        return 0

    path, added = append_records(records)
    print(f"결정 {added}건 추가 → {path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
