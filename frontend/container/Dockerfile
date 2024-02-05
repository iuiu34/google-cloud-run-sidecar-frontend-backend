FROM node:16-alpine as build
#RUN npm install -g npm@10.4.0

WORKDIR /app

COPY package.json package.json
RUN npm install

COPY src/ src/
COPY public/ public/
COPY tsconfig.json tsconfig.json

RUN npm run build

# Use nginx to serve the static content
FROM nginx:stable-alpine

COPY --from=build /app/build /usr/share/nginx/html
# proxy to the backend
COPY default.conf /etc/nginx/conf.d/default.conf

COPY container/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80
ENV PORT 80
#ENTRYPOINT ["nginx", "-g", "daemon off;"]
ENTRYPOINT ["/entrypoint.sh"]