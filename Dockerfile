FROM nginx:alpine
RUN apk add --no-cache bash
COPY . /usr/share/nginx/html
