---
name: invia-candidatura
description: Invia una candidatura già preparata su un portale ESTERNO a LinkedIn (Greenhouse, Lever, Ashby, Workday, altri) via API o browser, compilando i campi con master.yaml e la banca risposte; passa all'utente CAPTCHA e domande sconosciute. Non invia mai su LinkedIn. Usare da prepara-candidature o per righe con stato "pronta".
---

# Invio su portali esterni

**Mai su LinkedIn**: le offerte con `tipo_candidatura='linkedin'` restano `pronta_linkedin` e le invia l'utente.

## Controlli iniziali
- Limite `config.invio.max_al_giorno` non superato.
- Documenti presenti in `data/applications/<id>/`.

## Canale
1. **API** dove esiste un endpoint pubblico di candidatura per quell'ATS e l'azienda lo consente
   (es. alcuni job board Ashby/Lever espongono il form via API): preferirla al browser.
2. **Browser** (Playwright MCP) negli altri casi: apri `url_candidatura`, compila con `anagrafica`, `form`
   e `banca_risposte`, carica CV e lettera (`browser_fill_form`, `browser_select_option`, upload).
   - Workday e portali con registrazione: non creare account senza consenso esplicito → `in_attesa`.

## Regole
- Domanda senza risposta nella banca o numeri non registrati → non indovinare: `stato='in_attesa'`,
  domanda in `nota_stato` e in `data/applications/<id>/domande_aperte.md`.
- CAPTCHA o verifiche umane: mai aggirarli → `in_attesa` con link "Completa a mano" in dashboard.
- Screenshot `pre_invio.png` prima dell'invio, `conferma.png` dopo; poi `stato='inviata'`, `aggiornato=now`.
- Errore inatteso: non inviare, `in_attesa` con descrizione.
