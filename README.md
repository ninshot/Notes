# FASTAPI Backend with JWT Authentication, PostgreSQL, Docker, and Isolated Test Environment

This project is a backend service built with **FastAPI**, **PostgreSQL**, **RESTful APIS** and **DOCKER**. It allows users to create notes, delete notes and update notes.
The appilcation follows modern backend engineering practices including containeraization.
---

---
## TECH STACK

### BACKEND
* PYTHON 3.14+
* FastAPI
* PostgresSQL 16
* SQLAlchemy (async)

### AUTHENTICATION
* JWT (PyJWT)
* Oauth2

### TESTING
* pytest

### DEVOPS
* Docker
* Docker Compose
---
## Installation
### Prerequisites
- Docker
- Git

1. Clone the repository
   Run `git clone https://github.com/ninshot/Notes.git`

2. Build the Containers
   Run `docker compose up --build`

Now the app is running on http://localhost:8000 or you can use http://localhost:8000/docs for interactive docs to interact with the backend.

## RUNNING TESTS
All the tests are in test directory. To run the test_cases run the following command.
Run `docker compose run --rm test-runner`

This will run all the test cases in an isolated environment using test database.

## AUTHOR
Aman Mansuri
Computer Science Student
  


