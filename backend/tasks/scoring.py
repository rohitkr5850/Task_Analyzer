from datetime import datetime, date

def clamp(x, a, b):
    return max(a, min(b, x))

def parse_date(d):
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return None

def compute_urgency_score(due_date):
    today = date.today()
    if due_date is None:
        return 0.5

    diff = (due_date - today).days

    if diff < 0:
        return 1.0
    elif diff == 0:
        return 1.0
    else:
        return clamp(1 - (diff / 30), 0.1, 1.0)

def compute_importance_score(importance):
    if importance is None:
        importance = 5
    importance = clamp(importance, 1, 10)
    return (importance - 1) / 9

def compute_effort_score(hours):
    if hours is None:
        hours = 3
    if hours <= 0:
        return 1.0
    return clamp(1 - (hours / 40), 0.1, 1.0)

def compute_dependency_score(task_id, all_tasks):
    count = 0
    for t in all_tasks:
        deps = t.get("dependencies", [])
        if task_id in deps:
            count += 1
    return clamp(count / 5, 0.0, 1.0)

def score_task(task, all_tasks, strategy="smart-balance"):
    due_date = parse_date(task.get("due_date"))
    urgency = compute_urgency_score(due_date)
    importance = compute_importance_score(task.get("importance"))
    effort = compute_effort_score(task.get("estimated_hours"))
    dependency = compute_dependency_score(task.get("id"), all_tasks)

    weights = {
        "urgency": 0.4,
        "importance": 0.3,
        "effort": 0.2,
        "dependency": 0.1
    }

    if strategy == "fastest-wins":
        weights = {"urgency": 0.1, "importance": 0.2, "effort": 0.6, "dependency": 0.1}
    elif strategy == "high-impact":
        weights = {"urgency": 0.1, "importance": 0.7, "effort": 0.1, "dependency": 0.1}
    elif strategy == "deadline-driven":
        weights = {"urgency": 0.7, "importance": 0.1, "effort": 0.1, "dependency": 0.1}

    score = (
        urgency * weights["urgency"] +
        importance * weights["importance"] +
        effort * weights["effort"] +
        dependency * weights["dependency"]
    )

    return {
        "score": round(score, 4),
        "urgency": urgency,
        "importance": importance,
        "effort": effort,
        "dependency": dependency
    }
