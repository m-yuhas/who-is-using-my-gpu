ARG GPU_LIST=hosts.yaml

FROM python:3-alpine

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del build-deps

COPY . .
COPY ${GPU_LIST} .

CMD python coordinator.py --period ${PROBE_PERIOD} --hosts ${GPU_LIST} --verbosity ${VERBOSITY}
