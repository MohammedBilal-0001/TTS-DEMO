'use client'

import { Table, ArrowDownUp } from 'lucide-react'

interface QueryResultsProps {
  data: any[]
  columns: string[]
}

export default function QueryResults({ data, columns }: QueryResultsProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Table className="w-5 h-5 mr-2 text-blue-600" />
          Query Results
        </h2>
        
        <div className="text-gray-500 italic h-32 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
          No data available. Run a query to see results.
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Table className="w-5 h-5 mr-2 text-blue-600" />
        Query Results
        <span className="ml-2 text-sm text-gray-500">
          ({data.length} rows)
        </span>
      </h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column, index) => (
                <th
                  key={index}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  <div className="flex items-center">
                    {column}
                    <ArrowDownUp className="w-3 h-3 ml-1 text-gray-400" />
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50">
                {columns.map((column, colIndex) => (
                  <td
                    key={colIndex}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                  >
                    {row[column] !== null && row[column] !== undefined 
                      ? String(row[column]) 
                      : '-'
                    }
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {data.length > 10 && (
        <div className="mt-4 text-sm text-gray-500 text-center">
          Showing first 10 of {data.length} rows
        </div>
      )}
    </div>
  )
}
