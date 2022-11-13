# django skeleton

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Documentation: ###

* [Architecture overview](src/docs/architecture_overview.md)
* [Backend: Pre-commit hook](src/docs/pre_commit_hook.md)

### API documentation: ###

* ReDoc web UI: [http://localhost:9000/_platform/docs/v1/redoc/](http://localhost:9000/_platform/docs/v1/redoc/)
* Swagger web UI: [http://localhost:9000/_platform/docs/v1/swagger/](http://localhost:9000/_platform/docs/v1/swagger/)
* Swagger JSON: [http://localhost:9000/_platform/docs/v1/swagger.json](http://localhost:9000/_platform/docs/v1/swagger.json)
* Swagger YAML: [http://localhost:9000/_platform/docs/v1/swagger.yaml](http://localhost:9000/_platform/docs/v1/swagger.yaml)

### Small Information about project: ###

In this application We removed Dockerfile because it is gets long time for build,
and for restart app. Because we need to do docker-compose down/up when we restart app.
And we need to build each time when we add new requirements for our project.
And for that purpose I am not containerized main app in dockerfile 
instead we start django app in terminal and other component will run with docker-compose.


### First run: ###
Our application runs with 2 step

### Firsts step ###

Create virtual environment, and install Python requirements:

```bash
pip install -r requirments-dev.txt
```

Run backing services (require Docker & docker-compose):

```bash
docker-compose up -d
```

Run migrations:

```bash
python manage.py migrate
```

Run Django server:

```bash
python manage.py runserver 0.0.0.0:9000
```


### Second step ###

Open new terminal window for celery, and enter this command 

```bash
celery -A src worker -l INFO -f celery.logs
```


### Run Tests : ###

For run tests 

```bash
pytest --cache-clear --no-migrations --disable-warnings
```

For run tests with test coverage info

```bash
pytest --cache-clear --capture=no --showlocals --verbose --cov=src --cov-report term-missing --cov-fail-under=100 --no-migrations --disable-warnings
```

