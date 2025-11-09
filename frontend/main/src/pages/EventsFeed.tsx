"use client"

import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { api } from "../api/axiosInstance"
import { EventCard } from "../components/EventCard"
import { Calendar } from "lucide-react" // Assuming Calendar component is imported
import type { EventItem } from "../api/types"
import {PageContainer} from "../components/PageContainer.tsx"; // ✅ только для типизации

export const EventsFeed = () => {
  const [events, setEvents] = useState<EventItem[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api
      .get("/events/")
      .then((res) => setEvents(res.data))
      .catch((err) => console.error("Ошибка загрузки событий:", err))
  }, [])

  return (
      <PageContainer>
    <div className="flex flex-col items-center w-full min-h-screen bg-gradient-to-b from-gray-50 to-white pt-4 pb-20">
      <div className="relative w-full max-w-md mb-6 px-3">
        <div className="relative bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl p-6 shadow-lg overflow-hidden">
          {/* Decorative circles */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full translate-y-1/2 -translate-x-1/2" />

          <div className="relative">
            <h1 className="text-2xl font-bold text-white mb-1">Мероприятия</h1>
            <p className="text-white/90 text-sm">Предстоящие события и активности</p>
          </div>
        </div>
      </div>

      <div className="w-full max-w-md flex flex-col gap-5 px-3">
        {events.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
              <Calendar className="w-8 h-8 text-blue-500" />
            </div>
            <p className="text-gray-500 text-sm">Пока нет мероприятий</p>
          </div>
        ) : (
          events.map((event) => (
            <EventCard key={event.id} event={event} onClick={() => navigate(`/event/${event.id}`)} />
          ))
        )}
      </div>
    </div>
          </PageContainer>
  )
}
