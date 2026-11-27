---
name: adatta-cv
description: Genera un CV su misura per un'offerta usando SOLO fatti presenti in profilo/master.yaml, lo fa verificare da un subagent indipendente e produce il PDF. Usare per offerte con stato "valutata" o quando l'utente chiede un CV per un annuncio.
---

# CV su misura, senza invenzioni

## 1. Bozza con citazioni
Scrivi `data/applications/<id>/cv.draft.md`: ogni riga termina con gli ID dei fatti usati, es.
`- Ridotto del 30% il tempo di rilascio automatizzando le pipeline CI/CD [exp2.b1]`.

Consentito: selezionare i fatti più pertinenti, riordinare, accorciare, usare la terminologia dell'annuncio
quando è davvero equivalente, scrivere il profilo iniziale nella lingua dell'annuncio.
Vietato: competenze non presenti, livelli più alti di quelli registrati, numeri non registrati,
date/titoli/aziende modificati, testo nascosto per gli ATS, trasformare un'esperienza "studiata" in "esperienza lavorativa".

## 2. Verifica indipendente (obbligatoria)
Avvia un subagent con SOLO `master.yaml` e `cv.draft.md` e questo compito:
"Per ogni riga, rispondi SUPPORTATA / NON SUPPORTATA / ESAGERATA confrontandola con i fatti citati. Sii severo."
Rimuovi o riscrivi le righe non supportate e ripeti finché sono tutte SUPPORTATE (max 3 giri, poi chiedi all'utente).

## 3. Rendering
Esegui `python3 scripts/render_cv.py data/applications/<id>/cv.draft.md CV_<Nome>_<Azienda>.pdf`: rimuove le citazioni e usa `templates/cv.css` (una colonna, font standard, niente tabelle/immagini per
l'ATS), esporta in PDF con Playwright: `data/applications/<id>/CV_<Nome>_<Azienda>.pdf`. Massimo 2 pagine.
Salva il log della verifica in `verifica_cv.md`.
