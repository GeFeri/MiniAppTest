import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, X } from "lucide-react";
import { getUsers } from "../api/usersApi"; // используется /users/?search=
import clsx from "clsx";

interface UserItem {
  id: number | string;
  username: string;
  first_name: string;
  last_name: string;
}

export const Header = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<UserItem[]>([]);
  const [focused, setFocused] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const delay = setTimeout(() => {
      if (query.trim().length > 0) {
        getUsers(query).then(setResults).catch(() => setResults([]));
      } else {
        setResults([]);
      }
    }, 300); // debounce

    return () => clearTimeout(delay);
  }, [query]);

  const clearSearch = () => {
    setQuery("");
    setResults([]);
  };

  return (
    <div className="fixed top-0 left-0 w-full bg-white border-b border-gray-200 z-30 px-4 py-3 shadow-sm">
      <div className="relative max-w-md mx-auto">
        {/* поле поиска */}
        <div className="flex items-center bg-gray-100 rounded-full px-3 py-2">
          <Search size={18} className="text-gray-400 mr-2" />
          <input
            type="text"
            value={query}
            onFocus={() => setFocused(true)}
            onBlur={() => setTimeout(() => setFocused(false), 200)} // немного задержки, чтобы клик сработал
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Поиск пользователей..."
            className="flex-1 bg-transparent outline-none text-sm text-gray-800"
          />
          {query && (
            <button onClick={clearSearch} className="text-gray-400">
              <X size={16} />
            </button>
          )}
        </div>

        {/* выпадающий список */}
        {focused && results.length > 0 && (
          <div
            className={clsx(
              "absolute left-0 right-0 bg-white rounded-lg shadow-lg mt-2 border border-gray-200 max-h-60 overflow-auto"
            )}
          >
            {results.map((user) => (
              <div
                key={user.id}
                onClick={() => navigate(`/profile/${user.id}`)}
                className="px-4 py-2 text-sm text-gray-800 hover:bg-gray-50 cursor-pointer flex items-center justify-between"
              >
                <span>
                  {user.first_name} {user.last_name}
                </span>
                <span className="text-gray-400">@{user.username}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
