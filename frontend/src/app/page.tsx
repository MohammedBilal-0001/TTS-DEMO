'use client'

import { useState } from 'react'
import { Search, BarChart3, Brain, Activity } from 'lucide-react'
import QueryInput from '@/components/QueryInput'
import AgentLogs from '@/components/AgentLogs'
import InsightsPanel from '@/components/InsightsPanel'
import ChartVisualization from '@/components/ChartVisualization'
import QueryResults from '@/components/QueryResults'

export default function Home() {
  const [logs, setLogs] = useState<string[]>([])
  const [insights, setInsights] = useState<string>('')
  const [chartSpec, setChartSpec] = useState<any>(null)
  const [queryResults, setQueryResults] = useState<any>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleQuery = async (question: string) => {
    setIsProcessing(true)
    setLogs([])
    setInsights('')
    setChartSpec(null)
    setQueryResults(null)

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      const result = await response.json()

      if (result.success) {
        setLogs(result.logs)
        setInsights(result.insights)
        setChartSpec(result.chart_spec)
        setQueryResults(result.query_results)
      } else {
        setLogs([...result.logs, `Error: ${result.error}`])
      }
    } catch (error) {
      setLogs([`Network error: ${error}`])
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-8 h-8 text-blue-600 mr-2" />
            <h1 className="text-3xl font-bold text-gray-900">AI Analytics System</h1>
          </div>
          <p className="text-gray-600">Multi-agent AI system for natural language SQL queries</p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Query Input */}
            <QueryInput onSubmit={handleQuery} disabled={isProcessing} />

            {/* Agent Logs */}
            <AgentLogs logs={logs} isProcessing={isProcessing} />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Query Results Table */}
            <QueryResults 
              data={queryResults?.data || []} 
              columns={queryResults?.columns || []} 
            />

            {/* Insights */}
            <InsightsPanel insights={insights} />

            {/* Chart Visualization */}
            <ChartVisualization chartSpec={chartSpec} />
          </div>
        </div>

        {/* Status Bar */}
        <div className="mt-8 p-4 bg-white rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <Activity className="w-4 h-4 text-green-500 mr-2" />
                <span className="text-sm text-gray-600">
                  {isProcessing ? 'Processing...' : 'Ready'}
                </span>
              </div>
              <div className="flex items-center">
                <Search className="w-4 h-4 text-blue-500 mr-2" />
                <span className="text-sm text-gray-600">AI Agents Active</span>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Powered by LangGraph + FastAPI + Next.js
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
