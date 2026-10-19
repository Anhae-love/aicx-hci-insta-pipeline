#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대시보드가 읽을 data/manifest.json 을 만든다.
대시보드(코드)는 output 폴더를 직접 뒤지지 않는다. 이 manifest(데이터 인덱스)만 읽는다.
= 코드와 데이터의 분리. 대량이 쌓여도 대시보드는 인덱스 한 파일만 본다.

파이프라인 끝(카드 제작 후)에 실행한다:
    python build_manifest.py <프로젝트루트> <docs출력폴더>
예) python automation/build_manifest.py . docs
"""
import json, os, sys, re, datetime

def read_text(p, default=""):
    try:
        return open(p, encoding="utf-8-sig").read().strip()
    except Exception:
        return default

def read_jsonl(p):
    rows = []
    try:
        for line in open(p, encoding="utf-8-sig"):
            line = line.strip()
            if line:
                try: rows.append(json.loads(line))
                except Exception: pass
    except Exception:
        pass
    return rows

def _pick(root, name):
    """새 구조(data/<name>)를 우선 쓰되, 옛 구조(<name>)도 하위호환으로 받는다."""
    new = os.path.join(root, "data", name)
    old = os.path.join(root, name)
    return new if os.path.isdir(new) else old

def main(root, docs):
    output_dir = _pick(root, "output")
    state_dir  = _pick(root, "state")
    docs_data  = os.path.join(docs, "data")
    docs_cards = os.path.join(docs, "cards")
    os.makedirs(docs_data, exist_ok=True)
    os.makedirs(docs_cards, exist_ok=True)

    index_rows = {r.get("folder"): r for r in read_jsonl(os.path.join(state_dir, "index.jsonl"))}
    last_run   = {}
    try: last_run = json.load(open(os.path.join(state_dir, "last_run.json"), encoding="utf-8"))
    except Exception: pass

    # 사람의 결정 기록 (승인/반려) — 측정 루프의 재료
    decisions = read_jsonl(os.path.join(state_dir, "decisions.jsonl"))
    dec_by_folder = {}
    for d in decisions:
        f = d.get("folder")
        if f:
            dec_by_folder[f] = d   # 같은 폴더면 마지막(최신) 결정이 이긴다

    entries = []
    if os.path.isdir(output_dir):
        for folder in sorted(os.listdir(output_dir), reverse=True):
            fpath = os.path.join(output_dir, folder)
            if not os.path.isdir(fpath) or folder.startswith("_"):
                continue
            status = read_text(os.path.join(fpath, "STATUS"), "unknown")
            notes  = read_text(os.path.join(fpath, "NOTES.md"))
            caption = read_text(os.path.join(fpath, "caption.txt"))
            meta = index_rows.get(folder, {})

            # 카드 이미지를 docs/cards/<folder>/ 로 복사 (대시보드가 웹에서 로드)
            cards = []
            dest = os.path.join(docs_cards, folder)
            os.makedirs(dest, exist_ok=True)
            for i in range(1, 7):
                src = os.path.join(fpath, f"slide_{i}.png")
                if os.path.exists(src):
                    import shutil
                    shutil.copy2(src, os.path.join(dest, f"slide_{i}.png"))
                    cards.append(f"cards/{folder}/slide_{i}.png")

            # 날짜 추출 (폴더명 앞 8자리)
            m = re.match(r"(\d{8})", folder)
            date = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:8]}" if m else ""

            dec = dec_by_folder.get(folder, {})
            entries.append({
                "folder": folder,
                "date": date or meta.get("date", ""),
                "title": meta.get("content_title", folder),
                "category": meta.get("weekday_category", ""),
                "source_title": meta.get("source_title", ""),
                "source_url": meta.get("source_url", ""),
                "object_name": meta.get("object_name", ""),
                "accent_color": meta.get("accent_color", ""),
                "verdict": meta.get("verdict", ""),
                "attempts": meta.get("attempts", 0),
                "status": status,
                "cards": cards,
                "caption": caption,
                "notes": notes,
                "decision": dec.get("decision", ""),      # approved / rejected / ""
                "reject_reason": dec.get("reason", "") if dec.get("decision") == "rejected" else "",
            })

    # 측정 루프 지표: 결정이 쌓인 것만 집계 (아직 결정 안 난 건 제외)
    decided = [e for e in entries if e.get("decision")]
    n_app = sum(1 for e in decided if e["decision"] == "approved")
    n_rej = sum(1 for e in decided if e["decision"] == "rejected")
    # 최근 반려 사유(기획실이 읽는 바로 그 신호)를 날짜 내림차순으로
    recent_rejects = [
        {"date": e["date"], "title": e["title"], "reason": e["reject_reason"]}
        for e in entries if e.get("decision") == "rejected" and e.get("reject_reason")
    ]

    manifest = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "last_run": last_run,
        "count": len(entries),
        "metrics": {
            "decided": len(decided),
            "approved": n_app,
            "rejected": n_rej,
            "approval_rate": round(n_app / len(decided), 3) if decided else None,
            "recent_rejects": recent_rejects[:8],
        },
        "latest": entries[0] if entries else None,
        "history": entries,
    }
    out = os.path.join(docs_data, "manifest.json")
    json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"manifest 생성: {out}  (콘텐츠 {len(entries)}건)")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    docs = sys.argv[2] if len(sys.argv) > 2 else "docs"
    main(root, docs)
