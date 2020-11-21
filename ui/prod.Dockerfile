FROM node:10

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn --check-files

COPY . .

RUN yarn build

RUN yarn global add serve

CMD serve -s build