"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

export default function RegisterPage() {

  const router = useRouter()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleRegister = () => {

    if (!email || !password) {
      alert("Please fill all fields")
      return
    }

    localStorage.setItem("userEmail", email)
    localStorage.setItem("userPassword", password)

    alert("Registration successful")

    router.push("/login")
  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-indigo-700 to-purple-800">

      <div className="bg-white/20 backdrop-blur-lg border border-white/30 shadow-xl rounded-xl p-10 w-[380px] text-white">

        <h2 className="text-3xl font-bold text-center mb-6">
          Register
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
          onClick={handleRegister}
          className="w-full bg-white text-indigo-700 p-3 rounded font-semibold hover:bg-gray-200"
        >
          Register
        </button>

        <p className="text-center text-sm mt-4">

          Already have an account?{" "}

          <span
            className="underline cursor-pointer"
            onClick={() => router.push("/login")}
          >
            Login
          </span>

        </p>

      </div>

    </div>

  )
}