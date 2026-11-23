---
name: candidature-giornaliere
description: Esegue la routine giornaliera completa (ricerca, valutazione, CV, lettera, invio) e produce il report in data/report/AAAA-MM-GG.md. Usare quando l'utente scrive /candidature-giornaliere, "esegui la routine" o da un'attività pianificata.
---

# Routine giornaliera

1. `ricerca-offerte`
2. `valuta-match` su tutte le offerte `trovata`
3. Per le migliori `valutata` (ordinate per punteggio, max `config.invio.max_al_giorno`):
   `adatta-cv` → `lettera-motivazionale` → stato `pronta`
4. `invia-candidatura` sulle `pronta` (rispettando la modalità di approvazione)
5. Scrivi `data/report/<data>.md`:
   - nuove offerte trovate / scartate (con motivo sintetico)
   - candidature inviate (azienda, ruolo, punteggio, link)
   - **in attesa di te**: approvazioni, domande aperte, CAPTCHA
   - follow-up: candidature inviate da più di 10 giorni senza risposta
   - eventuali avvisi (es. LinkedIn ha mostrato un controllo di sicurezza → ricerca LinkedIn sospesa)
6. Se configurato, aggiungi le righe al Google Sheet di tracking.
