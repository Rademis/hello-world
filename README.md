# Agente candidature (LinkedIn + portali ATS)

Agente basato su Claude Code che, partendo da CV e profilo LinkedIn, intervista l'utente, cerca offerte
compatibili ogni giorno, genera CV e lettere su misura senza invenzioni e invia le candidature.

- Progetto e ricerca: [docs/PROGETTO.md](docs/PROGETTO.md)
- Skill: [.claude/skills/](.claude/skills/)
- Template profilo/config: [templates/](templates/)

Dashboard: `python3 dashboard/server.py` → http://127.0.0.1:8765
(demo: `python3 dashboard/demo_seed.py && python3 dashboard/server.py --db data/demo.sqlite`)

Avvio rapido: metti il CV in `profilo/`, poi in Claude Code chiedi "avvia l'onboarding".
