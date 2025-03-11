ARG GPU_LIST=hosts.yaml

FROM python:3-alpine


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ${GPU_LIST} .

CMD python coordinator.py --period ${PROBE_PERIOD} --hosts ${GPU_LIST} --verbosity ${VERBOSITY}
