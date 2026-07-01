ARG NODE_VERSION=22-slim

# Build stage
FROM node:${NODE_VERSION} AS build

RUN corepack enable && corepack prepare pnpm@10.23.0 --activate

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN pnpm build


# Production stage
FROM node:${NODE_VERSION} AS production

RUN corepack enable && corepack prepare pnpm@10.23.0 --activate

WORKDIR /app

ENV NODE_ENV=production

# Copy built application
COPY --from=build /app/.output ./.output

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
