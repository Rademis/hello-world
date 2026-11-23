---
name: invia-candidatura
description: Invia una candidatura pronta tramite LinkedIn Easy Apply o il portale esterno (Greenhouse, Lever, Workday, altri) compilando i campi con master.yaml e la banca risposte, con approvazione, limiti giornalieri e passaggio all'utente per CAPTCHA e domande sconosciute. Usare per candidature con stato "pronta".
---

# Invio candidatura

## Prima di iniziare
- Controlla `config.invio.max_al_giorno` e quante ne sono già state inviate oggi: se raggiunto, fermati.
- Modalità `config.invio.approvazione`: `sempre` (default) | `solo_esterni` | `mai`.
  Se serve approvazione e l'utente non l'ha data → stato `in_attesa`, passa alla successiva.

## Compilazione (Playwright MCP, sessione browser dell'utente)
1. Apri `url_candidatura`. Identifica il tipo (Easy Apply, Greenhouse, Lever, Workday, altro).
2. Compila i campi da `anagrafica` e `form` di master.yaml. Carica CV e lettera generati.
3. Domande di screening: usa `banca_risposte`. Per domande numeriche (anni di esperienza) usa SOLO i valori
   registrati. Se nessuna risposta è adatta → **non indovinare**: stato `in_attesa`, registra la domanda in
   `domande_aperte.md` per l'utente (che poi la aggiunge alla banca risposte).
4. Prima di "Invia": screenshot in `data/applications/<id>/pre_invio.png` e rilettura di tutti i campi.
5. Invia, attendi conferma, screenshot `conferma.png`, stato `inviata` con data.

## Sicurezza
- CAPTCHA, verifica identità, "attività insolita": **non aggirare mai**. Stato `in_attesa`, avvisa l'utente.
- Non creare account sui portali senza consenso esplicito dell'utente; non salvare password in chiaro.
- Pause casuali tra un'azione e l'altra; mai più di una candidatura in parallelo.
- In caso di errore inatteso lascia il form senza inviare e registra il problema.
