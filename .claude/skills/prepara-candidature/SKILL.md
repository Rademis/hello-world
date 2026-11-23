---
name: prepara-candidature
description: Esegue la pipeline sulle offerte che l'utente ha selezionato nella dashboard (stato "selezionata") - CV su misura, lettera motivazionale, poi invio automatico se il canale è un portale esterno, oppure stato "pronta_linkedin" con link per l'invio manuale su LinkedIn. Usare quando l'utente scrive /prepara-candidature, preme "Prepara ora" o dalla routine giornaliera.
---

# Pipeline sulle offerte selezionate

Per ogni riga di `data/jobs.sqlite` con `stato='selezionata'`, una alla volta, ordinate per `match`:

1. `stato='in_preparazione'`.
2. Esegui `adatta-cv` → `data/applications/<id>/CV_*.pdf` (con verifica indipendente).
3. Esegui `lettera-motivazionale` → `Lettera_*.pdf` + `lettera.txt`.
4. Prepara `risposte.md`: le probabili domande del form con le risposte dalla `banca_risposte`
   (utile anche per l'invio manuale su LinkedIn).
5. Smista per canale (`tipo_candidatura`):
   - **`linkedin`** → NON aprire LinkedIn. `stato='pronta_linkedin'`. La dashboard mostra "Apri su LinkedIn"
     e i documenti da caricare; l'utente invia e preme "Segna inviata".
   - **portale esterno** (`greenhouse | lever | ashby | workday | altro`) → esegui `invia-candidatura`.
     Se `config.invio.approvazione` è `sempre`, fermati a `stato='pronta'` e attendi; altrimenti invia.
6. Se una fase fallisce o serve l'utente → `stato='in_attesa'` con il motivo in `nota_stato`.

7. Poi, per le righe con `stato='approvata'` (l'utente ha premuto "Approva invio" nella dashboard),
   esegui `invia-candidatura`.

Alla fine scrivi un riepilogo breve: preparate, inviate, pronte per LinkedIn, in attesa.
