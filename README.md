# AEGIS HEALTH

A student healthcare-assistant demo built with Python and Streamlit.

Features: login and sign up, symptom checker, medical Q&A, medicine reminders,
hospital finder, and PDF/JSON reports.

## Run it on a Mac

```bash
git clone https://github.com/YOUR-USERNAME/aegis-health.git
cd aegis-health
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Then open http://localhost:8501

## Folder structure

- `app.py` starts the app
- `aegis/` has the code (database, login, symptom checker, reports, pages)
- `data/` is created automatically and holds the local database (not uploaded to GitHub)

## Important

- This is a demo project, not a medical product. It does not give a real diagnosis.
- Hospital data is demo data. Verify details before relying on it.
- Do not store real patient data in it.