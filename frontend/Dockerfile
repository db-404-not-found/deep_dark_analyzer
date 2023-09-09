FROM node:20-alpine

WORKDIR /usr/local/analyzer

COPY ./src .

RUN npm install

RUN npm run build 

CMD ["npm", "run", "dev"]