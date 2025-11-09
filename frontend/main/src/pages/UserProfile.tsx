import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getUser } from "../api/usersApi"
import { HobbyBlock } from "../components/HobbyBlock"
import { PageContainer } from "../components/PageContainer"
import { AddHobbyModal } from "../components/AddHobbyModal"

export const UserProfile = () => {
  const { id } = useParams()
  const [user, setUser] = useState<any>(null)
  const [modalOpen, setModalOpen] = useState(false)

  const loadUser = () => getUser(id!).then(setUser)
  useEffect(() => {
    loadUser()
  }, [id])

  if (!user)
    return (
      <PageContainer>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <div className="text-gray-500">Загрузка…</div>
          </div>
        </div>
      </PageContainer>
    )

  return (
    <PageContainer>
      <div className="relative -mx-4 -mt-4 mb-8 px-4 pt-12 pb-8 bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-100 overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-200/30 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-indigo-200/30 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

        {/* 🧑 User Information with enhanced styling */}
        <div className="relative flex flex-col items-center text-center">
          <div className="relative group mb-4">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full blur-md opacity-75 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative w-32 h-32 bg-white rounded-full overflow-hidden ring-4 ring-white shadow-xl flex items-center justify-center text-5xl font-bold text-gray-700">
              {user.avatar ? (
                <img src={`${user.avatar}`} alt="avatar" className="object-cover w-full h-full" />
              ) : (
                <span className="bg-gradient-to-br from-blue-500 to-indigo-600 bg-clip-text text-transparent">
                  {user.first_name?.[0] || "👤"}
                </span>
              )}
            </div>
          </div>

          <h1 className="text-3xl font-bold text-gray-900 mb-2 tracking-tight">
            {user.first_name} {user.last_name}
          </h1>

          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-3">
            <span>@{user.username}</span>
          </div>

          {user.birth_date && (
            <div className="flex items-center gap-2 text-gray-600 text-sm bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm">
              <span className="text-lg">🎂</span>
              <span>
                {new Date(user.birth_date).toLocaleDateString("ru-RU", {
                  day: "numeric",
                  month: "long",
                  year: "numeric",
                })}
              </span>
            </div>
          )}
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-1">Хобби</h2>
            <p className="text-sm text-gray-500">
              {user.hobbies?.length > 0
                ? `${user.hobbies.length} ${user.hobbies.length === 1 ? "хобби" : "хобби"}`
                : "Добавьте свои интересы"}
            </p>
          </div>
          <button
            onClick={() => setModalOpen(true)}
            className="group flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium rounded-xl shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 active:scale-95"
          >
            <span className="text-xl group-hover:rotate-90 transition-transform duration-300">+</span>
            <span className="hidden sm:inline">Добавить</span>
          </button>
        </div>

        <div className="grid gap-4">
          {user.hobbies?.length > 0 ? (
            user.hobbies.map((uh: any, index: number) => (
              <div
                key={uh.hobby.id}
                className="transform hover:scale-[1.02] transition-transform duration-200"
                style={{
                  animation: `fadeInUp 0.5s ease-out ${index * 0.1}s both`,
                }}
              >
                <HobbyBlock hobby={uh.hobby} description={uh.description} />
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-16 px-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl border-2 border-dashed border-gray-300">
              <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mb-4 text-4xl">
                ✨
              </div>
              <p className="text-gray-500 text-center font-medium mb-2">Хобби пока нет</p>
              <p className="text-gray-400 text-sm text-center max-w-xs">Расскажите о своих интересах и увлечениях</p>
            </div>
          )}
        </div>
      </div>

      {modalOpen && <AddHobbyModal onClose={() => setModalOpen(false)} onCreated={loadUser} />}

      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </PageContainer>
  )
}
