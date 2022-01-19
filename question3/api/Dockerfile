FROM python:3.10.1-alpine

WORKDIR /api
RUN apk update \
    && apk add build-base
COPY . .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["/bin/sh", "/api/runner.sh"]