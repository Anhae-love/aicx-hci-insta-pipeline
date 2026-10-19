#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""개인과제 지표: 정상적으로 열리는 이미지 수 / 만들기로 한 이미지 수.

로그의 '성공' 숫자를 믿지 않고, 실제 PNG 파일을 하나씩 열어서(디코딩까지) 센다.
- 카드: output/<폴더>/slide_1~6.png  (계획 = 6장, 단 STATUS가 rejected/verify_failed면 계획 0장)
- 이미지 테스트: image_tests/<날짜>/image_test_report.json 의 planned 값

사용: python code/tools/check_images.py data
결과: data/metrics/image_open_rate.json
"""
import json, os, sys, datetime
from PIL import Image

NO_CARD_STATUS = {"rejected", "verify_failed", "no_output", "needs_human"}

def can_open(p):
    try:
        with Image.open(p) as im:
            im.load()
        return True
    except Exception:
        return False

def main(data):
    rows, tot_plan, tot_open = [], 0, 0
    out_dir = os.path.join(data, "output")
    for folder in sorted(os.listdir(out_dir)):
        fp = os.path.join(out_dir, folder)
        if not os.path.isdir(fp) or folder.startswith("_"):
            continue
        try:
            status = open(os.path.join(fp, "STATUS"), encoding="utf-8-sig").read().strip()
        except Exception:
            status = "unknown"
        planned = 0 if status in NO_CARD_STATUS else 6
        opened = sum(can_open(os.path.join(fp, f"slide_{i}.png")) for i in range(1, 7)
                     if os.path.exists(os.path.join(fp, f"slide_{i}.png")))
        rows.append({"kind": "card", "folder": folder, "status": status, "planned": planned, "opened": opened})
        tot_plan += planned; tot_open += min(opened, planned) if planned else 0

    it_dir = os.path.join(data, "image_tests")
    if os.path.isdir(it_dir):
        for d in sorted(os.listdir(it_dir)):
            rp = os.path.join(it_dir, d, "image_test_report.json")
            if not os.path.exists(rp):
                continue
            rep = json.load(open(rp, encoding="utf-8"))
            files = [f["file"] for f in rep.get("files", [])]
            opened = sum(can_open(os.path.join(it_dir, d, f)) for f in files)
            rows.append({"kind": "image_test", "folder": d, "tool": rep.get("tool"), "planned": rep.get("planned", len(files)), "opened": opened})
            tot_plan += rep.get("planned", len(files)); tot_open += opened

    res = {"generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
           "metric": "정상적으로 열리는 이미지 수 / 만들기로 한 이미지 수",
           "planned": tot_plan, "opened": tot_open,
           "rate": round(tot_open / tot_plan, 4) if tot_plan else None,
           "rows": rows}
    os.makedirs(os.path.join(data, "metrics"), exist_ok=True)
    json.dump(res, open(os.path.join(data, "metrics", "image_open_rate.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{tot_open}/{tot_plan} = {res['rate']}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data")
