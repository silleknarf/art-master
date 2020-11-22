FROM node:10

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn --check-files

COPY . .

CMD yarn start