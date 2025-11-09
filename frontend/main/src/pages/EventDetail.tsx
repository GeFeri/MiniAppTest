"use client"

import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { getEventById } from "../api/eventsApi"
import { format } from "date-fns"
import { ru } from "date-fns/locale"
import { ArrowLeft, Calendar, User } from "lucide-react"
import type { EventItem } from "../api/types"
import { PageContainer } from "../components/PageContainer.tsx"

export const EventDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [event, setEvent] = useState<EventItem | null>(null)

  useEffect(() => {
    if (!id) return
    getEventById(Number(id))
      .then((data) => setEvent(data))
      .catch((err) => console.error("Ошибка загрузки:", err))
  }, [id])

  if (!event)
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-gradient-to-b from-gray-50 to-white">
        <div className="w-12 h-12 rounded-full border-4 border-blue-500 border-t-transparent animate-spin mb-4" />
        <p className="text-gray-500">Загрузка...</p>
      </div>
    )

  return (
    <PageContainer>
      <div className="bg-gradient-to-b from-gray-50 to-white min-h-screen text-gray-900 pb-10">
        <div className="sticky top-0 bg-white/80 backdrop-blur-md z-10 flex items-center justify-center border-b border-gray-200 py-3 shadow-sm">
          <button
            onClick={() => navigate(-1)}
            className="absolute left-4 text-gray-700 hover:text-blue-600 active:scale-95 transition-all duration-200 p-2 hover:bg-gray-100 rounded-full"
          >
            <ArrowLeft size={22} />
          </button>
          <h2 className="font-semibold text-[16px] text-gray-900">Мероприятие</h2>
        </div>

        <div className="max-w-md mx-auto px-4 mt-6">
          {/* Cover image with enhanced styling */}
          {event.image && (
            <div className="relative rounded-2xl overflow-hidden shadow-xl mb-6 group">
              <img
                src={event.image.startsWith("http") ? event.image : `http://localhost:8000${event.image}`}
                alt={event.title}
                className="w-full object-cover max-h-[280px] group-hover:scale-105 transition-transform duration-300"
              />
              {/* Gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
            </div>
          )}

          <div className="mb-6">
            <h1 className="text-[24px] font-bold leading-tight text-gray-900 mb-3 text-balance">{event.title}</h1>

            <div className="flex flex-wrap items-center gap-3">
              {/* Date badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-100">
                <Calendar className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-700">
                  {format(new Date(event.date), "d MMMM yyyy", { locale: ru })}
                </span>
              </div>

              {/* Creator badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200">
                <User className="w-4 h-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">{event.created_by}</span>
              </div>
            </div>
          </div>

          <div className="prose prose-sm max-w-none">
            <div className="text-[15px] leading-relaxed text-gray-700 whitespace-pre-line bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              {event.content}
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-[13px] text-gray-400 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-gray-300" />
              Опубликовано {format(new Date(event.created_at), "d MMMM yyyy, HH:mm", { locale: ru })}
            </p>
          </div>
        </div>
      </div>
    </PageContainer>
  )
}
