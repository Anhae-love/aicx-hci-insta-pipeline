#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""노션 「YYYY-MM-DD · 측정 기록」 페이지를 채울 숫자를 한 번에 계산한다.

개인과제 6칸 양식(목적·지표·세는 법·결과·한계·다음 행동)에 들어갈 값만 만든다.
로그의 성공 문구가 아니라 실제 PNG를 열어서 센다(check_images.py 와 같은 기준).

사용: python code/tools/measure_summary.py data [--start 2026-09-21] [--today 2026-10-20]
결과: data/metrics/measure_summary.json  (+ 같은 내용을 stdout)
"""
import argparse, datetime, json, os, re
from PIL import Image

NO_CARD = {"rejected", "verify_failed", "no_output", "needs_human"}


def can_open(p):
    try:
        with Image.open(p) as im:
            im.load()
        return True
    except Exception:
        return False


def read(p, default=""):
    try:
        return open(p, encoding="utf-8-sig").read().strip()
    except Exception:
        return default


def jsonl(p):
    rows = []
    for line in read(p).splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data", nargs="?", default="data")
    ap.add_argument("--start", default="2026-09-21")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    out_dir = os.path.join(a.data, "output")
    by_date = {}
    for folder in sorted(os.listdir(out_dir)):
        m = re.match(r"(\d{4})(\d{2})(\d{2})_", folder)
        if not m or not os.path.isdir(os.path.join(out_dir, folder)):
            continue
        d = f"{m[1]}-{m[2]}-{m[3]}"
        fp = os.path.join(out_dir, folder)
        status = read(os.path.join(fp, "STATUS"), "unknown")
        opened = sum(can_open(os.path.join(fp, f"slide_{i}.png")) for i in range(1, 7)
                     if os.path.exists(os.path.join(fp, f"slide_{i}.png")))
        by_date[d] = {"folder": folder, "status": status, "opened": opened}

    decisions = {}
    for r in jsonl(os.path.join(a.data, "state", "decisions.jsonl")):
        decisions[r.get("folder")] = r  # 같은 폴더면 마지막 결정이 이긴다

    start = datetime.date.fromisoformat(a.start)
    today = datetime.date.fromisoformat(a.today)
    days, opened_total = [], 0
    d = start
    while d <= today:
        k = d.isoformat()
        row = by_date.get(k)
        if row:
            dec = decisions.get(row["folder"], {})
            days.append({"date": k, **row, "decision": dec.get("decision", ""), "reason": dec.get("reason", "")})
            opened_total += row["opened"]
        else:
            days.append({"date": k, "folder": "", "status": "missing", "opened": 0, "decision": "", "reason": ""})
        d += datetime.timedelta(days=1)

    n = len(days)
    with_cards = [x for x in days if x["opened"] > 0]
    gate_planned = sum(6 for x in days if x["status"] not in NO_CARD and x["status"] != "missing")
    cnt = lambda key, val: sum(1 for x in days if x[key] == val)

    tests = []
    it = os.path.join(a.data, "image_tests")
    if os.path.isdir(it):
        for t in sorted(os.listdir(it)):
            rp = os.path.join(it, t, "image_test_report.json")
            if os.path.exists(rp):
                rep = json.load(open(rp, encoding="utf-8"))
                files = [f["file"] for f in rep.get("files", [])]
                tests.append({"date": t, "tool": rep.get("tool"), "planned": rep.get("planned", len(files)),
                              "opened": sum(can_open(os.path.join(it, t, f)) for f in files),
                              "human_check": rep.get("human_check", [])})

    latest = days[-1] if days else None
    res = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "period": {"start": a.start, "end": a.today, "days": n},
        "metric": "정상적으로 열리는 이미지 수 / 만들기로 한 이미지 수",
        "calendar": {"opened": opened_total, "planned": n * 6,
                     "rate": round(opened_total / (n * 6), 4) if n else None},
        "gate_passed": {"opened": opened_total, "planned": gate_planned,
                        "rate": round(opened_total / gate_planned, 4) if gate_planned else None},
        "days_with_cards": len(with_cards),
        "status_counts": {s: cnt("status", s) for s in sorted({x["status"] for x in days})},
        "missing_dates": [x["date"] for x in days if x["status"] == "missing"],
        "decisions": {"approved": cnt("decision", "approved"), "rejected": cnt("decision", "rejected"),
                      "expired": cnt("decision", "expired") + cnt("status", "expired_no_review"),
                      "undecided_awaiting": sum(1 for x in days if x["status"] == "awaiting_human_review" and not x["decision"])},
        "recent_rejects": [{"date": x["date"], "reason": x["reason"]} for x in days if x["decision"] == "rejected"][-5:],
        "latest": latest,
        "last_7_days": days[-7:],
        "image_tests": tests,
    }
    os.makedirs(os.path.join(a.data, "metrics"), exist_ok=True)
    json.dump(res, open(os.path.join(a.data, "metrics", "measure_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
