---
name: lettera-motivazionale
description: Scrive una lettera motivazionale su misura per un'offerta, basata solo su fatti di profilo/master.yaml e su informazioni pubbliche verificabili dell'azienda, con verifica indipendente. Usare dopo adatta-cv o quando l'utente chiede una cover letter.
---

# Lettera motivazionale

1. Ricerca breve sull'azienda (sito ufficiale, pagina careers, notizie recenti): 1-2 elementi specifici,
   annotando la fonte in `data/applications/<id>/fonti_azienda.md`.
2. Struttura (200-300 parole, lingua dell'annuncio, tono da `config.tono_lettera`):
   - apertura: ruolo e motivo specifico per questa azienda;
   - 2 paragrafi: i 2-3 requisiti principali dell'annuncio collegati a fatti concreti (con ID nella bozza);
   - chiusura: disponibilità, nessuna formula generica.
3. Stessa verifica del CV tramite subagent (affermazioni su di te → master.yaml; affermazioni sull'azienda → fonti).
4. Se `preferenze.motivazioni` contiene note dell'utente, usale; non inventare entusiasmi o legami personali.
5. Esporta PDF e salva anche il testo semplice (`lettera.txt`) per i campi di testo dei portali.
