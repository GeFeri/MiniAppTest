import { useEffect, useState } from "react";
import { useSafeLaunchParams } from "./useSafeLaunchParams.ts";
import { useRawInitData, cloudStorage } from "@tma.js/sdk-react";
import { api } from "../api/axiosInstance";

/**
 * Авторизация Telegram MiniApp через tma.js
 *  1️⃣ Проверяет CloudStorage -> isAuthorized
 *  2️⃣ Если нет, шлёт initDataRaw на бек
 *  3️⃣ При успехе сохраняет tg_id и роль в CloudStorage
 */
export const useTelegramAuth = () => {
  const launch = useSafeLaunchParams();
  const initDataRaw = useRawInitData();
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // 1. Проверяем CloudStorage
        const flag = await cloudStorage.get("isAuthorized");
        if (flag === "true") {
          setAuthorized(true);
          return;
        }

        // 2. Проверяем входные данные Telegram
        const tgId = launch?.user?.id;
        if (!tgId || !initDataRaw) {
          console.warn("initData или tgId отсутствуют");
          setAuthorized(false);
          return;
        }

        // 3. Отправляем initDataRaw на бекенд
        const res = await api.post("/auth/tg/", { init_data: initDataRaw });

        if (res.status === 200 && res.data?.user) {
          // 4. Сохраняем данные в CloudStorage
          await cloudStorage.set("isAuthorized", "true");
          await cloudStorage.set("tg_id", String(res.data.user.tg_id));
          await cloudStorage.set("is_manager", res.data.is_manager ? "1" : "0");

          setAuthorized(true);
        } else {
          setAuthorized(false);
        }
      } catch (err) {
        console.error("Ошибка авторизации:", err);
        setAuthorized(false);
      }
    };

    checkAuth();
  }, [launch, initDataRaw]);

  return authorized;
};
