import { useLaunchParams } from "@tma.js/sdk-react";

export const useSafeLaunchParams = () => {
  try {
    return useLaunchParams();
  } catch {
    console.warn("⚠️ Telegram environment not detected — using DEV fallback");
    return {
      user: {
        id: 999999,
        first_name: "Dev",
        last_name: "Tester",
        username: "dev_user",
        language_code: "ru",
      },
    } as any;
  }
};
