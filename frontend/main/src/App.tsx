import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Header } from "./components/Header";
import { EventsFeed } from "./pages/EventsFeed";
import { Birthdays } from "./pages/Birthdays";
import { EventDetail } from "./pages/EventDetail";
import { UserProfile } from "./pages/UserProfile";
import { ScrollToTopButton } from "./components/ScrollToTopButton";
import { BottomNav } from "./components/BottonNav";
import { useTelegramAuth } from "./hooks/useTelegramAuth";
import { Loader2 } from "lucide-react";

/**
 * Главный компонент MiniApp
 * 🔹 Проверяет авторизацию Telegram
 * 🔹 Показывает лоадер при входе
 * 🔹 Отображает основной интерфейс после успешного входа
 */
function App() {
  const authorized = useTelegramAuth();

  if (authorized === null)
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
        <Loader2 className="animate-spin text-[#2a5885]" size={36} />
        <p className="mt-3 text-sm text-gray-600">Проверка доступа...</p>
      </div>
    );

  if (!authorized)
    return (
      <div className="flex flex-col items-center justify-center h-screen text-center px-6 bg-gray-50">
        <p className="text-lg font-semibold mb-2 text-gray-800">
          🚫 Доступ ограничен
        </p>
        <p className="text-sm text-gray-600 leading-snug">
          Обратитесь к руководителю, чтобы получить InviteKey через Telegram-бота.
        </p>
      </div>
    );

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen bg-[#f2f3f5]">
        <Header />
        <Routes>
          <Route path="/" element={<EventsFeed />} />
          <Route path="/event/:id" element={<EventDetail />} />
          <Route path="/birthdays" element={<Birthdays />} />
          <Route path="/profile/:id" element={<UserProfile />} />
          <Route path="/profile/me" element={<UserProfile />} />
        </Routes>

        <ScrollToTopButton />
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;
