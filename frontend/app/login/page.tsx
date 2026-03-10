"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

export default function LoginPage() {

  const router = useRouter()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = () => {

    const storedEmail = localStorage.getItem("userEmail")
    const storedPassword = localStorage.getItem("userPassword")

    if (email === storedEmail && password === storedPassword) {

      router.push("/dashboard")

    } else {

      alert("Invalid credentials")

    }

  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-700 to-blue-800">

      <div className="bg-white/20 backdrop-blur-lg border border-white/30 shadow-xl rounded-xl p-10 w-[380px] text-white">

        <h2 className="text-3xl font-bold text-center mb-6">
          Login
        </h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 rounded mb-4 text-black"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 rounded mb-4 text-black"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-white text-indigo-700 p-3 rounded font-semibold hover:bg-gray-200"
        >
          Login
        </button>

        <p className="text-center text-sm mt-4">

          New user?{" "}

          <span
            className="underline cursor-pointer"
            onClick={() => router.push("/register")}
          >
            Register
          </span>

        </p>

      </div>

    </div>

  )

}