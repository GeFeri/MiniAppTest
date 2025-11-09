import { Home, CalendarDays, User2 } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import clsx from "clsx";

export const BottomNav = () => {
  const location = useLocation();
  const [hidden, setHidden] = useState(false);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScroll = window.scrollY;
      if (currentScroll > lastScrollY && currentScroll > 50) {
        setHidden(true);
      } else {
        setHidden(false);
      }
      setLastScrollY(currentScroll);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [lastScrollY]);

  const active = (path: string) => location.pathname === path;

  return (
    <div
      className={clsx(
        "fixed bottom-4 left-1/2 -translate-x-1/2 z-30 transition-transform duration-300",
        hidden ? "translate-y-32 opacity-0" : "translate-y-0 opacity-100"
      )}
    >
      <div
        className="flex items-center justify-between gap-8 bg-white rounded-full shadow-lg px-6 py-3
                   border border-gray-200 backdrop-blur-md"
      >
        <Link
          to="/"
          className={clsx(
            "p-2 transition-colors",
            active("/") ? "text-[#2a5885]" : "text-gray-500"
          )}
        >
          <Home size={24} />
        </Link>

        <Link
          to="/birthdays"
          className={clsx(
            "p-2 transition-colors",
            active("/birthdays") ? "text-[#2a5885]" : "text-gray-500"
          )}
        >
          <CalendarDays size={24} />
        </Link>

        <Link
          to="/profile/1"
          className={clsx(
            "p-2 transition-colors",
            active("/profile/me") ? "text-[#2a5885]" : "text-gray-500"
          )}
        >
          <User2 size={24} />
        </Link>
      </div>
    </div>
  );
};
