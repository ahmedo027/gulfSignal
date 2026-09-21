# GulfSignal 
Run on Windows: install Python 3.10+, open PowerShell in this folder, run `python app.py`, then open http://localhost:8000. The app uses SQLite,  roles, transparent scoring, location filters, CV upload flow, direct company links, and application tracking. It runs without API keys and deliberately avoids LinkedIn scraping.

Live company feeds use public Greenhouse and Lever postings. Set `GREENHOUSE_BOARDS` and `LEVER_ACCOUNTS` as comma-separated public board identifiers before starting the server; empty variables keep the  jobs.

