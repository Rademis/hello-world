---
name: valuta-match
description: Valuta le offerte con stato "trovata" contro profilo/master.yaml - filtri duri, compatibilità 0-100, coerenza col percorso di carriera, stipendio, benefit, luogo e smart working - e le scrive in data/jobs.sqlite per la dashboard. Usare dopo ricerca-offerte o quando l'utente incolla un annuncio e chiede se è adatto.
---

# Valutazione delle offerte

Scrive nelle colonne di `data/jobs.sqlite` (schema in `db/schema.sql`) tutto ciò che la dashboard mostra.

## 1. Filtri duri
Da `preferenze` di master.yaml e `profilo/config.yaml`: luogo/remoto, RAL, lingua, seniority, contratto,
permesso di lavoro. Se fallisce → `stato='scartata'`, motivo in `nota_stato`.
- RAL: scarta solo se l'annuncio dichiara un massimo sotto `preferenze.ral_filtro` (trattabile verso `ral_minima`).
  Se la RAL non è indicata, non scartare.
- Full remote: ammesso solo se la RAL dichiarata è >= `preferenze.full_remote_ral_minima`.
- `settori_esclusi_soft`: non scartare, togli 15 punti alla coerenza e annotalo in `coerenza_nota`.
- `tipo_azienda`: usa le priorità per la componente "preferenze" del match.

## 2. Dati dell'annuncio (estrarre SOLO ciò che è scritto)
- `luogo`, `modalita` (`remoto | ibrido | sede | non_indicato`), `giorni_remoto` se specificati.
- `stip_min`, `stip_max`, `stip_valuta`, `stip_periodo`, `stip_fonte='annuncio'`.
  Se l'annuncio non lo indica: lasciare NULL. Una stima è ammessa solo se `config.stime_stipendio: true`,
  da una fonte pubblica citata (`stip_fonte='stima:<fonte>'`); la dashboard la marca come "stima".
- `benefit`: array JSON dei benefit citati (buoni pasto, welfare, assicurazione, formazione, auto, stock…).
  Mai dedurre benefit non scritti.

## 3. Compatibilità (`match`, 0-100)
Requisiti obbligatori e preferenziali dell'annuncio → evidenze nella banca dei fatti (ID).
Ogni requisito: `coperto | parziale | gap`. Peso: 70% obbligatori, 20% preferenziali, 10% preferenze.
`punti_forza` (max 4) e `gap` in JSON. Requisito obbligatorio scoperto → annotarlo nei gap con "(obbligatorio)".

## 4. Coerenza col percorso di carriera (`coerenza`, 0-100)
Confronta con `carriera` di master.yaml (ruolo attuale, obiettivo a 3-5 anni, direzioni accettate/escluse):
- `coerenza_label`: `passo_avanti | laterale | passo_indietro | cambio_direzione`
- `coerenza_nota`: una frase che spiega il giudizio (seniority, responsabilità, dominio, settore).

## 5. Esito
`sintesi` di 1-2 frasi. Se `match >= config.soglia_match` → `stato='valutata'` (compare in "Da valutare"),
altrimenti `stato='scartata'`. Non selezionare mai al posto dell'utente: la scelta avviene nella dashboard.
