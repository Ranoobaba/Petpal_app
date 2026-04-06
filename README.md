# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Several algorithmic improvements were added on top of the base priority-queue scheduler:

| Feature | How it works |
|---|---|
| **Shared window pool** | `schedule_all()` schedules every pet's tasks into one shared availability pool, eliminating cross-pet time conflicts |
| **Window merging** | Overlapping availability windows (e.g. 8–12 and 10–13) are merged before scheduling so no capacity is double-counted |
| **Health-aware priority boost** | Tasks are automatically promoted if a pet's health condition is relevant (e.g. joint problems → walk tasks get boosted) |
| **Feeding interval boost** | If a pet hasn't been fed in over 6 hours, its feeding task is elevated to priority 1 |
| **Bin-packing second pass** | Tasks that don't fit on the first pass are retried in remaining window gaps instead of being silently dropped |
| **Skipped task reporting** | Any task that couldn't be scheduled is surfaced as a warning rather than silently omitted |
| **Recurring tasks** | Tasks with `frequency="daily"` or `"weekly"` auto-generate a new instance (with the correct next `due_date`) when marked complete, using Python's `timedelta` |
| **Filter and sort helpers** | `filter_by_status()`, `filter_by_pet()`, and `sort_by_time()` allow querying the schedule after it is built |

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
