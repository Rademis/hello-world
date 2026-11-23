---
name: candidature-giornaliere
description: Routine giornaliera - cerca nuove offerte, le valuta per la dashboard, lancia la pipeline sulle offerte già selezionate dall'utente e scrive il report in data/report/AAAA-MM-GG.md. Usare quando l'utente scrive /candidature-giornaliere, "esegui la routine" o da un'attività pianificata.
---

# Routine giornaliera

1. `ricerca-offerte` (LinkedIn in sola lettura, a ritmo umano; ATS via API).
2. `valuta-match` su tutte le offerte `trovata` → compaiono nella dashboard in "Da valutare".
3. `prepara-candidature` sulle offerte che l'utente ha messo in pipeline (`selezionata`).
4. Report `data/report/<data>.md`:
   - nuove offerte da valutare (le 5 migliori con match, coerenza, stipendio, modalità);
   - pronte da inviare su LinkedIn (link);
   - inviate oggi sui portali esterni;
   - in attesa del tuo intervento (motivo);
   - follow-up: inviate da oltre 10 giorni senza risposta;
   - avvisi (es. LinkedIn ha mostrato un controllo di sicurezza → ricerca LinkedIn sospesa).
Ricorda all'utente: `python3 dashboard/server.py` per aprire la dashboard.
