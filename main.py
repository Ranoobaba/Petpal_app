from datetime import date, time
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Owner ---
owner = Owner(name="Jordan")
owner.add_availability_window(time(8, 0), time(12, 0))
owner.add_availability_window(time(10, 0), time(13, 0))  # overlaps with above (merge test)
owner.add_availability_window(time(14, 0), time(17, 0))

# --- Pets ---
dog = Pet(name="Mochi", pet_type="dog")
dog.add_health_problem("bad knees")

# Tasks added OUT OF ORDER (low priority first, high last)
# frequency="daily"/"weekly" enables auto-rescheduling on completion
dog.add_requirement(Task(task_type="Grooming",      priority=4, duration=45, frequency="weekly"))
dog.add_requirement(Task(task_type="Morning Walk",  priority=1, duration=30, frequency="daily"))
dog.add_requirement(Task(task_type="Feeding",       priority=2, duration=15, frequency="daily"))

cat = Pet(name="Whiskers", pet_type="cat")

# Tasks added OUT OF ORDER
cat.add_requirement(Task(task_type="Play Session",      priority=5, duration=20))
cat.add_requirement(Task(task_type="Litter Box Clean",  priority=3, duration=15, frequency="daily"))
cat.add_requirement(Task(task_type="Feeding",           priority=1, duration=10, frequency="daily"))

owner.add_pet(dog)
owner.add_pet(cat)

# --- Schedule (shared window pool — no cross-pet conflicts) ---
scheduler = Scheduler()
scheduler.reset()
scheduler.schedule_all(owner)

# Mark tasks complete — collect any auto-generated next occurrences
next_occurrences = []

for task in scheduler.filter_by_pet("Mochi"):
    if task.get_type() == "Morning Walk":
        next_task = task.mark_complete()
        if next_task:
            next_occurrences.append(next_task)

for task in scheduler.filter_by_pet("Whiskers"):
    if task.get_type() == "Feeding":
        next_task = task.mark_complete()
        if next_task:
            next_occurrences.append(next_task)

# ── Helper to print a task table ──────────────────────────────────────────────
def print_tasks(tasks, label):
    print(f"\n  {label}")
    print(f"  {'Pet':<12} {'Time':<12} {'Task':<22} {'Min':<6} {'Pri':<5} {'Status'}")
    print(f"  {'-'*12} {'-'*12} {'-'*22} {'-'*6} {'-'*5} {'-'*8}")
    for t in tasks:
        scheduled = t.get_scheduled_time()
        time_str = scheduled.strftime("%I:%M %p") if scheduled else "—"
        print(
            f"  {(t.pet_name or '?'):<12} {time_str:<12} "
            f"{t.get_type():<22} {t.get_duration():<6} "
            f"{t.get_priority():<5} {t.get_status()}"
        )

# ── 1. All tasks sorted by time ───────────────────────────────────────────────
print("=" * 70)
print(f"  Full Schedule for {owner.name}  (tasks added out-of-order, sorted by time)")
print("=" * 70)
print_tasks(scheduler.sort_by_time(scheduler.all_scheduled_tasks), "All tasks — sorted by scheduled time")

# ── 2. Filter by pet ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  Filter by Pet")
print("=" * 70)
print_tasks(scheduler.sort_by_time(scheduler.filter_by_pet("Mochi")),    "Mochi's tasks")
print_tasks(scheduler.sort_by_time(scheduler.filter_by_pet("Whiskers")), "Whiskers's tasks")

# ── 3. Filter by status ───────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  Filter by Status")
print("=" * 70)
print_tasks(scheduler.filter_by_status("complete"), "Completed tasks")
print_tasks(scheduler.filter_by_status("pending"),  "Pending tasks")

# ── 4. Skipped tasks ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
skipped = scheduler.cached_skipped_tasks
print(f"  Skipped tasks (didn't fit any window): {len(skipped)}")
if skipped:
    for t in skipped:
        print(f"    - [{t.pet_name}] {t.get_type()} ({t.get_duration()} min)")

# ── 5. Recurring tasks ───────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  Recurring Tasks — auto-created on completion")
print("=" * 70)
print(f"\n  {'Pet':<12} {'Task':<22} {'Frequency':<10} {'Due Date'}")
print(f"  {'-'*12} {'-'*22} {'-'*10} {'-'*12}")
if next_occurrences:
    for t in next_occurrences:
        print(f"  {(t.pet_name or '?'):<12} {t.get_type():<22} {(t.frequency or '—'):<10} {t.due_date}")
else:
    print("  (none)")

# ── 6. Conflict check ─────────────────────────────────────────────────────────
print(f"\n  Conflicts detected: {scheduler.has_conflicts()}")
print("=" * 70)
