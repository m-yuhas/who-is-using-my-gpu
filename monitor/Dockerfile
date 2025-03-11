FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD [ "flask", "--app", "monitor", "run", "--host=0.0.0.0" ]

# TODO: Parameterize CUDA Driver Version
