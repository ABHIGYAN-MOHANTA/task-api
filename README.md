# Task API

Task API is a lightweight Python Flask application developed for the GitOps delivery platform demo. It serves a simple HTTP endpoint and exposes custom Prometheus metrics for automated canary analysis and load-based autoscaling.

## Architecture

*   **Framework:** Python 3 with Flask
*   **Metrics:** `prometheus_client` library
*   **Containerization:** Docker
*   **CI/CD:** Jenkins (build/test/push) -> Argo CD (deploy) -> Argo Rollouts (canary)

## Endpoints

### `GET /`
The main application endpoint.
*   **Returns:** `Hello, World!`
*   **Metrics:** Each call increments the `http_requests_total` metric.

### `GET /metrics`
The Prometheus metrics scraping endpoint.
*   **Returns:** Standard Prometheus metrics along with `http_requests_total`.
*   **Content-Type:** `text/plain; version=0.0.4; charset=utf-8` (required by Prometheus).

## Metrics & Autoscaling

The application is instrumented to track the total number of HTTP requests. This metric (`http_requests_total`) is central to the platform's advanced deployment features:

1.  **Canary Analysis (Argo Rollouts):** During a deployment, an `AnalysisTemplate` queries the request rate. If the new canary pods are successfully serving traffic (rate > 0), the rollout proceeds.
2.  **Event-Driven Autoscaling (KEDA):** A KEDA `ScaledObject` monitors the HTTP request rate across all pods. If the rate exceeds 10 requests per second per pod, it triggers the cluster to scale up the deployment.

## Development & CI

This repository contains a `Jenkinsfile` configuring a declarative CI pipeline.
When code is pushed to the `main` branch, Jenkins:
1. Builds a new Docker image labeled with the Jenkins build number.
2. Pushes the image to Docker Hub (`abhigyanmohanta/task-api`).
3. Updates the `application.yaml` manifest in the central GitOps repository to trigger an ArgoCD deployment.
