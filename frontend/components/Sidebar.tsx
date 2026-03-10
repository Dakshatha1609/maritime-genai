"use client"

import { useRouter } from "next/navigation"
import { MessageCircle, Network, LayoutDashboard, LogOut } from "lucide-react"

export default function Sidebar() {

  const router = useRouter()

  const scrollTo = (id: string) => {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: "smooth" })
  }

  return (

    <div className="w-64 min-h-screen bg-black/40 backdrop-blur-md border-r border-white/10 p-6">

      <h2 className="text-2xl font-bold text-white mb-10">
         Maritime GenAI
      </h2>

      <nav className="space-y-6">

        <button
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-3 text-white hover:text-indigo-300"
        >
          <LayoutDashboard size={20}/>
          Dashboard
        </button>

        <button
          onClick={() => scrollTo("chat-section")}
          className="flex items-center gap-3 text-white hover:text-indigo-300"
        >
          <MessageCircle size={20}/>
          Chat Assistant
        </button>

        <button
          onClick={() => scrollTo("graph-section")}
          className="flex items-center gap-3 text-white hover:text-indigo-300"
        >
          <Network size={20}/>
          Knowledge Graph
        </button>

        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-3 text-red-400 hover:text-red-300 pt-10"
        >
          <LogOut size={20}/>
          Logout
        </button>

      </nav>

    </div>

  )

}