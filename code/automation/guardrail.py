#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사람 부재 가드레일 — 승인이 늦어도 파이프라인이 '대기'로 영원히 멈추지 않게 한다.

문제: 매일 새벽 콘텐츠는 `awaiting_human_review` 로 멈춰 사람을 기다린다.
사람이 그날 못 보면 그 상태로 계속 머문다(= stay 상태로 삭는다).

규칙: 어떤 콘텐츠가 `awaiting_human_review` 인데
  - 그 날짜의 마감시각(기본 당일 21:00)이 지났고
  - decisions.jsonl 에 그 folder 에 대한 사람 결정이 **없으면**
→ STATUS 를 `expired_no_review` 로 바꾸고, decisions.jsonl 에
  {decision:"expired", reason:"21시까지 미검토 — 자동 보류"} 한 줄을 남긴다.
이러면 '사람이 보고 결정한 것'과 '시간이 지나 자동 보류된 것'이 구분되어 쌓인다.

호출 (매일, run_daily 와 별도로 저녁에 한 번 돌리는 게 이상적):
    python code/automation/guardrail.py            # 기본 마감 21:00
    python code/automation/guardrail.py --deadline 21:00
    python code/automation/guardrail.py --dry-run  # 바꾸지 않고 대상만 출력

처리 결과를 종료코드로 알린다: 0=처리할 것 없음/정상, 2=만료 처리한 항목 있음.
"""
import argparse, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))

def project_root():
    cr = os.path.dirname(HERE)
    return os.path.dirname(cr) if os.path.basename(cr) == "code" else cr

def paths():
    root = project_root()
    data = os.path.join(root, "data")
    base = data if os.path.isdir(data) else root
    return {
        "output": os.path.join(base, "output"),
        "state":  os.path.join(base, "state"),
    }

def read_jsonl(p):
    rows = []
    if os.path.isfile(p):
        for line in open(p, encoding="utf-8-sig"):
            line = line.strip()
            if line:
                try: rows.append(json.loads(line))
                except Exception: pass
    return rows

def folder_date(folder):
    import re
    m = re.match(r"(\d{8})", folder)
    if not m: return None
    s = m.group(1)
    try: return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except Exception: return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deadline", default="21:00", help="당일 마감시각 HH:MM (기본 21:00)")
    ap.add_argument("--within-days", type=int, default=2,
                    help="최근 N일 이내 콘텐츠만 대상 (기본 2 = 어제·오늘). 오래된 과거 것은 건드리지 않는다.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    try:
        hh, mm = [int(x) for x in a.deadline.split(":")]
    except Exception:
        print("잘못된 --deadline 형식. HH:MM 로.", file=sys.stderr); return 1

    P = paths()
    now = datetime.datetime.now()

    decided_folders = {d.get("folder") for d in read_jsonl(os.path.join(P["state"], "decisions.jsonl"))}

    if not os.path.isdir(P["output"]):
        print("output 폴더 없음 — 처리할 것 없음"); return 0

    expired = []
    for folder in sorted(os.listdir(P["output"])):
        fpath = os.path.join(P["output"], folder)
        if not os.path.isdir(fpath) or folder.startswith("_"):
            continue
        sf = os.path.join(fpath, "STATUS")
        if not os.path.isfile(sf):
            continue
        status = open(sf, encoding="utf-8-sig").read().strip()
        if status != "awaiting_human_review":
            continue
        if folder in decided_folders:
            continue  # 사람이 이미 결정함

        d = folder_date(folder)
        if d is None:
            continue
        # 최근 N일 이내만 — 오래 전 미결정 콘텐츠는 가드레일이 건드리지 않는다
        age_days = (now.date() - d).days
        if age_days < 0 or age_days >= a.within_days:
            continue
        deadline = datetime.datetime(d.year, d.month, d.day, hh, mm)
        if now < deadline:
            continue  # 아직 마감 전 — 사람 시간 남았다

        expired.append((folder, fpath, sf, d))

    if not expired:
        print("만료 대상 없음 — 사람 검토 시간이 남았거나 이미 결정됨"); return 0

    print(f"만료 처리 대상 {len(expired)}건 (마감 {a.deadline} 지남, 미검토):")
    for folder, fpath, sf, d in expired:
        print(f"  - {folder}")
        if a.dry_run:
            continue
        # STATUS 교체
        with open(sf, "w", encoding="utf-8") as f:
            f.write("expired_no_review\n")
        # decisions.jsonl 에 자동 보류 기록
        rec = {
            "folder": folder, "date": d.isoformat(),
            "decision": "expired",
            "reason": f"{a.deadline}까지 미검토 — 자동 보류 (사람 부재 가드레일)",
            "decided_at": now.isoformat(timespec="seconds"),
        }
        with open(os.path.join(P["state"], "decisions.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if a.dry_run:
        print("(dry-run: 아무것도 바꾸지 않음)")
        return 0
    print("처리 완료 — STATUS=expired_no_review, decisions.jsonl 에 기록")
    return 2

if __name__ == "__main__":
    sys.exit(main())
