from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Create Owner ---
owner = Owner(name="Jordan")
owner.add_availability_window(time(8, 0), time(12, 0))   # 8:00 AM - 12:00 PM
owner.add_availability_window(time(14, 0), time(17, 0))   # 2:00 PM - 5:00 PM

# --- Create Pets ---
dog = Pet(name="Mochi", pet_type="dog")
dog.add_health_problem("bad knees")
dog.add_requirement(Task(task_type="Morning Walk", priority=1, duration=30))
dog.add_requirement(Task(task_type="Feeding", priority=2, duration=15))
dog.add_requirement(Task(task_type="Grooming", priority=4, duration=45))

cat = Pet(name="Whiskers", pet_type="cat")
cat.add_requirement(Task(task_type="Feeding", priority=1, duration=10))
cat.add_requirement(Task(task_type="Litter Box Clean", priority=3, duration=15))
cat.add_requirement(Task(task_type="Play Session", priority=5, duration=20))

owner.add_pet(dog)
owner.add_pet(cat)

# --- Schedule and Print ---
scheduler = Scheduler()

print("=" * 50)
print(f"  Today's Schedule for {owner.name}")
print("  Availability: ", end="")
for start, end in owner.get_availability_windows():
    print(f"{start.strftime('%I:%M %p')}-{end.strftime('%I:%M %p')}  ", end="")
print()
print("=" * 50)

for pet in owner.get_pets():
    scheduled = scheduler.schedule(owner, pet)
    print(f"\n  {pet.name} ({pet.pet_type})")
    if pet.get_health_problems():
        print(f"  Health notes: {', '.join(pet.get_health_problems())}")
    print(f"  {'Time':<12} {'Task':<20} {'Duration':<12} {'Priority'}")
    print(f"  {'-'*12} {'-'*20} {'-'*12} {'-'*8}")
    for task in scheduled:
        t = task.get_scheduled_time()
        if t is None:
            continue
        print(
            f"  {t.strftime('%I:%M %p'):<12} "
            f"{task.get_type():<20} "
            f"{task.get_duration()} min{'':<7} "
            f"{task.get_priority()}"
        )

print("\n" + "=" * 50)
print(f"  Conflicts detected: {scheduler.has_conflicts()}")
print("=" * 50)
