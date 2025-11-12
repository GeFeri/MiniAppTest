# === Stage 1: build frontend ===
FROM node:20-alpine AS builder
WORKDIR /app

# копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm ci

# копируем исходники
COPY . .
RUN npm run build

# === Stage 2: prepare static nginx files ===
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
