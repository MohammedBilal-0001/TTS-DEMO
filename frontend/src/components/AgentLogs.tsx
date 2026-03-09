'use client'

import { useEffect, useRef } from 'react'
import { Activity, Clock } from 'lucide-react'

interface AgentLogsProps {
  logs: string[]
  isProcessing: boolean
}

export default function AgentLogs({ logs, isProcessing }: AgentLogsProps) {
  const logsEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [logs])

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Activity className="w-5 h-5 mr-2 text-green-600" />
        Agent Logs
        {isProcessing && (
          <span className="ml-2 flex items-center text-sm text-blue-600">
            <Clock className="w-4 h-4 mr-1 animate-pulse" />
            Processing...
          </span>
        )}
      </h2>
      
      <div className="bg-gray-900 text-green-400 p-4 rounded-md font-mono text-sm h-64 overflow-y-auto">
        {logs.length === 0 ? (
          <div className="text-gray-500">Waiting for query...</div>
        ) : (
          <>
            {logs.map((log, index) => (
              <div key={index} className="mb-1">
                {log}
              </div>
            ))}
            <div ref={logsEndRef} />
          </>
        )}
      </div>
      
      {logs.length > 0 && (
        <div className="mt-2 text-xs text-gray-500">
          {logs.length} log entries
        </div>
      )}
    </div>
  )
}
