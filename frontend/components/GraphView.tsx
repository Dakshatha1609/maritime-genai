"use client"

import { useEffect, useRef, useState } from "react"
import dynamic from "next/dynamic"
import axios from "axios"

const ForceGraph2D = dynamic(
  () => import("react-force-graph-2d"),
  { ssr: false }
)

type Node = { id: string }
type Link = { source: string; target: string }

type GraphData = {
  nodes: Node[]
  links: Link[]
}

export default function GraphView({ query }: { query: string }) {

  const containerRef = useRef<HTMLDivElement>(null)

  const [size, setSize] = useState({
    width: 800,
    height: 500
  })

  const [graphData, setGraphData] = useState<GraphData>({
    nodes: [],
    links: []
  })

  const [loaded, setLoaded] = useState(false)

  useEffect(() => {

    const resize = () => {

      if (containerRef.current) {

        setSize({
          width: containerRef.current.offsetWidth,
          height: 500
        })

      }

    }

    resize()

    window.addEventListener("resize", resize)

    return () => window.removeEventListener("resize", resize)

  }, [])

  useEffect(() => {

    if (!query) return

    const fetchGraph = async () => {

      try {

        const res = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/graph`,
          { params: { query } }
        )

        const nodes = res.data.nodes || []
        const links = res.data.links || []

        setGraphData({ nodes, links })

        setLoaded(true)

      } catch (err) {

        console.error("Graph API error:", err)

        setLoaded(true)

      }

    }

    fetchGraph()

  }, [query])

  return (

    <div>

      <h2 className="text-xl font-semibold mb-3">
        Knowledge Graph
      </h2>

      <p className="text-sm text-gray-500 mb-3">
        Nodes: {graphData.nodes.length} | Edges: {graphData.links.length}
      </p>

      <div ref={containerRef} className="w-full h-[500px]">

        {graphData.nodes.length > 0 ? (

          <ForceGraph2D
            graphData={graphData}
            width={size.width}
            height={size.height}
            nodeRelSize={8}
            linkWidth={2}
            cooldownTicks={120}
            nodeColor={(node: any) =>
              node.id.toLowerCase() === query.toLowerCase()
                ? "#ff4d4f"
                : "#1f77b4"
            }
            nodeCanvasObject={(node: any, ctx: any, globalScale: any) => {

              const label = node.id
              const fontSize = 12 / globalScale

              ctx.font = `${fontSize}px Sans-Serif`
              ctx.fillStyle = "black"

              ctx.fillText(label, node.x + 8, node.y + 3)

            }}
          />

        ) : loaded ? (

          <div className="flex items-center justify-center h-full text-gray-500">
            Graph loaded but no nodes to display.
          </div>

        ) : (

          <div className="flex items-center justify-center h-full text-gray-500">
            Loading graph...
          </div>

        )}

      </div>

    </div>

  )

}