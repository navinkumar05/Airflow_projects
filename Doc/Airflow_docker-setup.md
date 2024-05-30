# Running Airflow in Docker

Create directory

```bash
mkdir Airflow_Docker_setup
```

> Note: Here after run all commands inside `Airflow_Docker_setup` directory

## Fetching `docker-compose.yaml`

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'
```

## LocalExecutor setup

in `docker-compose.yaml` file

```yaml

# line no 56
    AIRFLOW__CORE__EXECUTOR: LocalExecutor

# command 
    # redis:
    #   condition: service_healthy

# --------------------------------------------------------------------------------------------

  # redis:
  #   # Redis is limited to 7.2-bookworm due to licencing change
  #   # https://redis.io/blog/redis-adopts-dual-source-available-licensing/
  #   image: redis:7.2-bookworm
  #   expose:
  #     - 6379
  #   healthcheck:
  #     test: ["CMD", "redis-cli", "ping"]
  #     interval: 10s
  #     timeout: 30s
  #     retries: 50
  #     start_period: 30s
  #   restart: always

# --------------------------------------------------------------------------------------------

  # airflow-worker:
    # <<: *airflow-common
    # command: celery worker
    # healthcheck:
    #   # yamllint disable rule:line-length
    #   test:
    #     - "CMD-SHELL"
    #     - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}" || celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
    #   interval: 30s
    #   timeout: 10s
    #   retries: 5
    #   start_period: 30s
    # environment:
    #   <<: *airflow-common-env
    #   # Required to handle warm shutdown of the celery workers properly
    #   # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
    #   DUMB_INIT_SETSID: "0"
    # restart: always
    # depends_on:
    #   <<: *airflow-common-depends-on
    #   airflow-init:
    #     condition: service_completed_successfully

# --------------------------------------------------------------------------------------------

  # You can enable flower by adding "--profile flower" option e.g. docker-compose --profile flower up
  # or by explicitly targeted on the command line e.g. docker-compose up flower.
  # See: https://docs.docker.com/compose/profiles/
  # flower:
  #   <<: *airflow-common
  #   command: celery flower
  #   profiles:
  #     - flower
  #   ports:
  #     - "5555:5555"
  #   healthcheck:
  #     test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
  #     interval: 30s
  #     timeout: 10s
  #     retries: 5
  #     start_period: 30s
  #   restart: always
  #   depends_on:
  #     <<: *airflow-common-depends-on
  #     airflow-init:
  #       condition: service_completed_successfully

```

## commands

up the container

```bash
docker-compose up -d
```

Down the continer

```bash
docker-compose down
```

view the running docker images or running instance

```bash
docker ps
```

## AWS cli setup in airflow to store the data frame result:

### For `LocalExecutor`
if you run the airflow in `LocalExecutor` perform these below action on `airflow_docker_setup-airflow-scheduler-1` container

```bash
# airflow_docker_setup-airflow-scheduler-1 - interactive mode
docker exec -it -u root ab70e0d73819 /bin/bash
```

```bash
apt update

apt install -y awscli
aws configure

groupadd airflow
useradd -m -g airflow airflow
mkdir -p /home/airflow/.aws
cp /root/.aws/credentials /home/airflow/.aws/credentials
cp /root/.aws/config /home/airflow/.aws/config
chown -R airflow:airflow /home/airflow/.aws

#verify
su - airflow
cat ~/.aws/credentials
cat ~/.aws/config
```

### For `CeleryExecutor`
do the same step in `airflow-worker` container