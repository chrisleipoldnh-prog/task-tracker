import { useEffect, useState } from "react";

const API_URL = "http://localhost:8050";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  // READ
  async function fetchTasks() {
    const response = await fetch(`${API_URL}/tasks`);
    const data = await response.json();
    setTasks(data);
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  // CREATE
  async function createTask(event) {
    event.preventDefault();

    if (!title.trim()) {
      return;
    }

    await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
      }),
    });

    setTitle("");
    await fetchTasks();
  }

  // UPDATE
  async function toggleTask(task) {
    await fetch(`${API_URL}/tasks/${task.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        completed: !task.completed,
      }),
    });

    await fetchTasks();
  }

  // DELETE
  async function deleteTask(taskId) {
    await fetch(`${API_URL}/tasks/${taskId}`, {
      method: "DELETE",
    });

    await fetchTasks();
  }

  return (
    <main>
      <h1>Task Tracker</h1>

      <form onSubmit={createTask}>
        <input
          type="text"
          placeholder="Enter a task"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />

        <button type="submit">Add Task</button>
      </form>

      <h2>Tasks</h2>

      {tasks.length === 0 ? (
        <p>No tasks yet.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              <span>
                {task.title} —{" "}
                {task.completed ? "Complete" : "Incomplete"}
              </span>

              <button onClick={() => toggleTask(task)}>
                {task.completed ? "Mark Incomplete" : "Mark Complete"}
              </button>

              <button onClick={() => deleteTask(task.id)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}

export default App;