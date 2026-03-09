'use client'

import { Brain, Lightbulb } from 'lucide-react'

interface InsightsPanelProps {
  insights: string
}

export default function InsightsPanel({ insights }: InsightsPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Brain className="w-5 h-5 mr-2 text-purple-600" />
        Insights
      </h2>
      
      <div className="space-y-3">
        {insights ? (
          <div className="flex items-start space-x-3">
            <Lightbulb className="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
            <p className="text-gray-700 leading-relaxed">{insights}</p>
          </div>
        ) : (
          <div className="text-gray-500 italic">
            No insights available yet. Ask a question to generate insights.
          </div>
        )}
      </div>
    </div>
  )
}
