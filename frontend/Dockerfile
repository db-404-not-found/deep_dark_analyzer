FROM node:20-alpine

WORKDIR /usr/local/analyzer

COPY ./src .

RUN npm install

CMD ["npm", "run", "dev"]