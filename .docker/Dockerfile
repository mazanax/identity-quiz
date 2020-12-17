FROM node:latest as frontend-build-stage
ARG APP_SITE_HOST=''
ARG VK_CLIENT_ID
ARG FB_CLIENT_ID
ARG GOOGLE_CLIENT_ID

WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN VUE_APP_SITE_HOST=$APP_SITE_HOST \
    VUE_APP_VK_CLIENT_ID=$VK_CLIENT_ID \
    VUE_APP_FB_CLIENT_ID=$FB_CLIENT_ID \
    VUE_APP_GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
    ./node_modules/.bin/vue-cli-service build

###

FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine as backend-build-stage
ARG APP_SITE_HOST=''

ARG POSTGRES_DB_NAME=''
ARG POSTGRES_DB_USER=''
ARG POSTGRES_DB_PASS=''
ARG POSTGRES_DB_HOST=''
ARG POSTGRES_DB_PORT='5432'

ARG VK_CLIENT_ID
ARG VK_CLIENT_SECRET
ARG FB_CLIENT_ID
ARG FB_CLIENT_SECRET
ARG GOOGLE_CLIENT_ID
ARG GOOGLE_CLIENT_SECRET

## Environment variables

ENV POSTGRES_DB_NAME=$POSTGRES_DB_NAME
ENV POSTGRES_DB_USER=$POSTGRES_DB_USER
ENV POSTGRES_DB_PASS=$POSTGRES_DB_PASS
ENV POSTGRES_DB_HOST=$POSTGRES_DB_HOST
ENV POSTGRES_DB_PORT=$POSTGRES_DB_PORT

ENV APP_SITE_HOST=$APP_SITE_HOST

ENV VK_CLIENT_ID=$VK_CLIENT_ID
ENV VK_CLIENT_SECRET=$VK_CLIENT_SECRET
ENV FB_CLIENT_ID=$FB_CLIENT_ID
ENV FB_CLIENT_SECRET=$FB_CLIENT_SECRET
ENV GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
ENV GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

RUN mkdir -p /app/static/js /app/static/css
COPY --from=frontend-build-stage /app/dist/js /app/static/js
COPY --from=frontend-build-stage /app/dist/css /app/static/css
COPY --from=frontend-build-stage /app/dist/img /app/static/img
COPY --from=frontend-build-stage /app/dist/index.html /app/templates/index.html
COPY --from=frontend-build-stage /app/dist/favicon.ico /app/static/favicon.ico
COPY --from=frontend-build-stage /app/dist/logo.jpg /app/static/logo.jpg

RUN sed -i 's/img\//static\/img\//g' $(ls /app/static/js/app*js)
RUN sed -i 's/\/css\//\/static\/css\//g' /app/templates/index.html
RUN sed -i 's/\/js\//\/static\/js\//g' /app/templates/index.html
COPY . /app
RUN mv /app/.docker/config/uwsgi.ini /app/uwsgi.ini

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache jpeg-dev && \
 apk add --no-cache freetype-dev && \
 apk add --no-cache libjpeg && \
 apk add --no-cache zlib-dev && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt && \
 apk --purge del .build-deps