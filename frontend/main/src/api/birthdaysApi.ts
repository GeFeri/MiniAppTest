// src/api/birthdaysApi.ts
import { api } from "./axiosInstance";
import type { BirthdayUser } from "./types";

export async function getBirthdays(limit = 30): Promise<BirthdayUser[]> {
  const r = await api.get("/birthdays/");
  return r.data;
}
