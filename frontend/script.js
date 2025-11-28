// Backend API URL
const API_URL = "http://127.0.0.1:8000/api/tasks/analyze/";

let tasks = [];

// Add task via form
document.getElementById("taskForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value.trim();
  const due_date = document.getElementById("due_date").value;
  const estimated_hours = document.getElementById("estimated_hours").value;
  const importance = document.getElementById("importance").value;
  const dependencies = document
    .getElementById("dependencies")
    .value.split(",")
    .map((d) => d.trim())
    .filter((d) => d !== "")
    .map(Number);

  if (!title) {
    alert("Title is required");
    return;
  }

  let task = {
    title,
    due_date,
    estimated_hours: estimated_hours ? Number(estimated_hours) : null,
    importance: importance ? Number(importance) : null,
    dependencies,
  };

  tasks.push(task);
  alert("Task Added!");
  this.reset();
});

// Analyze button
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const bulkInput = document.getElementById("bulkJson").value.trim();
  const strategy = document.getElementById("strategy").value;

  let sendTasks = tasks;

  // If JSON is pasted, override tasks
  if (bulkInput) {
    try {
      sendTasks = JSON.parse(bulkInput);
      if (!Array.isArray(sendTasks)) throw new Error("JSON must be an array");
    } catch (err) {
      alert("Invalid JSON: " + err.message);
      return;
    }
  }

  if (sendTasks.length === 0) {
    alert("Please add some tasks first.");
    return;
  }

  const payload = {
    strategy: strategy,
    tasks: sendTasks,
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    renderResults(data.tasks);
  } catch (err) {
    alert("Failed to connect to backend: " + err.message);
  }
});

// Render results
function renderResults(tasks) {
  const container = document.getElementById("results");
  container.innerHTML = "";

  tasks.forEach((t) => {
    const card = document.createElement("div");
    card.className = "task-card";

    card.innerHTML = `
      <div><strong>${t.title}</strong></div>
      <div class="meta">
        Due: ${t.due_date || "N/A"} |
        Hours: ${t.estimated_hours || "N/A"} |
        Importance: ${t.importance || "N/A"}
      </div>
      <div class="meta">Dependencies: ${t.dependencies.join(", ")}</div>
      <div class="score">Score: ${t.score}</div>
    `;

    container.appendChild(card);
  });
}
