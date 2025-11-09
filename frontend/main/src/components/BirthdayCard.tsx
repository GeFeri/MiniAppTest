import { Link } from "react-router-dom"
import { Cake } from "lucide-react"

export const BirthdayCard = ({ user }: any) => {
  const birthDate = new Date(user.birth_date)
  const today = new Date()
  const nextBirthday = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate())

  if (nextBirthday < today) {
    nextBirthday.setFullYear(today.getFullYear() + 1)
  }

  const daysUntil = Math.ceil((nextBirthday.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  const isToday = daysUntil === 0
  const isSoon = daysUntil <= 7

  return (
    <Link
      to={`/profile/${user.id}`}
      className="group block relative overflow-hidden bg-gradient-to-br from-white to-gray-50 p-4 rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-purple-200"
    >
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      <div className="relative flex items-center gap-4">
        {/* Birthday icon with animation */}
        <div
          className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 ${
            isToday
              ? "bg-gradient-to-br from-pink-500 to-orange-500 animate-pulse"
              : isSoon
                ? "bg-gradient-to-br from-purple-500 to-pink-500"
                : "bg-gradient-to-br from-gray-400 to-gray-500"
          } group-hover:scale-110`}
        >
          <Cake className="w-6 h-6 text-white" />
        </div>

        {/* User info */}
        <div className="flex-1 min-w-0">
          <div className="font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
            {user.first_name} {user.last_name}
          </div>
          <div className="text-sm text-gray-500">
            {birthDate.toLocaleDateString("ru-RU", { day: "numeric", month: "long" })}
          </div>
        </div>

        {/* Days until badge */}
        <div className="flex-shrink-0">
          {isToday ? (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-pink-500 to-orange-500 text-white animate-pulse">
              Сегодня! 🎉
            </span>
          ) : isSoon ? (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700">
              Через {daysUntil} {daysUntil === 1 ? "день" : daysUntil < 5 ? "дня" : "дней"}
            </span>
          ) : (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
              Через {daysUntil} дней
            </span>
          )}
        </div>
      </div>

      {/* Confetti decoration for today's birthdays */}
      {isToday && (
        <div className="absolute top-0 right-0 w-20 h-20 opacity-20">
          <div
            className="absolute top-2 right-2 w-2 h-2 bg-pink-500 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <div
            className="absolute top-4 right-6 w-2 h-2 bg-orange-500 rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <div
            className="absolute top-6 right-3 w-2 h-2 bg-purple-500 rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
        </div>
      )}
    </Link>
  )
}
