---
name: ricerca-offerte
description: Cerca nuove offerte di lavoro compatibili con profilo/master.yaml su LinkedIn e sugli ATS delle aziende target, e le salva deduplicate in data/jobs.sqlite. Usare nell'esecuzione giornaliera o quando l'utente chiede "cerca offerte".
---

# Ricerca offerte

## Fonti
1. **ATS diretti** (preferiti, nessun rischio account) per le aziende in `profilo/aziende.yaml`:
   - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<board>/jobs?content=true`
   - Lever: `https://api.lever.co/v0/postings/<azienda>?mode=json`
   - Ashby: `https://api.ashbyhq.com/posting-api/job-board/<azienda>`
2. **LinkedIn** con la sessione dell'utente (Playwright MCP o linkedin-mcp-server `search_jobs`), usando
   ruoli e località da `preferenze` in master.yaml.
   - Massimo `config.linkedin.max_pagine_giorno` pagine, pause casuali 5-20 s tra le azioni.
   - Se compare un CAPTCHA o un avviso di attività insolita: **fermati** e segnalalo nel report.

## Salvataggio
Per ogni offerta salva in `data/jobs.sqlite` (tabella `jobs`): id, fonte, url, url_candidatura,
tipo_candidatura (`easy_apply | greenhouse | lever | workday | altro`), azienda, titolo, luogo, remoto,
testo completo, data_trovata, stato=`trovata`.
Deduplica su (azienda normalizzata, titolo normalizzato, luogo). Se esiste già, aggiungi solo la nuova fonte.
