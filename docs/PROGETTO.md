# Agente di candidatura automatica — Progetto

> Obiettivo: partire dal profilo LinkedIn e dal CV, intervistare l'utente per completare il quadro,
> trovare ogni giorno le offerte compatibili, generare CV e lettera motivazionale su misura
> **senza mai dichiarare cose non vere**, e inviare la candidatura (LinkedIn Easy Apply o portale esterno).

---

## 1. Avvertenza importante (da leggere prima di tutto)

- **LinkedIn vieta l'automazione.** La sezione 8.2 dello User Agreement e la pagina
  [Prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387) vietano bot
  e accessi automatizzati; chi li usa rischia limitazioni temporanee o la chiusura dell'account.
  LinkedIn non offre API pubbliche per candidarsi: ogni "auto-apply" lavora dentro la tua sessione loggata.
- **Conseguenza progettuale:** l'agente è pensato in modalità **semi-automatica** ("human-in-the-loop"):
  prepara tutto da solo, ma l'invio su LinkedIn avviene con volumi bassi, ritmo umano e — di default —
  con la tua approvazione. L'automazione piena è un'opzione che attivi tu, sapendo il rischio.
- **Dove possibile si aggira LinkedIn:** molte offerte rimandano a ATS aziendali (Greenhouse, Lever, Ashby,
  Workday, SmartRecruiters). Greenhouse, Lever e Ashby hanno API pubbliche di lettura degli annunci,
  quindi la *ricerca* può avvenire lì senza toccare LinkedIn.
- **Privacy (GDPR):** CV, risposte e storico restano in locale (cartelle `profilo/` e `data/`, escluse da git).

---

## 2. Architettura a fasi

```
┌──────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────┐
│ 0 ONBOARDING │ → │ 1 RICERCA    │ → │ 2 VALUTA    │ → │ 3 ADATTA CV  │ → │ 5 INVIO      │ → │ 6 REPORT   │
│ CV+LinkedIn+ │   │ LinkedIn+ATS │   │ match 0-100 │   │ 4 LETTERA    │   │ Easy Apply / │   │ tracker +  │
│ intervista   │   │ dedup SQLite │   │ filtri duri │   │ + verifica   │   │ portale ATS  │   │ riepilogo  │
└──────┬───────┘   └──────────────┘   └─────────────┘   └──────────────┘   └──────────────┘   └────────────┘
       ▼
  profilo/master.yaml  ← unica fonte di verità ("banca dei fatti")
```

Ogni fase è una **skill** di Claude Code in `.claude/skills/<nome>/SKILL.md`. Un comando orchestratore
(`claude -p "/candidature-giornaliere"`) le esegue in sequenza ed è ciò che viene schedulato.

### Fase 0 — Onboarding (una volta, poi aggiornamenti)
1. **Input:** CV (PDF/DOCX) + profilo LinkedIn. Per LinkedIn conviene usare il "Salva in PDF" del profilo
   o l'export dati ufficiale (Impostazioni → Privacy → Ottieni una copia dei tuoi dati): niente scraping.
2. **Estrazione** in `profilo/master.yaml` (schema in `templates/master.example.yaml`): esperienze,
   formazione, certificazioni, lingue, progetti.
3. **Intervista guidata** — domande mirate per colmare i vuoti, per esempio:
   - per ogni esperienza: risultati misurabili (numeri, %, €), tecnologie realmente usate, dimensione team;
   - livello reale di ogni competenza (`esperto / uso quotidiano / base / solo studiata`) con un'evidenza;
   - competenze complementari non nel CV (soft skill con esempi, volontariato, side project, strumenti);
   - preferenze: ruoli, seniority, città/remoto, RAL minima, tipo contratto, preavviso, settori esclusi;
   - dati da form: permesso di lavoro, disponibilità a trasferte/trasferimento, patente, data di inizio;
   - **banca risposte** alle domande di screening ricorrenti ("anni di esperienza con X", "perché noi").
4. Ogni fatto riceve un **ID** (`exp1.b3`) che verrà citato nei documenti generati.

### Fase 1 — Ricerca offerte (giornaliera)
- **LinkedIn:** ricerca con le parole chiave/luoghi del profilo, tramite browser con la tua sessione
  (Playwright MCP) o un MCP dedicato (es. `stickerdaniel/linkedin-mcp-server`, tool `search_jobs`).
  Limiti: poche decine di pagine al giorno, pause casuali.
- **ATS diretti:** elenco aziende target in `profilo/aziende.yaml`, lette via API pubbliche
  (`boards-api.greenhouse.io`, `api.lever.co/v0/postings`, `api.ashbyhq.com/posting-api`).
- Normalizzazione e **deduplica** in `data/jobs.sqlite` (stessa offerta su più canali = una riga).

### Fase 2 — Valutazione del match
- **Filtri duri** (scarta subito): luogo, RAL, lingua, seniority, settori esclusi, permesso di lavoro.
- **Punteggio 0–100** confrontando requisiti dell'annuncio con la banca dei fatti; produce anche la
  lista dei *gap* (requisiti che non hai). Sotto soglia (es. 70) → non si candida.
- Se un requisito obbligatorio è un gap reale → non si candida (o chiede a te).

### Fase 3 — CV su misura (con garanzia di veridicità)
Trasformazioni **consentite**: selezionare, riordinare, accorciare, riformulare usando la terminologia
dell'annuncio *se equivalente* (es. "CI/CD" ↔ "pipeline di deploy automatizzate"), mettere in evidenza
metriche già registrate.
Trasformazioni **vietate**: aggiungere competenze non presenti, alzare il livello di una competenza,
cambiare date/titoli/aziende, inventare numeri, "keyword stuffing" invisibile.

Meccanismo anti-invenzione:
1. il generatore produce il CV in un formato intermedio dove **ogni riga cita gli ID dei fatti** usati;
2. una **seconda istanza "verificatore"** (subagent) controlla riga per riga che ogni affermazione sia
   supportata dai fatti citati; se no, la riga viene rimossa o rigenerata;
3. solo dopo la verifica si genera il PDF (HTML → PDF con Playwright, layout a colonna singola, ATS-friendly).

### Fase 4 — Lettera motivazionale
Stesse regole del CV. In più: breve ricerca sull'azienda (sito, notizie recenti) per 1–2 frasi
specifiche e verificabili. Lunghezza 200–300 parole, lingua dell'annuncio, tono configurabile.

### Fase 5 — Invio
- **LinkedIn Easy Apply:** caricamento CV/lettera, risposte ai campi con la banca risposte.
- **Portale esterno:** Playwright MCP (`browser_fill_form`, `browser_select_option`, upload file).
  Greenhouse e Lever sono i più prevedibili; Workday richiede account e passaggi multipli (supporto
  "best effort").
- **Regole di sicurezza:**
  - domanda a cui la banca risposte non sa rispondere → candidatura messa **in attesa**, ti viene chiesto;
  - CAPTCHA / verifica umana → **mai aggirati**: passaggio a te;
  - modalità `approvazione: sempre | solo_esterni | mai` (default `sempre`);
  - tetto giornaliero (default 10) e pause tra un invio e l'altro;
  - screenshot della pagina prima del click su "Invia" salvato in `data/applications/<id>/`.

### Fase 6 — Tracking e report
`data/jobs.sqlite` contiene stato (`trovata → valutata → pronta → in_attesa → inviata → risposta`),
punteggio, file generati, data. Ogni giorno un report Markdown (eventualmente inviato su Google Sheets
o email) con: nuove offerte, candidature inviate, quelle in attesa della tua decisione, follow-up da fare.

---

## 3. Schedulazione giornaliera

| Opzione | Dove gira | Pro | Contro |
|---|---|---|---|
| **cron / launchd + `claude -p`** sul tuo PC | locale | sessione LinkedIn e IP residenziale reali; dati in locale | il PC deve essere acceso |
| **Attività pianificate dell'app Claude desktop** | locale | nessuna configurazione cron | come sopra |
| **Attività pianificate cloud (claude.ai/code)** | container cloud | sempre attivo | IP da datacenter, nessuna sessione LinkedIn: adatto solo a ricerca su ATS e bozze |

Schema consigliato: di notte (cloud o locale) **ricerca + valutazione + bozze**; al mattino ricevi il
report, approvi; l'invio gira **in locale** col tuo browser.

Esempio cron (ogni giorno alle 7:40):
```
40 7 * * * cd ~/job-agent && claude -p "/candidature-giornaliere" --permission-mode acceptEdits >> data/log.txt 2>&1
```

---

## 4. Cosa esiste già su GitHub (ricerca novembre 2026)

Nessun progetto è stato verificato a fondo: leggere sempre il codice / lo SKILL.md prima di installarlo.

| Progetto | Cosa fa | Utilità per noi |
|---|---|---|
| [santifer/career-ops](https://github.com/santifer/career-ops) (MIT) | Sistema completo per Claude Code: legge career page con Playwright, valuta il fit, genera CV su misura, traccia le candidature | **Base consigliata** da cui partire/ispirarsi per fasi 1–4 e 6 |
| [varunr89/resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill) (MIT) | Skill Claude Code per CV su misura, singolo o multi-annuncio | Fase 3 |
| [amanattar/resume-tailoring-skill](https://github.com/amanattar/resume-tailoring-skill) | Skill minimale: ricerca ruolo, punteggio di fit, CV "truthful" | Fase 2–3 |
| [earino/resumasher](https://earino.github.io/resumasher/) | CV su misura in Claude Code/Codex/Gemini, storico locale | Fase 3 |
| [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server) | MCP che usa la tua sessione browser: `search_jobs`, dettagli offerta, profilo | Fase 0 e 1 |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | MCP ufficiale per pilotare il browser: compila form, upload | Fase 1 e 5 |
| [job-apply-mcp](https://glama.ai/mcp/servers/jpzg08t4pw) | Cerca su Greenhouse/Lever/Ashby/Workday; compila form Greenhouse e Lever e lascia a te il click finale | Fase 5 portali esterni |
| [ibarrajo/ApplyPilot](https://github.com/ibarrajo/ApplyPilot) | Pipeline scopri→valuta→CV→lettera; auto-apply solo Easy Apply, pausa su login/CAPTCHA | Riferimento per human-in-the-loop |
| [shwechau/applymatic](https://github.com/shwechau/applymatic) | Usa Claude; invio su Greenhouse e Lever, Workday in sviluppo | Fase 5 |
| [GodsScion/Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn) | Bot Easy Apply in locale con il tuo account | Riferimento tecnico (rischio ToS) |
| [feder-cr/Jobs_Applier_AI_Agent](https://github.com/feder-cr/Jobs_Applier_AI_Agent) (AGPL) | Ex "AIHawk": genera CV, profilo in YAML; stato dell'auto-apply open source incerto | Riferimento per lo schema dati |
| [attdobi/aipply](https://github.com/attdobi/aipply) | Scansione LinkedIn, auto-apply, CV/lettera con OpenAI, tracking | Riferimento |

Registri dove cercare altre skill: [skills.sh](https://skills.sh), [claudemarketplaces.com](https://claudemarketplaces.com),
[topic GitHub job-application-automation](https://github.com/topics/job-application-automation).

**Raccomandazione:** non ripartire da zero. Usare *career-ops* come riferimento per ricerca/valutazione/tracking,
aggiungere **le nostre** skill per (a) intervista di onboarding, (b) verificatore anti-invenzione,
(c) invio con regole di sicurezza; usare Playwright MCP per i browser e, opzionalmente,
linkedin-mcp-server per la ricerca su LinkedIn.

---

## 5. Struttura del repository

```
.claude/skills/
  onboarding-intervista/SKILL.md   fase 0
  ricerca-offerte/SKILL.md         fase 1
  valuta-match/SKILL.md            fase 2
  adatta-cv/SKILL.md               fase 3 (+ verificatore)
  lettera-motivazionale/SKILL.md   fase 4
  invia-candidatura/SKILL.md       fase 5
  candidature-giornaliere/SKILL.md  fase 6 + orchestrazione giornaliera
templates/
  master.example.yaml              schema della banca dei fatti
  config.example.yaml              soglie, limiti, modalità approvazione
profilo/   (privato, gitignored)   master.yaml, cv originale, aziende.yaml
data/      (privato, gitignored)   jobs.sqlite, documenti generati, screenshot, log
```

## 6. Roadmap suggerita

1. **Settimana 1:** onboarding + `master.yaml` + CV/lettera su misura per annunci incollati a mano
   (già utile da solo, zero rischi).
2. **Settimana 2:** ricerca su ATS diretti + valutazione + report giornaliero schedulato.
3. **Settimana 3:** invio su Greenhouse/Lever con approvazione.
4. **Settimana 4:** ricerca e Easy Apply su LinkedIn, volumi bassi, con approvazione.
5. Poi: metriche (tasso di risposta per tipo di CV), miglioramento dei prompt.
