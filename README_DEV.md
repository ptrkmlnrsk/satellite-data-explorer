Console:
http://localhost:9001

S3 API:
http://localhost:9000

Endpoint from host/WSL/QGIS:
127.0.0.1:9000

Endpoint from Docker container:
minio:9000


---Kontenery---
```docker compose build satellite app``` - buduje jeszcze raz kontener
```docker compose exec satellite-app uv run python -m src.storage_utils.img_uploader``` - odpala skrypt który znajduje się w kontenerze (jako moduł)
```docker compose exec satellite-app bash``` - wejscie do basha contenera
```docker inspect satellite-data-explorer-satellite-app-1``` - info o kontenerze


```uv add <package name>``` - z poziomu terminala i folderu na Windows dodaje paczke




---Taski---

Prometheus + grafana

Jak postawic sentry

Poczytac o loggerze

Popytac basha,

podzielic np na dwie sieci

zrobic dwie aplikacje
z jednego kontenera odpytywac drugi

pub sub

istio
