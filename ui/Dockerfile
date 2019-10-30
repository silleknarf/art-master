FROM node:10

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn

COPY . .

CMD yarn start