"use client"

import Sidebar from "../../components/Sidebar"
import Chat from "../../components/Chat"
import Metrics from "../../components/Metrics"

export default function Dashboard() {

  return (

    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white">

      {/* Sidebar */}

      <Sidebar />

      {/* Main Content */}

      <div className="flex-1 p-8 overflow-y-auto">

        <h1 className="text-3xl font-bold mb-6">
          Maritime GenAI Assistant
        </h1>

        {/* Metrics */}

        <Metrics />

        {/* Chat + Graph */}

        <Chat />

      </div>

    </div>

  )

}