#!/usr/bin/env python3
"""Scarica gli annunci dalle API pubbliche di Greenhouse, Lever e Ashby e salva in data/ats/ quelli
pertinenti (ruolo + luogo). La valutazione la fa poi la skill valuta-match.

    python3 scripts/cerca_ats.py                  # usa scripts/ats_boards.txt
    python3 scripts/cerca_ats.py --boards altro.txt

Formato del file boards: una riga per azienda, "ats slug" (ats = greenhouse | lever | ashby).
"""
import argparse, json, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUOLI = re.compile(r"product (manager|lead|owner|director)|head of product|director of product|vp product|chief product|"
                   r"digital product|product operations|head of (digital )?operations|customer success (lead|director)|head of customer", re.I)
LUOGHI = re.compile(r"milan|milano|ital", re.I)
API = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true",
    "lever": "https://api.lever.co/v0/postings/{s}?mode=json",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{s}?includeCompensation=true",
}

def normalizza(ats, slug, d):
    if ats == "greenhouse":
        for j in d.get("jobs", []):
            yield dict(id=f"gh-{slug}-{j['id']}", titolo=j["title"], luogo=j.get("location", {}).get("name", ""),
                       url=j["absolute_url"], testo=j.get("content", ""), pubblicato=j.get("updated_at", "")[:10])
    elif ats == "lever":
        for j in d:
            yield dict(id=f"lv-{slug}-{j['id'][:8]}", titolo=j["text"], luogo=(j.get("categories") or {}).get("location") or "",
                       url=j["hostedUrl"], testo=j.get("descriptionPlain", ""), pubblicato="")
    else:
        for j in d.get("jobs", []):
            luogo = " / ".join([j.get("location") or ""] + [x.get("location", "") for x in j.get("secondaryLocations") or []])
            yield dict(id=f"ab-{slug}-{j['id'][:8]}", titolo=j["title"], luogo=luogo, url=j["jobUrl"],
                       url_candidatura=j.get("applyUrl"), modalita=j.get("workplaceType"),
                       compenso=(j.get("compensation") or {}).get("compensationTierSummary"),
                       testo=j.get("descriptionPlain", ""), pubblicato=(j.get("publishedAt") or "")[:10])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boards", default=str(ROOT / "scripts" / "ats_boards.txt"))
    a = ap.parse_args()
    out_dir = ROOT / "data" / "ats"; out_dir.mkdir(parents=True, exist_ok=True)
    trovati = []
    for riga in Path(a.boards).read_text().splitlines():
        if not riga.strip() or riga.startswith("#"):
            continue
        ats, slug = riga.split()[:2]
        try:
            req = urllib.request.Request(API[ats].format(s=slug), headers={"User-Agent": "job-agent/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
        except Exception as e:
            print(f"! {ats}/{slug}: {e}"); continue
        for j in normalizza(ats, slug, d):
            if RUOLI.search(j["titolo"]) and LUOGHI.search(j["luogo"]):
                j.update(ats=ats, azienda=slug); trovati.append(j)
    (out_dir / "ultimi.json").write_text(json.dumps(trovati, ensure_ascii=False, indent=1))
    for j in trovati:
        print(f"{j['ats']:10} {j['azienda']:15} {j['titolo']}  [{j['luogo']}]")
    print(f"{len(trovati)} annunci pertinenti → data/ats/ultimi.json")

if __name__ == "__main__":
    main()
