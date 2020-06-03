![Quality Assuracen Platform](https://qualitysphere.github.io/images/qap.png)

# Quality Sphere

##### English | [中文](README.cn.md)

> Open source software for quality assurance platform

[![org](https://img.shields.io/static/v1?style=for-the-badge&label=org&message=Truth%20%26%20Insurance%20Office&color=597ed9)](http://bx.baoxian-sz.com)
![author](https://img.shields.io/static/v1?style=for-the-badge&label=author&message=v.stone@163.com&color=blue)
![license](https://img.shields.io/github/license/QualitySphere/qsphere?style=for-the-badge)
[![python](https://img.shields.io/static/v1?style=for-the-badge&logo=python&label=Python&message=3.7&color=3776AB)](https://www.python.org)
![flask](https://img.shields.io/static/v1?style=for-the-badge&logo=Flask&label=flask&message=1.1.1&color=000000)
[![vue](https://img.shields.io/static/v1?style=for-the-badge&logo=Vue.js&label=Vue.js&message=2.6.11&color=4FC08D)](https://vuejs.org)
[![element](https://img.shields.io/static/v1?style=for-the-badge&logo=css3&label=element&message=2.13.0&color=579EF8)](https://element.eleme.cn/#/en-US/component/icon)
[![grafana](https://img.shields.io/static/v1?style=for-the-badge&logo=Grafana&label=grafana&message=6.3.6&color=F46800)]()
[![postgresql](https://img.shields.io/static/v1?style=for-the-badge&logo=PostgresQL&label=postgresql&message=10&color=336791)]()
[![docker](https://img.shields.io/static/v1?style=for-the-badge&logo=docker&label=docker&message=bxwill/qsphere&color=2496ED)](https://hub.docker.com/r/bxwill/qsphere)

## Preview

![Tracker](https://qualitysphere.github.io/images/tracker.png)
![Project](https://qualitysphere.github.io/images/project.png)
![Sprint](https://qualitysphere.github.io/images/sprint.png)
![Dashboard](https://qualitysphere.github.io/images/dashboard.png)

## Vision

**EASY METRICS EASY MANAGEMENT**

**CHANGE DATA TO HEALTH INDEX VIA QUALITY ASSURANCE MANAGEMENT SHARING**

## Framework

#### Component

![Framework](https://qualitysphere.github.io/images/framework.svg)

#### Database

![Database](https://qualitysphere.github.io/images/database.svg)

## API Document

http://{qsphere-server}/api/ui

## Quick Start

#### Deploy/Upgrade QSphere

```bash
docker-compose -f docker-compose.yaml pull
docker-compose -f docker-compose.yaml up -d
```

> docker-compose.yaml

```yaml
version: "3"
services:
  qsphere-db:
    container_name: qsphere-db
    image: postgres:10
    restart: always
    environment:
      POSTGRES_DB: 'qsphere'
      POSTGRES_PASSWORD: 'password'
    volumes:
      - ./qsphere-pgdata:/var/lib/postgresql/data
    command: ["-c", "max_connections=2000"]
  qsphere-svc:
    container_name: qsphere-svc
    image: bxwill/qsphere:svc-latest
    restart: always
    ports:
      - 6001:6001
    environment:
      PG_DB: 'qsphere'
      PG_SERVER: qsphere-db
      PG_USER: 'postgres'
      PG_PASSWORD: 'password'
    depends_on:
      - qsphere-db
  qsphere-grafana:
    container_name: qsphere-grafana
    image: bxwill/qsphere:grafana-latest
    restart: always
    ports:
      - 3000:3000
    environment:
      PG_DB: 'qsphere'
      PG_SERVER: qsphere-db
      PG_PORT: '5432'
      PG_USER: 'postgres'
      PG_PASSWORD: 'password'
    depends_on:
      - qsphere-db
      - qsphere-svc
  qsphere-ui:
    container_name: qsphere-ui
    image: bxwill/qsphere:ui-latest
    restart: always
    ports:
      - 8080:80
    depends_on:
      - qsphere-svc
      - qsphere-grafana
```

#### Config QSphere

- Bind tracker
- Add project
- Add sprint

#### Check data graph

## Changelog

- 1.0.0 - `2020-06-01`
  - UI rewrite
  - Change database models
  - Improve service API data
  - Data graph change to project/sprint
  - Add Portal menu
  - Remove VM online check function

- 0.9.0 - `2019-12-31`
  - Enhance UI

- 0.2.0 - `2019-10-23`
  - Support to update JIRA connection info
  - Support to update Sprint info
  - Support to disable/active Sprint
  - Support to VM online check

- 0.1.0 - `2019-10-14`
  - Get and analyze JIRA data, show graph via Grafana
  - Support JIRA
  - Support to add Project/Sprint
  - Support data graph 
  - Support API swagger

## More

- Homepage: https://QualitySphere.github.io
- GitHub: https://github.com/QualitySphere/qsphere
- Docker: https://hub.docker.com/r/bxwill/qsphere

