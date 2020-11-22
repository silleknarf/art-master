FROM node:10

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn --check-files

COPY . .

RUN yarn build

FROM node:10

COPY --from=0 /artmaster/build /build

RUN yarn global add serve

CMD serve -s /build