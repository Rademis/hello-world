---
name: onboarding-intervista
description: Costruisce o aggiorna profilo/master.yaml partendo dal CV e dall'export del profilo LinkedIn, poi intervista l'utente per colmare i vuoti. Usare al primo avvio, quando l'utente carica un nuovo CV o dice "aggiorna il mio profilo".
---

# Onboarding e intervista

Obiettivo: creare `profilo/master.yaml` (schema in `templates/master.example.yaml`), la **unica fonte di verità**
per tutte le altre skill. Niente in questo file deve essere dedotto senza conferma dell'utente.

## Passi
1. Leggi i file in `profilo/` (CV PDF/DOCX, PDF del profilo LinkedIn o export dati). Estrai esperienze,
   formazione, certificazioni, lingue, progetti. Assegna a ogni fatto un ID stabile (`exp1`, `exp1.b1`, `sk.python`).
2. Mostra all'utente un riepilogo e segnala le **incongruenze** tra CV e LinkedIn (date, titoli): chiedi quale è corretta.
3. Intervista, **poche domande alla volta** (max 3-4 per messaggio), in quest'ordine:
   - Risultati misurabili per ogni esperienza (numeri, %, budget, team). Se l'utente non ricorda un numero, NON stimarlo.
   - Livello reale di ogni competenza: `esperto | quotidiano | base | studiata`, con un'evidenza concreta.
   - Competenze complementari assenti dal CV: strumenti, side project, volontariato, soft skill con un esempio.
   - Preferenze: ruoli target, seniority, città / remoto / ibrido, RAL minima, contratto, preavviso, settori esclusi.
   - Dati da form: permesso di lavoro, trasferimento, trasferte, patente, data di disponibilità.
   - Banca risposte: risposte standard alle domande di screening frequenti (anni di esperienza per tecnologia,
     "perché vuoi cambiare", aspettative economiche, ecc.).
4. Salva in `profilo/master.yaml`, marcando `confermato: true` solo ciò che l'utente ha confermato.
5. Chiedi anche l'elenco di aziende target per `profilo/aziende.yaml` (nome + URL career page).

## Regole
- Mai inventare, arrotondare per eccesso o "migliorare" un fatto.
- Se una risposta è vaga, chiedi un esempio concreto.
- I dati restano in locale: non inviarli a servizi esterni.
