"use client"

import { Calendar, User } from "lucide-react"
import { format } from "date-fns"
import { ru } from "date-fns/locale"
import type { EventItem } from "../api/types"

interface EventCardProps {
  event: EventItem
  onClick: () => void
}

export const EventCard = ({ event, onClick }: EventCardProps) => {
  const eventDate = new Date(event.date)
  const today = new Date()
  const isPast = eventDate < today
  const isToday = eventDate.toDateString() === today.toDateString()
  const isSoon = !isPast && (eventDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24) <= 7

  return (
    <div
      onClick={onClick}
      className="group cursor-pointer relative overflow-hidden bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-blue-200"
    >
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      <div className="relative">
        {/* Image section */}
        {event.image && (
          <div className="relative h-48 overflow-hidden">
            <img
              src={event.image.startsWith("http") ? event.image : `http://localhost:8000${event.image}`}
              alt={event.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            {/* Gradient overlay on image */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />

            {/* Date badge on image */}
            <div className="absolute top-3 right-3">
              <div
                className={`px-3 py-1.5 rounded-lg backdrop-blur-sm font-semibold text-sm ${
                  isToday
                    ? "bg-gradient-to-r from-pink-500 to-orange-500 text-white animate-pulse"
                    : isSoon
                      ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white"
                      : isPast
                        ? "bg-gray-900/70 text-gray-300"
                        : "bg-white/90 text-gray-900"
                }`}
              >
                {format(eventDate, "d MMM", { locale: ru })}
              </div>
            </div>
          </div>
        )}

        {/* Content section */}
        <div className="p-4">
          {/* Title */}
          <h3 className="font-bold text-lg text-gray-900 group-hover:text-blue-600 transition-colors mb-2 line-clamp-2">
            {event.title}
          </h3>

          {/* Meta info */}
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
            <div className="flex items-center gap-1.5">
              <Calendar className="w-4 h-4" />
              <span>{format(eventDate, "d MMMM yyyy", { locale: ru })}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <User className="w-4 h-4" />
              <span className="truncate">{event.created_by}</span>
            </div>
          </div>

          {/* Description preview */}
          {event.content && <p className="text-sm text-gray-600 line-clamp-2 leading-relaxed">{event.content}</p>}

          {/* Status indicator */}
          {isToday && (
            <div className="mt-3 inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-pink-500 to-orange-500 text-white">
              Сегодня! 🎉
            </div>
          )}
        </div>
      </div>

      {/* Decorative corner accent */}
      <div className="absolute bottom-0 right-0 w-24 h-24 bg-gradient-to-tl from-blue-500/10 to-transparent rounded-tl-full opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
    </div>
  )
}
