# Three Tier Hardware

Change pin factory

`export GPIOZERO_PIN_FACTORY=native`

Install command

`pip install -r requirements.txt`

Run command

`uvicorn app.main:app --host 0.0.0.0 --port 8000`
