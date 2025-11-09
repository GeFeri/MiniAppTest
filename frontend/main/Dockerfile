# --- Stage 1: build ---
FROM node:20-alpine AS builder
WORKDIR /app

# копируем package.json из папки main
COPY frontend/main/package*.json ./
RUN npm ci

# копируем остальной проект
COPY frontend/main/ .

# сборка production-билда
RUN npm run build

# --- Stage 2: Nginx для отдачи статики ---
FROM nginx:1.25-alpine

# копируем билд из предыдущего этапа
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
