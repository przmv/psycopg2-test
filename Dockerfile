FROM alpine

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    postgresql-dev \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt /app/
RUN virtualenv /env \
  && /env/bin/pip install -r /app/requirements.txt

COPY . /app/

CMD ["/env/bin/python", "-m", "unittest", "discover", "-v"]
