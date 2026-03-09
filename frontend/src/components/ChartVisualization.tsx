'use client'

import { BarChart3, LineChart, PieChart } from 'lucide-react'
import {
  BarChart,
  Bar,
  LineChart as RechartsLineChart,
  Line,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

interface ChartVisualizationProps {
  chartSpec: any
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

export default function ChartVisualization({ chartSpec }: ChartVisualizationProps) {
  if (!chartSpec || chartSpec.chart_type === 'none') {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-orange-600" />
          Visualization
        </h2>
        
        <div className="text-gray-500 italic h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
          No chart available. Ask a question to generate a visualization.
        </div>
      </div>
    )
  }

  // Extract actual data from chart_spec - need to get this from backend
  // For now, we'll need the backend to include the actual data in chart_spec
  const chartData = chartSpec.data || []

  const renderChart = () => {
    switch (chartSpec.chart_type) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={chartSpec.x || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={chartSpec.y || 'value'} fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        )
      
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <RechartsLineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={chartSpec.x || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={chartSpec.y || 'value'} stroke="#3B82F6" strokeWidth={2} />
            </RechartsLineChart>
          </ResponsiveContainer>
        )
      
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <RechartsPieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey={chartSpec.y || 'value'}
              >
                {chartData.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </RechartsPieChart>
          </ResponsiveContainer>
        )
      
      default:
        return (
          <div className="text-gray-500 h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
            Unsupported chart type: {chartSpec.chart_type}
          </div>
        )
    }
  }

  const getChartIcon = () => {
    switch (chartSpec.chart_type) {
      case 'bar':
        return <BarChart3 className="w-5 h-5" />
      case 'line':
        return <LineChart className="w-5 h-5" />
      case 'pie':
        return <PieChart className="w-5 h-5" />
      default:
        return <BarChart3 className="w-5 h-5" />
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <div className="w-5 h-5 mr-2 text-orange-600">
          {getChartIcon()}
        </div>
        Visualization
      </h2>
      
      <div className="mb-3">
        <h3 className="text-md font-medium text-gray-800">
          {chartSpec.title || 'Data Visualization'}
        </h3>
        <p className="text-sm text-gray-600">
          Chart type: {chartSpec.chart_type}
        </p>
      </div>
      
      {renderChart()}
    </div>
  )
}
