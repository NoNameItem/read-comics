FROM node:16.19 as builder
WORKDIR /app

ARG FONTAWESOME_AUTH_TOKEN
ENV FONTAWESOME_NPM_AUTH_TOKEN=$FONTAWESOME_AUTH_TOKEN

COPY . /app

RUN yarn
RUN yarn build

ENTRYPOINT ["yarn", "preview"]

FROM nginxinc/nginx-unprivileged:1.23-alpine
COPY --from=builder --chown=nginx:root /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY deploy/nginx/nginx.conf /etc/nginx/conf.d

COPY --chown=nginx:root deploy/replace_vars.sh deploy/entrypoint.sh /
RUN chmod +x replace_vars.sh /entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]