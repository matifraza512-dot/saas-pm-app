import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'
import client from '../api/client'

export default function DashboardPage() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [orgs, setOrgs] = useState([])
  const [projects, setProjects] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [o, p, t] = await Promise.all([
          client.get('/organizations/'),
          client.get('/projects/'),
          client.get('/tasks/'),
        ])
        setOrgs(o.data)
        setProjects(p.data)
        setTasks(t.data)
      } catch {
        logout()
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const tasksByStatus = {
    todo: tasks.filter(t => t.status === 'todo'),
    in_progress: tasks.filter(t => t.status === 'in_progress'),
    in_review: tasks.filter(t => t.status === 'in_review'),
    done: tasks.filter(t => t.status === 'done'),
  }

  const columns = [
    { key: 'todo', label: 'To Do', color: 'border-gray-500' },
    { key: 'in_progress', label: 'In Progress', color: 'border-blue-500' },
    { key: 'in_review', label: 'In Review', color: 'border-yellow-500' },
    { key: 'done', label: 'Done', color: 'border-green-500' },
  ]

  const priorityColor = {
    low: 'bg-gray-500/20 text-gray-400',
    medium: 'bg-blue-500/20 text-blue-400',
    high: 'bg-orange-500/20 text-orange-400',
    urgent: 'bg-red-500/20 text-red-400',
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-gray-400 text-lg">Loading your workspace...</div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navbar */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold text-indigo-400">SaaS PM</span>
          <span className="text-gray-600">|</span>
          <span className="text-gray-400 text-sm">
            {user?.full_name || user?.email}
          </span>
        </div>
        <button onClick={handleLogout}
          className="text-sm text-gray-400 hover:text-white transition">
          Sign out
        </button>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          {[
            { label: 'Organizations', value: orgs.length, color: 'text-indigo-400' },
            { label: 'Projects', value: projects.length, color: 'text-blue-400' },
            { label: 'Tasks', value: tasks.length, color: 'text-green-400' },
          ].map((stat) => (
            <div key={stat.label} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className={`text-3xl font-bold ${stat.color}`}>{stat.value}</div>
              <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Kanban Board */}
        <h2 className="text-lg font-semibold text-gray-300 mb-4">Task Board</h2>
        {tasks.length === 0 ? (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-10 text-center text-gray-500">
            No tasks yet. Create an organization and project first via the API, then add tasks.
          </div>
        ) : (
          <div className="grid grid-cols-4 gap-4">
            {columns.map((col) => (
              <div key={col.key} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <div className={`flex items-center gap-2 mb-4 pb-3 border-b-2 ${col.color}`}>
                  <span className="font-semibold text-sm">{col.label}</span>
                  <span className="ml-auto bg-gray-800 text-gray-400 text-xs px-2 py-0.5 rounded-full">
                    {tasksByStatus[col.key].length}
                  </span>
                </div>
                <div className="space-y-3">
                  {tasksByStatus[col.key].map((task) => (
                    <div key={task.id} className="bg-gray-800 rounded-lg p-3 border border-gray-700 hover:border-indigo-500/50 transition">
                      <p className="text-sm font-medium text-white mb-2">{task.title}</p>
                      <div className="flex items-center justify-between">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${priorityColor[task.priority]}`}>
                          {task.priority}
                        </span>
                        {task.due_date && (
                          <span className="text-xs text-gray-500">{task.due_date}</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}