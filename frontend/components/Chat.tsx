"use client"

import { useState } from "react"
import axios from "axios"
import GraphView from "./GraphView"

export default function Chat() {

  const [question, setQuestion] = useState("")
  const [submittedQuery, setSubmittedQuery] = useState("")
  const [answer, setAnswer] = useState("")
  const [contexts, setContexts] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [topk, setTopk] = useState(3)

  const askQuestion = async () => {

    if (!question.trim()) return

    setLoading(true)

    try {
      
       
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/chat`,
        {
          question: question,
          top_k: topk
        }
      )

      setAnswer(res.data.answer)
      setContexts(res.data.contexts)
      setSubmittedQuery(question)

    } catch (err) {

      console.error("Chat API error:", err)

    }

    setLoading(false)

  }

  return (

    <div className="space-y-8">

      {/* Ask Question */}

      <div
        id="chat-section"
        className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-6"
      >

        <h2 className="text-xl font-semibold mb-4">
          Ask Maritime Question
        </h2>

        <input
          className="w-full p-3 rounded bg-black/30 text-white border border-white/20 mb-4"
          placeholder="Ask maritime regulation question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <div className="mb-4">

          <label className="text-sm text-gray-300">
            Top-K Retrieval: {topk}
          </label>

          <input
            type="range"
            min="1"
            max="10"
            value={topk}
            onChange={(e) => setTopk(Number(e.target.value))}
            className="w-full"
          />

        </div>

        <button
          onClick={askQuestion}
          className="bg-indigo-600 px-6 py-2 rounded hover:bg-indigo-700"
        >
          Ask
        </button>

        {loading && (
          <p className="mt-4 text-gray-300">Thinking...</p>
        )}

      </div>


      {/* Answer */}

      {answer && (

        <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-6">

          <h2 className="text-xl font-semibold mb-2">
            Answer
          </h2>

          <p className="text-gray-200">
            {answer}
          </p>

        </div>

      )}


      {/* Contexts */}

      {contexts.length > 0 && (

        <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-6">

          <h2 className="text-xl font-semibold mb-4">
            Retrieved Contexts
          </h2>

          {contexts.map((c: any, i: number) => (

            <div
              key={i}
              className="border border-white/10 rounded p-4 mb-3 bg-black/30 max-h-40 overflow-y-auto"
            >

              <p className="text-xs text-gray-400 mb-1">

                Rank: {c.rank} |
                Source: {c.source} |
                Page: {c.page} |
                Score: {c.score?.toFixed(2)}

              </p>

              <p className="text-sm text-gray-200">
                {c.text}
              </p>

            </div>

          ))}

        </div>

      )}


      {/* Graph */}

      {submittedQuery && (

        <div
          id="graph-section"
          className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-6"
        >

          <GraphView query={submittedQuery} />

        </div>

      )}

    </div>

  )

}