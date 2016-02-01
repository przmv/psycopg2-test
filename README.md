Simple tests for PostgreSQL types adaptation in psycopg2.

Requirements:

* [Docker Engine](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Run tests:

```console
$ docker-compose up -d db   # Start PostgreSQL database server
$ docker-compose build      # Build Docker container with tests
$ docker-compose run tests  # Run tests from Docker container
```
