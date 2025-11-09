import axios from "axios";
import WebApp from "@twa-dev/sdk";

// Базовый инстанс
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL?.replace(/\/+$/, "") || "http://localhost:8000/api",
  withCredentials: false,
  headers: { "Content-Type": "application/json" },
});

// Хелпер: положим tg данные в localStorage один раз при старте приложения
export function syncTelegramUserToStorage() {
  try {
    const tgUser = WebApp?.initDataUnsafe?.user;
    if (tgUser?.id) {
      localStorage.setItem("tg_id", String(tgUser.id));
      if (tgUser.username) localStorage.setItem("tg_username", tgUser.username);
    }
  } catch { /* ignore */ }
}

// Интерсептор: добавляем X-Telegram-Id/Username к каждому запросу
api.interceptors.request.use((config) => {
  const tgId = localStorage.getItem("tg_id");
  const tgUsername = localStorage.getItem("tg_username");
  if (tgId) config.headers.set("X-Telegram-Id", tgId);
  if (tgUsername) config.headers.set("X-Telegram-Username", tgUsername);
  return config;
});

// Удобный хелпер для multipart (создание/обновления где потребуется)
export function makeFormData(payload: Record<string, any>): FormData {
  const fd = new FormData();
  Object.entries(payload).forEach(([k, v]) => {
    if (Array.isArray(v)) {
      v.forEach((item) => fd.append(k, item));
    } else if (v !== undefined && v !== null) {
      fd.append(k, v);
    }
  });
  return fd;
}
