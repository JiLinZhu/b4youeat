# b4youeat – Backend

A minimal **Python gRPC + PostgreSQL** backend for the _b4youeat_ food-blog project, ready to pair with a React (gRPC-Web / Connect-Web) front-end.

---

## Stack

| Layer             | Tech used                                         |
| ----------------- | ------------------------------------------------- |
| Language          | **Python 3.12**                                   |
| RPC               | gRPC (aio) – `grpcio` / `grpcio-tools`            |
| ORM / DB          | SQLAlchemy 2 (Async) + **PostgreSQL 15**          |
| Protobuf stubs    | `scripts/generate_protos.sh` → `b4youeat/proto/…` |
| Container runtime | Docker / **docker-compose**                       |
| Config management | `b4youeat/configs/*.ini` (+ dotenv / env vars)    |

---

## Local quick-start

```bash
pyenv local 3.12.3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# generate / re-generate protobuf stubs
python -m b4youeat.protobuf

# run the database + gRPC server
docker compose up --build
#  ↳ Postgres  :5433  (user: app / pw: secret)
#  ↳ gRPC      :50051
```

## Manual run without Docker

```bash
# Postgres running locally on 5432 (or edit DB_URL)
source .venv/bin/activate
python -m b4youeat.main
```
