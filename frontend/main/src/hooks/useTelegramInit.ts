import WebApp from "@twa-dev/sdk";
import {useEffect} from "react";

export function useTelegramInit() {
  useEffect(() => {
    WebApp.ready();
    const tgId = WebApp.initDataUnsafe?.user?.id;
    if (tgId) localStorage.setItem("tg_id", tgId.toString());
  }, []);
}
