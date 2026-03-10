"use client"

import { useRouter } from "next/navigation"
import { motion } from "framer-motion"

export default function Home() {

  const router = useRouter()

  return (

    <div className="min-h-screen bg-gradient-to-br from-blue-700 via-indigo-700 to-purple-800 flex items-center justify-center">

      <div className="text-center text-white">

        <motion.h1
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold mb-6"
        >
           Maritime GenAI Assistant
        </motion.h1>

        <p className="text-lg mb-8 max-w-xl mx-auto">
          Graph-Enhanced Retrieval Augmented Generation System
          for Maritime Regulations Knowledge Exploration
        </p>

        <button
          onClick={() => router.push("/register")}
          className="bg-white text-blue-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Get Started
        </button>

      </div>

    </div>

  )
}