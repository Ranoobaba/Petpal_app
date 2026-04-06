# PawPal+ Class Diagram (Final)

```mermaid
classDiagram
    class Task {
        +task_type: str
        +priority: int
        +duration: int
        +status: str
        +task_id: str
        +scheduled_start_time: time
        +pet_name: str
        +frequency: str
        +due_date: date
        +get_priority() int
        +get_duration() int
        +get_type() str
        +get_status() str
        +get_task_id() str
        +set_scheduled_time(start_time)
        +get_scheduled_time() time
        +mark_complete() Task
    }

    class Pet {
        +name: str
        +pet_type: str
        +health_problems: list
        +last_fed_time: datetime
        +last_exercise_time: datetime
        +requirements: list~Task~
        +feed()
        +has_been_fed() bool
        +get_last_fed_time() datetime
        +exercise()
        +get_last_exercise_time() datetime
        +add_health_problem(problem)
        +get_health_problems() list
        +add_requirement(task)
        +get_requirements() list~Task~
    }

    class Owner {
        +name: str
        +availability_windows: list
        +pets: list~Pet~
        +add_availability_window(start, end)
        +get_availability_windows() list
        +clear_availability()
        +add_pet(pet)
        +get_pets() list~Pet~
    }

    class Scheduler {
        +priority_heap: list
        +cached_scheduled_tasks: list~Task~
        +cached_skipped_tasks: list~Task~
        +all_scheduled_tasks: list~Task~
        +schedule(owner, pet) list~Task~
        +schedule_all(owner) dict
        +reset()
        +get_scheduled_tasks() list~Task~
        +get_skipped_tasks() list~Task~
        +filter_by_status(status) list~Task~
        +filter_by_pet(pet_name) list~Task~
        +sort_by_time(tasks) list~Task~
        +has_conflicts() bool
        -_merge_windows(windows) list
        -_apply_priority_boosts(tasks, pet)
        -_resolve_priority_queue(tasks, availability) list~Task~
    }

    Owner "1" *-- "*" Pet : owns
    Pet "1" *-- "*" Task : requires
    Scheduler "1" ..> "*" Task : schedules
    Scheduler "1" ..> "1" Owner : reads availability
    Scheduler "1" ..> "*" Pet : boosts priorities
    Task ..> Task : creates next occurrence
```

## What changed from Phase 1

| Class | Phase 1 | Final |
|---|---|---|
| `Task` | 4 attributes, `mark_complete()` void | 9 attributes; `mark_complete()` returns new `Task` for recurring tasks |
| `Pet` | `is_fed: bool` boolean flag | `last_fed_time: datetime` timestamp; `add_requirement` auto-sets `pet_name` |
| `Owner` | Single `availability_start/end` pair | `availability_windows: list` supports multiple windows |
| `Scheduler` | 1 attribute, 4 methods | 4 attributes, 11 public + 3 private methods |

## Relationship types used

- `*--` (composition): Owner owns Pets; Pet owns Tasks — if the owner is deleted, their pets and tasks go with them
- `..>` (dependency): Scheduler reads from Owner/Pet/Task but does not own them — it only references them during scheduling

## Class Responsibilities

**Task** — Represents a single pet care activity. Knows its own type, duration, priority, scheduled time, and recurrence frequency. Can self-replicate (return a next occurrence) when marked complete.

**Pet** — Tracks a pet's health, feeding/exercise history, and list of required tasks. Stamps each task with the pet's name when added.

**Owner** — Holds multiple availability windows and a list of pets. The Scheduler reads these windows to know when time slots are available.

**Scheduler** — Orchestrates the full schedule. Uses a min-heap to process tasks by priority, fills shared availability windows across all pets to prevent conflicts, and exposes filtering and sorting helpers for querying the result.

## How to export as PNG

1. Copy the Mermaid code block above
2. Paste into [mermaid.live](https://mermaid.live)
3. Click **Download PNG** → save as `uml_final.png` in this project folder
