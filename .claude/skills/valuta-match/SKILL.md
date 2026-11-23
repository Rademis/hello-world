---
name: valuta-match
description: Valuta le offerte con stato "trovata" contro profilo/master.yaml, applica filtri duri e assegna un punteggio di compatibilità 0-100 con la lista dei gap. Usare dopo ricerca-offerte o quando l'utente incolla un annuncio e chiede se è adatto.
---

# Valutazione del match

1. **Filtri duri** da `preferenze` e `config.yaml`: luogo/remoto, RAL (se indicata), lingua, seniority,
   settori esclusi, permesso di lavoro. Se fallisce → stato `scartata` con motivo.
2. Estrai dall'annuncio i requisiti, separando **obbligatori** e **preferenziali**.
3. Per ciascun requisito cerca evidenze nella banca dei fatti (cita gli ID). Classifica: `coperto`,
   `parziale` (competenza affine o livello inferiore), `gap`.
4. Punteggio: 70% requisiti obbligatori, 20% preferenziali, 10% preferenze utente (settore, dimensione azienda).
5. Se un requisito obbligatorio è `gap` → stato `da_chiedere` (o `scartata` se `config.gap_obbligatorio: scarta`).
6. Se punteggio >= `config.soglia_match` → stato `valutata`, altrimenti `scartata`.
Salva punteggio, tabella requisiti→evidenze e gap in `data/applications/<id>/match.md`.
