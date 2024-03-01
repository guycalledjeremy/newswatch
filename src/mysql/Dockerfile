FROM python:3.10-slim-bookworm

RUN apt-get update \
  && apt-get install pkg-config -y \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  default-libmysqlclient-dev build-essential\
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 3060

CMD [ "python3", "server.py" ]