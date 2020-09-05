FROM python:3.9-rc-alpine

RUN pip install --no-cache-dir iteround==1.0.2

ADD ./src /src

WORKDIR /src

RUN pip install .
