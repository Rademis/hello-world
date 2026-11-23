-- Schema di data/jobs.sqlite. Le skill e la dashboard leggono/scrivono qui.
CREATE TABLE IF NOT EXISTS jobs (
  id                TEXT PRIMARY KEY,          -- es. "gh-acme-123456" o "li-4012345678"
  fonte             TEXT NOT NULL,             -- linkedin | greenhouse | lever | ashby | altro
  url               TEXT NOT NULL,             -- pagina dell'annuncio
  url_candidatura   TEXT,                      -- dove ci si candida
  tipo_candidatura  TEXT NOT NULL DEFAULT 'altro', -- linkedin | greenhouse | lever | ashby | workday | altro
  azienda           TEXT NOT NULL,
  titolo            TEXT NOT NULL,
  luogo             TEXT,
  modalita          TEXT DEFAULT 'non_indicato', -- remoto | ibrido | sede | non_indicato
  giorni_remoto     INTEGER,                   -- giorni di smart working a settimana, se indicati
  stip_min          INTEGER,
  stip_max          INTEGER,
  stip_valuta       TEXT DEFAULT 'EUR',
  stip_periodo      TEXT DEFAULT 'anno',       -- anno | mese | ora
  stip_fonte        TEXT,                      -- annuncio | stima:<fonte> | NULL = non indicato
  benefit           TEXT DEFAULT '[]',         -- JSON array di stringhe, solo se citati nell'annuncio
  match             INTEGER,                   -- compatibilità 0-100 (valuta-match)
  coerenza          INTEGER,                   -- coerenza col percorso di carriera 0-100
  coerenza_label    TEXT,                      -- passo_avanti | laterale | passo_indietro | cambio_direzione
  coerenza_nota     TEXT,
  punti_forza       TEXT DEFAULT '[]',         -- JSON array
  gap               TEXT DEFAULT '[]',         -- JSON array
  sintesi           TEXT,
  testo             TEXT,
  data_pubblicazione TEXT,
  data_trovata      TEXT NOT NULL,
  stato             TEXT NOT NULL DEFAULT 'trovata',
  nota_stato        TEXT,
  aggiornato        TEXT
);
-- Stati:
--  trovata → valutata → (utente) selezionata → in_preparazione → pronta | pronta_linkedin
--  pronta → (utente) approvata → inviata (agente, portale esterno)       pronta_linkedin → inviata (utente, a mano)
--  in_attesa (CAPTCHA / domanda aperta / errore)    scartata | archiviata | colloquio | rifiutata
CREATE INDEX IF NOT EXISTS idx_jobs_stato ON jobs(stato);
