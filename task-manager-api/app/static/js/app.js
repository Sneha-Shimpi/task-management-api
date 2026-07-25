const API_BASE = "/api/tasks";

const state = {
  tasks: [],
  filters: {
    priority: "",
    status: "",
    dueDate: "",
    search: "",
    sort: "created_at_desc",
  },
  loading: false,
};

const els = {
  columns: {
    todo: document.getElementById("list-todo"),
    in_progress: document.getElementById("list-in_progress"),
    done: document.getElementById("list-done"),
  },
  counts: {
    todo: document.getElementById("count-todo"),
    in_progress: document.getElementById("count-in_progress"),
    done: document.getElementById("count-done"),
  },
  stats: {
    total: document.getElementById("stat-total"),
    todo: document.getElementById("stat-todo"),
    progress: document.getElementById("stat-progress"),
    done: document.getElementById("stat-done"),
    high: document.getElementById("stat-high"),
    complete: document.getElementById("stat-complete"),
  },
  toolbarStatus: document.getElementById("toolbarStatus"),
  searchInput: document.getElementById("searchInput"),
  statusFilter: document.getElementById("statusFilter"),
  dueDateFilter: document.getElementById("dueDateFilter"),
  sortSelect: document.getElementById("sortSelect"),
  newTaskBtn: document.getElementById("newTaskBtn"),
  modalOverlay: document.getElementById("modalOverlay"),
  modalTitle: document.getElementById("modalTitle"),
  modalClose: document.getElementById("modalClose"),
  cancelBtn: document.getElementById("cancelBtn"),
  deleteBtn: document.getElementById("deleteBtn"),
  taskForm: document.getElementById("taskForm"),
  taskId: document.getElementById("taskId"),
  fieldTitle: document.getElementById("fieldTitle"),
  fieldDescription: document.getElementById("fieldDescription"),
  fieldStatus: document.getElementById("fieldStatus"),
  fieldPriority: document.getElementById("fieldPriority"),
  fieldDueDate: document.getElementById("fieldDueDate"),
  formError: document.getElementById("formError"),
  toast: document.getElementById("toast"),
  chips: document.querySelectorAll(".chip"),
};

async function apiRequest(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (res.status === 204) return null;

  const body = await res.json().catch(() => ({}));

  if (!res.ok) {
    const message = body.error || "Something went wrong";
    throw new Error(message);
  }
  return body;
}

function buildQuery() {
  const params = new URLSearchParams({ per_page: "100" });
  if (state.filters.priority) params.set("priority", state.filters.priority);
  if (state.filters.status) params.set("status", state.filters.status);
  if (state.filters.dueDate) params.set("due_date", state.filters.dueDate);
  if (state.filters.search) params.set("search", state.filters.search);
  const [sortBy, order] = getSortParts();
  params.set("sort_by", sortBy);
  params.set("order", order);
  return params.toString();
}

function getSortParts() {
  switch (state.filters.sort) {
    case "created_at_asc":
      return ["created_at", "asc"]; 
    case "priority_desc":
      return ["priority", "desc"]; 
    case "title_asc":
      return ["title", "asc"]; 
    default:
      return ["created_at", "desc"];
  }
}

async function fetchTasks() {
  state.loading = true;
  renderSkeleton();
  try {
    const data = await apiRequest(`${API_BASE}?${buildQuery()}`);
    state.tasks = data.tasks || [];
    updateSummary(data.summary || {});
    render();
  } catch (err) {
    els.toolbarStatus.textContent = "Could not reach the API";
    showToast(err.message);
  } finally {
    state.loading = false;
  }
}

function renderSkeleton() {
  for (const key of Object.keys(els.columns)) {
    const container = els.columns[key];
    container.innerHTML = "";
    const skeleton = document.createElement("div");
    skeleton.className = "column__empty";
    skeleton.textContent = "Loading workspace…";
    container.appendChild(skeleton);
  }
}

function updateSummary(summary) {
  els.stats.total.textContent = summary.total ?? 0;
  els.stats.todo.textContent = summary.todo ?? 0;
  els.stats.progress.textContent = summary.in_progress ?? 0;
  els.stats.done.textContent = summary.done ?? 0;
  els.stats.high.textContent = summary.high_priority ?? 0;
  els.stats.complete.textContent = `${summary.completion_rate ?? 0}%`;
}

function render() {
  const grouped = { todo: [], in_progress: [], done: [] };
  for (const task of state.tasks) {
    (grouped[task.status] || grouped.todo).push(task);
  }

  for (const status of Object.keys(grouped)) {
    const container = els.columns[status];
    container.innerHTML = "";
    els.counts[status].textContent = grouped[status].length;

    if (grouped[status].length === 0) {
      const empty = document.createElement("div");
      empty.className = "column__empty";
      empty.textContent = state.tasks.length === 0 ? "No tasks match your filters yet." : "Nothing in this lane yet.";
      container.appendChild(empty);
      continue;
    }

    for (const task of grouped[status]) {
      container.appendChild(renderCard(task));
    }
  }

  els.toolbarStatus.textContent = `${state.tasks.length} visible tasks`;
}

function renderCard(task) {
  const card = document.createElement("article");
  card.className = "task-card";
  card.dataset.priority = task.priority;
  card.tabIndex = 0;
  card.setAttribute("role", "button");
  card.setAttribute("aria-label", `Open task: ${task.title}`);

  const title = document.createElement("h3");
  title.className = "task-card__title";
  title.textContent = task.title;
  card.appendChild(title);

  if (task.description) {
    const desc = document.createElement("p");
    desc.className = "task-card__desc";
    desc.textContent = task.description;
    card.appendChild(desc);
  }

  const meta = document.createElement("div");
  meta.className = "task-card__meta";

  const priority = document.createElement("span");
  priority.className = "task-card__priority";
  priority.textContent = task.priority;
  meta.appendChild(priority);

  const due = document.createElement("span");
  due.className = "task-card__due";
  due.textContent = task.due_date ? `Due ${formatDate(task.due_date)}` : "No due date";
  meta.appendChild(due);

  card.appendChild(meta);

  const open = () => openModal(task);
  card.addEventListener("click", open);
  card.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      open();
    }
  });

  card.addEventListener("dragstart", (e) => {
    e.dataTransfer.setData("text/plain", String(task.id));
  });
  card.setAttribute("draggable", "true");

  return card;
}

function formatDate(isoString) {
  const d = new Date(isoString);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function openModal(task = null) {
  els.formError.hidden = true;
  els.taskForm.reset();

  if (task) {
    els.modalTitle.textContent = "Edit task";
    els.taskId.value = task.id;
    els.fieldTitle.value = task.title;
    els.fieldDescription.value = task.description || "";
    els.fieldStatus.value = task.status;
    els.fieldPriority.value = task.priority;
    els.fieldDueDate.value = task.due_date || "";
    els.deleteBtn.hidden = false;
  } else {
    els.modalTitle.textContent = "New task";
    els.taskId.value = "";
    els.fieldStatus.value = "todo";
    els.fieldPriority.value = "medium";
    els.fieldDueDate.value = "";
    els.deleteBtn.hidden = true;
  }

  els.modalOverlay.classList.add("is-open");
  els.fieldTitle.focus();
}

function closeModal() {
  els.modalOverlay.classList.remove("is-open");
}

function showFormError(message) {
  els.formError.textContent = message;
  els.formError.hidden = false;
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.add("is-visible");
  setTimeout(() => els.toast.classList.remove("is-visible"), 2200);
}

els.newTaskBtn.addEventListener("click", () => openModal());
els.modalClose.addEventListener("click", closeModal);
els.cancelBtn.addEventListener("click", closeModal);
els.modalOverlay.addEventListener("click", (e) => {
  if (e.target === els.modalOverlay) closeModal();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && els.modalOverlay.classList.contains("is-open")) {
    closeModal();
  }
});

els.taskForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  els.formError.hidden = true;

  const payload = {
    title: els.fieldTitle.value.trim(),
    description: els.fieldDescription.value.trim(),
    status: els.fieldStatus.value,
    priority: els.fieldPriority.value,
    due_date: els.fieldDueDate.value || null,
  };

  try {
    if (els.taskId.value) {
      await apiRequest(`${API_BASE}/${els.taskId.value}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      showToast("Task updated");
    } else {
      await apiRequest(API_BASE, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast("Task created");
    }
    closeModal();
    await fetchTasks();
  } catch (err) {
    showFormError(err.message);
  }
});

els.deleteBtn.addEventListener("click", async () => {
  const id = els.taskId.value;
  if (!id) return;
  if (!window.confirm("Delete this task? This action cannot be undone.")) return;

  try {
    await apiRequest(`${API_BASE}/${id}`, { method: "DELETE" });
    showToast("Task deleted");
    closeModal();
    await fetchTasks();
  } catch (err) {
    showFormError(err.message);
  }
});

els.chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    els.chips.forEach((c) => c.classList.remove("is-active"));
    chip.classList.add("is-active");
    state.filters.priority = chip.dataset.value;
    fetchTasks().catch((err) => showToast(err.message));
  });
});

document.querySelector('.chip[data-value=""]').classList.add("is-active");

els.searchInput.addEventListener("input", (e) => {
  state.filters.search = e.target.value.trim();
  fetchTasks().catch((err) => showToast(err.message));
});

els.statusFilter.addEventListener("change", (e) => {
  state.filters.status = e.target.value;
  fetchTasks().catch((err) => showToast(err.message));
});

els.dueDateFilter.addEventListener("change", (e) => {
  state.filters.dueDate = e.target.value;
  fetchTasks().catch((err) => showToast(err.message));
});

els.sortSelect.addEventListener("change", (e) => {
  state.filters.sort = e.target.value;
  fetchTasks().catch((err) => showToast(err.message));
});

for (const column of document.querySelectorAll(".column")) {
  column.addEventListener("dragover", (e) => e.preventDefault());
  column.addEventListener("drop", async (e) => {
    const taskId = e.dataTransfer.getData("text/plain");
    const status = column.dataset.status;
    if (!taskId || !status) return;
    try {
      await apiRequest(`${API_BASE}/${taskId}`, {
        method: "PUT",
        body: JSON.stringify({ status }),
      });
      showToast("Task moved");
      await fetchTasks();
    } catch (err) {
      showToast(err.message);
    }
  });
}

fetchTasks().catch((err) => {
  els.toolbarStatus.textContent = "Could not reach the API";
  showToast(err.message);
});
