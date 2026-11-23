# Agente candidature

Progetto descritto in `docs/PROGETTO.md`. Le fasi sono skill in `.claude/skills/`.

Regole non negoziabili:
- `profilo/master.yaml` è l'unica fonte di verità: nessun CV, lettera o risposta a form può contenere
  affermazioni non supportate da quel file.
- Mai inviare candidature su LinkedIn: solo stato `pronta_linkedin`, l'utente invia a mano.
- Mai aggirare CAPTCHA o controlli di sicurezza; mai indovinare risposte a domande di screening.
- Rispettare `profilo/config.yaml` (soglie, limiti giornalieri, modalità di approvazione).
- `profilo/` e `data/` contengono dati personali: non committarli e non inviarli a servizi esterni.
