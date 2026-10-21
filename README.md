# DevOps Capstone Project: Customer Accounts Microservice

[![CI Build](https://github.com/PranavJagtap03/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/PranavJagtap03/devops-capstone-project/actions/workflows/ci-build.yaml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://www.python.org/)

## Overview

This project is the Capstone Project for the **IBM DevOps and Software Engineering Professional Certificate**. The project develops and manages a **Customer Accounts Microservice** using modern DevOps practices, including:
- **Agile Planning & Scrum:** User stories, estimation, and sprint management via ZenHub / GitHub Projects Kanban board.
- **RESTful API Development:** Built with Python and Flask following REST architectural design and Test-Driven Development (TDD).
- **Automated Testing & Code Quality:** Automated testing with `nosetests`, code coverage tracking, and linting with `flake8` and `pylint`.
- **Continuous Integration (CI):** Fully automated GitHub Actions workflow verifying syntax and passing all test suites.
- **Security Engineering:** Secure HTTP headers with `Flask-Talisman` and Cross-Origin Resource Sharing with `Flask-CORS`.
- **Containerization & Orchestration:** Microservice containerized via Docker and deployed to a Kubernetes cluster.
- **Continuous Delivery (CD):** Automated pipeline orchestration using Tekton.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root info & service health |
| `GET` | `/health` | Service health status |
| `POST` | `/accounts` | Create a new customer account |
| `GET` | `/accounts` | List all customer accounts |
| `GET` | `/accounts/<id>` | Read details of an account by ID |
| `PUT` | `/accounts/<id>` | Update existing account by ID |
| `DELETE` | `/accounts/<id>` | Delete an account by ID |

## Project Setup & Local Development

### 1. Prerequisites
- Python 3.9+
- PostgreSQL or SQLite
- Docker (optional for containerization)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running Unit Tests
```bash
nosetests
```

### 4. Running the Service
```bash
gunicorn --bind 0.0.0.0:8080 --log-level info service:app
```
