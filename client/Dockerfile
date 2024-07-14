FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm cache clean --force && npm install

COPY . .

RUN npm run build

CMD ["npm", "run", "dev"]
