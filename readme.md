# Flask API Monitoring Stack

A monitoring application using:

- Python Flask
- Prometheus
- Grafana
- Docker Compose

## Requirements

- Docker
- Docker Compose

## Start the application

Run:

docker compose up -d --build

## Application URLs

Flask:
http://localhost:5000

Health:
http://localhost:5000/health

Prometheus Metrics:
http://localhost:5000/metrics

Prometheus Dashboard:
http://localhost:9090

Grafana Dashboard:
http://localhost:3000

## Grafana Credentials

Username: admin
Password: admin

## Test API

Successful request:

curl http://localhost:5000/api/success

Error request:

curl http://localhost:5000/api/error

## Stop application

docker compose down

## Remove persistent data

docker compose down -v