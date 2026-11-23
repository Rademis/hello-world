#!/usr/bin/env python3
"""Crea data/demo.sqlite con offerte FITTIZIE per provare la dashboard.

    python3 dashboard/demo_seed.py && python3 dashboard/server.py --db data/demo.sqlite
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "demo.sqlite"

OFFERTE = [
    # id, fonte, tipo, azienda, titolo, luogo, modalita, gg, min, max, periodo, fonte_stip, benefit, match, coer, label, nota, forza, gap, stato
    ("gh-nordlab-1", "greenhouse", "greenhouse", "Nordlab (demo)", "Senior Data Engineer", "Milano", "ibrido", 3, 55000, 65000, "anno", "annuncio",
     ["Buoni pasto", "Assicurazione sanitaria", "Budget formazione 1.500 €", "Welfare"], 88, 85, "passo_avanti",
     "Aumenta la seniority sullo stesso dominio dati: coerente con l'obiettivo 'tech lead entro 3 anni'.",
     ["5 anni di pipeline Python/Airflow", "Esperienza con dbt in produzione"], ["Kafka richiesto come preferenziale: livello base"], "valutata"),
    ("li-4021", "linkedin", "linkedin", "Fintech Aurora (demo)", "Analytics Engineer", "Roma", "remoto", None, None, None, "anno", None,
     ["Stock option"], 81, 70, "laterale", "Ruolo affine al percorso attuale, settore nuovo (fintech).",
     ["SQL avanzato", "Modellazione dati"], ["Esperienza fintech non presente"], "valutata"),
    ("lv-orbita-7", "lever", "lever", "Orbita Mobility (demo)", "Data Platform Lead", "Torino", "sede", 0, 70000, 80000, "anno", "stima:Glassdoor",
     ["Auto aziendale", "Premio di risultato"], 74, 90, "passo_avanti", "Primo ruolo di guida di un team: in linea con l'obiettivo di carriera.",
     ["Ha coordinato 3 persone in exp2"], ["Gestione budget non documentata", "Richiesta presenza 5 giorni"], "valutata"),
    ("li-4033", "linkedin", "linkedin", "Retail Group Sud (demo)", "BI Specialist", "Napoli", "ibrido", 2, 32000, 36000, "anno", "annuncio",
     [], 66, 35, "passo_indietro", "Ruolo meno tecnico e più junior rispetto all'attuale.", ["Power BI"], ["Seniority inferiore"], "valutata"),
    ("as-kite-2", "ashby", "ashby", "Kite Health (demo)", "Machine Learning Engineer", "Remoto (UE)", "remoto", None, 60000, 75000, "anno", "annuncio",
     ["Lavoro da remoto in UE", "Ferie illimitate", "Budget home office"], 77, 60, "cambio_direzione",
     "Spostamento verso ML: coerente con l'interesse dichiarato, ma con gap da colmare.", ["Python", "MLOps base"], ["Deep learning: solo studiato"], "selezionata"),
    ("li-4050", "linkedin", "linkedin", "Logistica Alpina (demo)", "Senior Data Engineer", "Bolzano", "ibrido", 2, 50000, 58000, "anno", "annuncio",
     ["Mensa aziendale", "Orario flessibile"], 84, 80, "passo_avanti", "Stesso ruolo, azienda più grande.", ["Airflow", "AWS"], [], "pronta_linkedin"),
    ("gh-verde-3", "greenhouse", "greenhouse", "Verde Energia (demo)", "Data Engineer", "Bologna", "ibrido", 2, 45000, 52000, "anno", "annuncio",
     ["Buoni pasto", "Welfare"], 79, 65, "laterale", "Laterale, settore energia.", ["ETL", "GCP"], ["Esperienza settore energia"], "in_attesa"),
    ("li-3990", "linkedin", "linkedin", "Media Plus (demo)", "Data Engineer", "Milano", "ibrido", 2, None, None, "anno", None,
     [], 72, 55, "laterale", "", ["Spark"], [], "inviata"),
]


def main():
    DB.parent.mkdir(exist_ok=True)
    DB.unlink(missing_ok=True)
    conn = sqlite3.connect(DB)
    conn.executescript((ROOT / "db" / "schema.sql").read_text(encoding="utf-8"))
    for o in OFFERTE:
        (id_, fonte, tipo, az, tit, luogo, mod, gg, smin, smax, per, sfonte, ben, m, c, lab, nota, forza, gap, stato) = o
        url = f"https://example.com/annunci/{id_}"
        conn.execute(
            """INSERT INTO jobs (id, fonte, url, url_candidatura, tipo_candidatura, azienda, titolo, luogo, modalita,
               giorni_remoto, stip_min, stip_max, stip_periodo, stip_fonte, benefit, match, coerenza, coerenza_label,
               coerenza_nota, punti_forza, gap, sintesi, data_trovata, stato, nota_stato)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (id_, fonte, url, url, tipo, az, tit, luogo, mod, gg, smin, smax, per, sfonte, json.dumps(ben), m, c, lab,
             nota, json.dumps(forza), json.dumps(gap), f"Offerta di esempio per {tit}.", "2026-11-23", stato,
             "Domanda aperta: 'Disponibilità a trasferte all'estero?'" if stato == "in_attesa" else None))
    conn.commit()
    print(f"Creato {DB} con {len(OFFERTE)} offerte fittizie")


if __name__ == "__main__":
    main()
