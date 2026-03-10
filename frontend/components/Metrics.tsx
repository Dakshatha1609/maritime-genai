"use client"

import { Activity, Database, Network } from "lucide-react"

export default function Metrics() {

  return (

    <div className="grid grid-cols-3 gap-4 mb-8">

      <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-4">

        <div className="flex items-center gap-2 text-indigo-300">
          <Network size={20}/>
          <span>Graph Nodes</span>
        </div>

        <p className="text-2xl font-bold mt-2">
          43
        </p>

      </div>

      <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-4">

        <div className="flex items-center gap-2 text-indigo-300">
          <Database size={20}/>
          <span>Graph Edges</span>
        </div>

        <p className="text-2xl font-bold mt-2">
          50
        </p>

      </div>

      <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl p-4">

        <div className="flex items-center gap-2 text-indigo-300">
          <Activity size={20}/>
          <span>Avg Latency</span>
        </div>

        <p className="text-2xl font-bold mt-2">
          ~120 ms
        </p>

      </div>

    </div>

  )

}