FROM node:20-alpine as build

WORKDIR /usr/local/analyzer
ARG VITE_API_URL=http://127.0.0.1:80/
COPY ./frontend/src/package.json .

RUN npm install

COPY ./frontend/src .

RUN npm run build

FROM nginx:alpine
COPY --from=build /usr/local/analyzer/dist /dist

RUN mkdir -p /var/logs/nginx/backend/ && rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/