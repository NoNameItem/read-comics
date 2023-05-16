FROM node:16.18 as builder
WORKDIR /app
COPY . /app
RUN yarn
RUN yarn build

FROM nginxinc/nginx-unprivileged:1.23-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx/nginx.conf /etc/nginx/conf.d

COPY --chown=nginx:root deploy/envs.js /usr/share/nginx/html/envs.js

COPY --chown=nginx:root deploy/replace_vars.sh deploy/entrypoint.sh /
RUN chmod +x replace_vars.sh /entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
