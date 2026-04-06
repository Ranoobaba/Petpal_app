# PawPal+ 🐾

A Streamlit app that helps pet owners build a smart daily care schedule across multiple pets — prioritizing tasks by urgency, health needs, and available time.

## 📸 Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Features

### Core Scheduling
- **Priority-queue scheduling** — Tasks are placed into the owner's availability windows using a min-heap. Lower priority number = scheduled first. Built with Python's `heapq`.
- **Multi-pet shared window pool** — `schedule_all()` runs every pet's tasks through one shared availability pool. Once a time slot is consumed, no other pet can use it — eliminating cross-pet time conflicts.
- **Overlapping window merging** — If an owner adds two windows that overlap (e.g. 8–12 and 10–13), they are automatically merged into a single span (8–13) before scheduling so no capacity is double-counted.
- **Bin-packing second pass** — Tasks that don't fit on the first scheduling pass are retried in any remaining window gaps, maximizing the number of tasks that get placed.

### Smart Priority Adjustments
- **Health-aware task boosting** — If a pet has a health condition (e.g. `"bad knees"`), related tasks (e.g. walks) are automatically promoted up one priority level so they're scheduled before lower-urgency work.
- **Feeding interval boost** — If a pet hasn't been fed in over 6 hours, its feeding task is automatically elevated to priority 1 regardless of its original value.

### Recurring Tasks
- **Daily and weekly recurrence** — Tasks can be marked `frequency="daily"` or `frequency="weekly"`. When `mark_complete()` is called, it returns a brand-new `Task` instance with `due_date` set to today + 1 day or today + 7 days using Python's `timedelta`. The current task is marked complete; the new one starts as `pending`.

### Querying the Schedule
- **`filter_by_pet(name)`** — Returns all scheduled tasks for a specific pet from the shared pool.
- **`filter_by_status(status)`** — Returns all `"pending"` or `"complete"` tasks across all pets.
- **`sort_by_time(tasks)`** — Returns a new list sorted by scheduled start time. Tasks with no assigned time are placed at the end.

### Conflict Detection
- **Cross-pet conflict detection** — `has_conflicts()` checks `all_scheduled_tasks` (the full shared pool) for any two tasks whose time windows overlap. Returns `True` with a logged error if a conflict is found.

### Visibility
- **Skipped task reporting** — Any task that couldn't fit in any availability window is tracked in `cached_skipped_tasks` and surfaced as a warning in the UI — never silently dropped.

---

## Running the App

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Running Tests

```bash
pytest tests/test_pawpal.py -v
```

53 tests covering: Task creation and recurrence, Pet tracking, Owner availability, Scheduler priority ordering, sort correctness, conflict detection, and cross-pet filtering.

---

## Project Structure

```
pawpal-starter/
├── pawpal_system.py   # Core classes: Task, Pet, Owner, Scheduler
├── app.py             # Streamlit UI
├── main.py            # CLI demo with sorting, filtering, and recurrence output
├── tests/
│   └── test_pawpal.py # 53 tests across 7 test classes
├── class_diagram.md   # Final Mermaid UML diagram
└── reflection.md      # Design decisions and tradeoffs
```

## Architecture

```
app.py / main.py
    ↓  creates Owner, Pet, Task
pawpal_system.py
    ↓  Scheduler.schedule_all(owner)
    ↓  → _apply_priority_boosts()   [health + feeding logic]
    ↓  → _merge_windows()           [collapse overlapping windows]
    ↓  → _resolve_priority_queue()  [min-heap + bin-packing]
    ↓  → filter / sort helpers
UI renders sorted, filtered schedule with conflict and skipped-task warnings
```
