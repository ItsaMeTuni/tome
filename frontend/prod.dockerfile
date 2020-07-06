FROM node:lts-buster AS builder

WORKDIR /app

COPY . .

RUN npm install && npm run build

FROM nginx

COPY --from=builder /app/dist /usr/share/nginx/html
