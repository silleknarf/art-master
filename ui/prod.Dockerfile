FROM node:10 as build

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn --check-files

COPY . .

RUN yarn build

FROM node:10

COPY --from=build /artmaster/build /build

RUN yarn global add serve

CMD serve -s /build