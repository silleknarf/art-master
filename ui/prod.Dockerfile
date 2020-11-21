FROM node:10

WORKDIR /artmaster

COPY package.json ./

COPY yarn.lock ./

RUN yarn --check-files

COPY . .

RUN yarn build

FROM nginx

COPY --from=0 /artmaster/build /usr/share/nginx/html