FROM node:20-alpine

WORKDIR /usr/local/analyzer

COPY ./src/package.json .

RUN npm install

COPY ./src .

RUN npm run build 