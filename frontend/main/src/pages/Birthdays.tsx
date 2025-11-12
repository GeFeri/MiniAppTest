"use client"

// pages/Birthdays.tsx
import { useEffect, useState } from "react"
import { getBirthdays } from "../api/birthdaysApi"
import { BirthdayCard } from "../components/BirthdayCard"
import { PageContainer } from "../components/PageContainer.tsx"
import { Cake } from "lucide-react"
import type {BirthdayUser} from "../api/types.ts"; // Assuming Cake is imported from here

export const Birthdays = () => {
  const [users, setUsers] = useState<BirthdayUser[]>([])

  useEffect(() => {
    getBirthdays().then(setUsers)
  }, [])

  return (
    <PageContainer>
      <div className="px-3 py-6">
        <div className="relative mb-6">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-orange-500/10 rounded-2xl blur-xl" />
          <div className="relative bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-2xl border border-purple-100">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Ближайшие дни рождения
            </h1>
            <p className="text-sm text-gray-600 mt-1">Не забудьте поздравить своих друзей! 🎂</p>
          </div>
        </div>

        <div className="space-y-3">
          {users.map((u, index) => (
            <div
              key={u.id}
              className="animate-in fade-in slide-in-from-bottom-4"
              style={{ animationDelay: `${index * 50}ms`, animationFillMode: "backwards" }}
            >
              <BirthdayCard user={u} />
            </div>
          ))}
        </div>

        {users.length === 0 && (
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 mb-4">
              <Cake className="w-8 h-8 text-purple-600" />
            </div>
            <p className="text-gray-500">Нет предстоящих дней рождения</p>
          </div>
        )}
      </div>
    </PageContainer>
  )
}
