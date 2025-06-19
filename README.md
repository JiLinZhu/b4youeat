# b4youeat – Backend

A **Python gRPC + PostgreSQL** backend for the _b4youeat_ food-blog project, ready to pair with a React (gRPC-Web / Connect-Web) front-end.

---

## Stack

| Layer             | Tech used                                      |
| ----------------- | ---------------------------------------------- |
| Language          | **Python 3.12**                                |
| RPC               | gRPC (aio) – `grpcio` / `grpcio-tools`         |
| ORM / DB          | SQLAlchemy 2 (Async) + **PostgreSQL 15**       |
| Protobuf Stubs    | b4youeat.protobuf                              |
| Container runtime | Docker / **docker-compose**                    |
| Config management | `b4youeat/configs/*.ini` (+ dotenv / env vars) |

---

```bash
pyenv local 3.12.3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m b4youeat.protobuf

docker compose up --build

docker compose run --rm server python -m scripts.create_tables

docker compose run --rm server python -m scripts.bootstrap_reviews

```
