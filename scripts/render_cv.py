#!/usr/bin/env python3
"""Converte una bozza di CV con citazioni (cv.draft.md) in HTML e PDF ATS-friendly.

    python3 scripts/render_cv.py data/applications/<id>/cv.draft.md "CV_Nome_Azienda.pdf"

Formato della bozza: sezioni "## Titolo"; righe "- testo [ID fatti]". Le citazioni finali tra
parentesi quadre vengono rimosse. Sezioni speciali: Header (nome, titolo, contatti), Profile, Skills;
le esperienze hanno il titolo "Azienda — Ruolo · Luogo · Date" e una prima riga opzionale "Context: ...".
"""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E = html.escape

def clean(t):
    return re.sub(r"\s*\[[^\]]*\]\s*$", "", t).strip()

def bullet(t):
    t = clean(t)
    m = re.match(r"([A-Z][A-Za-z &\-]{2,40}): (.*)", t)
    if m and len(m.group(1).split()) <= 4:
        return f"<li><b>{E(m.group(1))}:</b> {E(m.group(2))}</li>"
    return f"<li>{E(t)}</li>"

def to_html(src):
    out = []
    for sec in re.split(r"^## ", src, flags=re.M)[1:]:
        title, *lines = sec.strip().split("\n")
        lines = [l[2:] for l in lines if l.startswith("- ")]
        if title == "Header":
            out.append(f"<h1>{E(clean(lines[0]))}</h1><div class='headline'>{E(clean(lines[1]))}</div>"
                       f"<div class='contacts'>{E(clean(lines[2]))}</div>")
        elif title == "Profile":
            out.append("<h2>Profile</h2><p>" + " ".join(E(clean(l)) for l in lines) + "</p>")
        elif "·" in title:
            if not any(o.startswith("<h2>Experience") for o in out):
                out.append("<h2>Experience</h2>")
            parts = [p.strip() for p in clean(title).split("·")]
            ctx = ""
            if lines and lines[0].startswith("Context:"):
                ctx = f"<div class='context'>{E(clean(lines[0])[9:])}</div>"
                lines = lines[1:]
            out.append(f"<div class='job'><div class='job-head'><span>{E(parts[0])}</span>"
                       f"<span class='when'>{E(' · '.join(parts[1:]))}</span></div>{ctx}"
                       f"<ul>{''.join(bullet(l) for l in lines)}</ul></div>")
        elif title == "Skills":
            out.append("<h2>Skills & Languages</h2><div class='skills'>"
                       + "".join(f"<p>{bullet(l)[4:-5]}</p>" for l in lines) + "</div>")
        else:
            out.append(f"<h2>{E(title)}</h2><ul>{''.join(bullet(l) for l in lines)}</ul>")
    name = clean(re.search(r"^## Header\n- (.*)$", src, re.M).group(1))
    css = (ROOT / "templates" / "cv.css").read_text()
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{E(name)} - CV</title>"
            f"<style>{css}</style></head><body>{''.join(out)}</body></html>")

def main():
    draft, pdf_name = Path(sys.argv[1]).resolve(), sys.argv[2]
    html_path = draft.with_name("cv.html")
    html_path.write_text(to_html(draft.read_text()))
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{html_path}');await p.pdf({{path:'{draft.with_name(pdf_name)}',format:'A4',preferCSSPageSize:true}});"
          "await b.close();})()")
    subprocess.run(["node", "-e", js], check=True)
    print(draft.with_name(pdf_name))

if __name__ == "__main__":
    main()
