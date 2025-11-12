// Общие типы, чтобы весь фронт был строготипизирован

export type ID = number | string;

export interface TypeHobby {
  id: ID;
  name: string;
}

export interface Hobby {
  id: ID;
  name: string;
  emoji?: string | null;
  color?: string | null;
  type?: TypeHobby | null;
  // На бэке описание хранится в UserHobby, поэтому здесь его нет
}

export interface Department {
  id: ID;
  name: string;
  manager?: ID;
}
export interface UserHobby {
  id: ID;
  hobby: Hobby;
  description?: string | null;
}

export interface User {
  id: ID;
  username: string;
  first_name: string;
  last_name: string;
  bio?: string | null;
  birth_date?: string | null;
  tg_id: number;
  department?: ID | null;
  hobbies: UserHobby[]; // ✅ исправлено
}

export interface BirthdayUser {
  id: ID;
  first_name: string;
  last_name: string;
  birth_date: string; // ISO
  department_name?: string;
}

export interface EventItem {
  id: ID;
  title: string;
  content?: string | null;
  date: string; // ISO
  created_by: string; // username (по сериализатору)
  created_at: string; // ISO
  image?: string | null;
}

export interface InviteKey {
  id: ID;
  key: string;
  department: ID;
  department_name?: string;
  created_by: ID;
  created_by_name?: string;
  first_name?: string | null;
  last_name?: string | null;
  telegram_username?: string | null;
  used: boolean;
  used_by?: ID | null;
  used_by_name?: string | null;
  created_at: string;
  expires_at?: string | null;
}
