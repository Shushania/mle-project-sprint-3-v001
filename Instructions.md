# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение
##### Настройка виртуального окружения: 
```
python3 -m venv ./venv
source .venv/bin/activate
pip install -r requirements.txt
```
##### Запуск сервиса: 
```
cd services
uvicorn app.main:app
```
##### API: 
```
http://127.0.0.1:8000/docs - дока
http://127.0.0.1:8000/service-status - проверка работоспособности
http://127.0.0.1:8000/predict - принимает мараметры, отдает результат работы модели 
http://127.0.0.1:8000/test - генерация случайных параметров для проверки работоспособности
```

### 2. FastAPI микросервис в Docker-контейнере

##### Dockerfile:
```
cd services
docker build . --tag my_image:0
docker container run -p 8000:8000 my_image:0
```
CHECK: 
```
curl http://127.0.0.1:8000/test
```

##### Docker compose:
```
cd services
docker compose build
docker compose up
```
CHECK: 
```
curl http://127.0.0.1:8000/test
```

### 3. Запуск сервисов для системы мониторинга
Отсюда, надо добавить в файл .env параметры, чтобы отделить работу первых двух пунктов а отследующих: 
```
FLG=true

GRAFANA_USER=
GRAFANA_PASS=
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```
и запустить докер 
```
cd services
docker compose build
docker compose up
```
Grafana: http://localhost:3000
Prometheus: http://localhost:9090
