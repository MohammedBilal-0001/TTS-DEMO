'use client'

import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'

interface QueryInputProps {
  onSubmit: (question: string) => void
  disabled: boolean
}

export default function QueryInput({ onSubmit, disabled }: QueryInputProps) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (question.trim() && !disabled) {
      onSubmit(question.trim())
    }
  }

  const demoQuestions = [
    'Average price of all products per category',
    'Which product has the most sellers',
    'View annual sales reports',
    'The first 3 employees hired',
    'how are u today?'
  ]

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Search className="w-5 h-5 mr-2 text-blue-600" />
        Ask a Question
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your data..."
            className="w-full p-3 border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            disabled={disabled}
          />
        </div>
        
        <button
          type="submit"
          disabled={disabled || !question.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {disabled ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Search className="w-4 h-4 mr-2" />
              Analyze
            </>
          )}
        </button>
      </form>

      <div className="mt-4">
        <p className="text-sm text-gray-600 mb-2">Try these examples:</p>
        <div className="space-y-1">
          {demoQuestions.map((demo, index) => (
            <button
              key={index}
              onClick={() => setQuestion(demo)}
              disabled={disabled}
              className="block w-full text-left text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 px-2 py-1 rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              • {demo}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
