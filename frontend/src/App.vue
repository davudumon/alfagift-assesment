<script setup>
import { onMounted, reactive, ref } from 'vue'

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const tasks = ref([])
const loading = ref(false)
const error = ref('')
const form = reactive({
  title: '',
  description: '',
  status: 'Todo'
})
const statuses = ['Todo', 'In Progress', 'Done']

async function request(path, options = {}) {
  const response = await fetch(`${apiUrl}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options
  })

  if (!response.ok) {
    let message = 'Request failed'
    try {
      const body = await response.json()
      message = body.detail?.[0]?.msg || body.detail || message
    } catch {
      // Keep the fallback message when the response has no JSON body.
    }
    throw new Error(message)
  }

  if (response.status === 204) return null
  return response.json()
}

async function loadTasks() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await request('/tasks')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function createTask() {
  error.value = ''
  try {
    const task = await request('/tasks', {
      method: 'POST',
      body: JSON.stringify(form)
    })
    tasks.value = [task, ...tasks.value]
    form.title = ''
    form.description = ''
    form.status = 'Todo'
  } catch (err) {
    error.value = err.message
  }
}

async function updateStatus(task, status) {
  error.value = ''
  try {
    const updated = await request(`/tasks/${task.id}`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    })
    tasks.value = tasks.value.map((item) => (item.id === updated.id ? updated : item))
  } catch (err) {
    error.value = err.message
  }
}

async function deleteTask(task) {
  error.value = ''
  try {
    await request(`/tasks/${task.id}`, { method: 'DELETE' })
    tasks.value = tasks.value.filter((item) => item.id !== task.id)
  } catch (err) {
    error.value = err.message
  }
}

onMounted(loadTasks)
</script>

<template>
  <main class="app-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Personal workspace</p>
        <h1>Task Tracker</h1>
      </div>
      <span class="task-count">{{ tasks.length }} {{ tasks.length === 1 ? 'task' : 'tasks' }}</span>
    </header>

    <section class="create-panel" aria-labelledby="create-heading">
      <h2 id="create-heading">Create a task</h2>
      <form @submit.prevent="createTask">
        <label>
          Title
          <input v-model.trim="form.title" required maxlength="200" placeholder="What needs to be done?" />
        </label>
        <label>
          Description
          <textarea v-model.trim="form.description" maxlength="5000" rows="3" placeholder="Add useful details"></textarea>
        </label>
        <label>
          Status
          <select v-model="form.status">
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>
        </label>
        <button class="primary-button" type="submit">Add task</button>
      </form>
    </section>

    <p v-if="error" class="alert" role="alert">{{ error }}</p>
    <p v-if="loading" class="loading">Loading tasks...</p>

    <section v-else class="task-grid" aria-label="Task list">
      <article v-for="task in tasks" :key="task.id" class="task-card" :class="task.status.toLowerCase().replaceAll(' ', '-')">
        <div class="task-card-header">
          <h3>{{ task.title }}</h3>
          <button class="delete-button" type="button" :aria-label="`Delete ${task.title}`" @click="deleteTask(task)">
            Delete
          </button>
        </div>
        <p v-if="task.description" class="description">{{ task.description }}</p>
        <p v-else class="description empty">No description</p>
        <label class="status-control">
          Status
          <select :value="task.status" @change="updateStatus(task, $event.target.value)">
            <option v-for="status in statuses" :key="status" :value="status">{{ status }}</option>
          </select>
        </label>
      </article>

      <div v-if="tasks.length === 0" class="empty-state">
        <strong>No tasks yet</strong>
        <p>Create your first task above.</p>
      </div>
    </section>
  </main>
</template>
