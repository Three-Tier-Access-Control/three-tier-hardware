# Three Tier Hardware

Change pin factory

```sh
export GPIOZERO_PIN_FACTORY=native
```
Install command

```sh
pip install -r requirements.txt
```


## run on localhost

```sh
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

```sh
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```
