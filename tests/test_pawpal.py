import pytest
from datetime import date, time, datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Test suite for Task class"""
    
    def test_task_creation(self):
        """Test creating a task with required attributes"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.task_type == "feeding"
        assert task.priority == 1
        assert task.duration == 30
        assert task.status == "pending"
    
    def test_task_has_unique_id(self):
        """Test that each task gets a unique ID"""
        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=60)
        assert task1.task_id != task2.task_id
    
    def test_get_priority(self):
        """Test retrieving task priority"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.get_priority() == 1
    
    def test_get_duration(self):
        """Test retrieving task duration"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.get_duration() == 30
    
    def test_get_type(self):
        """Test retrieving task type"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.get_type() == "feeding"
    
    def test_get_status_initial(self):
        """Test initial task status is pending"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.get_status() == "pending"
    
    def test_mark_complete(self):
        """Test marking a task as complete"""
        task = Task(task_type="feeding", priority=1, duration=30)
        task.mark_complete()
        assert task.get_status() == "complete"
    
    def test_get_task_id(self):
        """Test retrieving task ID"""
        task = Task(task_type="feeding", priority=1, duration=30)
        task_id = task.get_task_id()
        assert isinstance(task_id, str)
        assert len(task_id) > 0
    
    def test_set_scheduled_time(self):
        """Test setting scheduled time for a task"""
        task = Task(task_type="feeding", priority=1, duration=30)
        scheduled_time = time(10, 30)
        task.set_scheduled_time(scheduled_time)
        assert task.get_scheduled_time() == scheduled_time
    
    def test_scheduled_time_initially_none(self):
        """Test that scheduled time is None initially"""
        task = Task(task_type="feeding", priority=1, duration=30)
        assert task.get_scheduled_time() is None


class TestPet:
    """Test suite for Pet class"""
    
    def test_pet_creation(self):
        """Test creating a pet with required attributes"""
        pet = Pet(name="Buddy", pet_type="dog")
        assert pet.name == "Buddy"
        assert pet.pet_type == "dog"
    
    def test_pet_initial_state(self):
        """Test pet's initial state"""
        pet = Pet(name="Buddy", pet_type="dog")
        assert pet.last_fed_time is None
        assert pet.last_exercise_time is None
        assert len(pet.health_problems) == 0
        assert len(pet.requirements) == 0
    
    def test_feed_pet(self):
        """Test feeding a pet"""
        pet = Pet(name="Buddy", pet_type="dog")
        pet.feed()
        assert pet.has_been_fed() is True
        assert pet.get_last_fed_time() is not None
    
    def test_has_been_fed_false_initially(self):
        """Test that pet has not been fed initially"""
        pet = Pet(name="Buddy", pet_type="dog")
        assert pet.has_been_fed() is False
    
    def test_exercise_pet(self):
        """Test exercising a pet"""
        pet = Pet(name="Buddy", pet_type="dog")
        pet.exercise()
        assert pet.get_last_exercise_time() is not None
    
    def test_add_health_problem(self):
        """Test adding a health problem"""
        pet = Pet(name="Buddy", pet_type="dog")
        pet.add_health_problem("allergies")
        assert "allergies" in pet.get_health_problems()
    
    def test_get_health_problems(self):
        """Test retrieving all health problems"""
        pet = Pet(name="Buddy", pet_type="dog")
        pet.add_health_problem("allergies")
        pet.add_health_problem("anxiety")
        problems = pet.get_health_problems()
        assert len(problems) == 2
        assert "allergies" in problems
        assert "anxiety" in problems
    
    def test_add_requirement(self):
        """Test adding a task requirement"""
        pet = Pet(name="Buddy", pet_type="dog")
        task = Task(task_type="feeding", priority=1, duration=30)
        pet.add_requirement(task)
        assert task in pet.get_requirements()
    
    def test_get_requirements(self):
        """Test retrieving all requirements"""
        pet = Pet(name="Buddy", pet_type="dog")
        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=60)
        pet.add_requirement(task1)
        pet.add_requirement(task2)
        requirements = pet.get_requirements()
        assert len(requirements) == 2
        assert task1 in requirements
        assert task2 in requirements
    
    def test_multiple_feedings(self):
        """Test that pet can be fed multiple times"""
        pet = Pet(name="Buddy", pet_type="dog")
        pet.feed()
        first_feed_time = pet.get_last_fed_time()
        
        # Simulate time passing
        import time as time_module
        time_module.sleep(0.1)
        
        pet.feed()
        second_feed_time = pet.get_last_fed_time()
        
        assert second_feed_time >= first_feed_time


class TestOwner:
    """Test suite for Owner class"""
    
    def test_owner_creation(self):
        """Test creating an owner"""
        owner = Owner(name="John")
        assert owner.name == "John"
    
    def test_owner_initial_state(self):
        """Test owner's initial state"""
        owner = Owner(name="John")
        assert len(owner.availability_windows) == 0
        assert len(owner.pets) == 0
    
    def test_add_availability_window(self):
        """Test adding an availability window"""
        owner = Owner(name="John")
        start = time(9, 0)
        end = time(12, 0)
        owner.add_availability_window(start, end)
        
        windows = owner.get_availability_windows()
        assert len(windows) == 1
        assert windows[0] == (start, end)
    
    def test_add_multiple_availability_windows(self):
        """Test adding multiple availability windows"""
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(12, 0))
        owner.add_availability_window(time(14, 0), time(18, 0))
        
        windows = owner.get_availability_windows()
        assert len(windows) == 2
    
    def test_clear_availability(self):
        """Test clearing all availability windows"""
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(12, 0))
        owner.clear_availability()
        
        assert len(owner.get_availability_windows()) == 0
    
    def test_add_pet(self):
        """Test adding a pet to owner"""
        owner = Owner(name="John")
        pet = Pet(name="Buddy", pet_type="dog")
        owner.add_pet(pet)
        
        pets = owner.get_pets()
        assert len(pets) == 1
        assert pet in pets
    
    def test_add_multiple_pets(self):
        """Test adding multiple pets to owner"""
        owner = Owner(name="John")
        pet1 = Pet(name="Buddy", pet_type="dog")
        pet2 = Pet(name="Whiskers", pet_type="cat")
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        pets = owner.get_pets()
        assert len(pets) == 2
        assert pet1 in pets
        assert pet2 in pets
    
    def test_get_pets(self):
        """Test retrieving all pets"""
        owner = Owner(name="John")
        pet1 = Pet(name="Buddy", pet_type="dog")
        pet2 = Pet(name="Whiskers", pet_type="cat")
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        pets = owner.get_pets()
        assert len(pets) == 2


class TestScheduler:
    """Test suite for Scheduler class"""
    
    def test_scheduler_creation(self):
        """Test creating a scheduler"""
        scheduler = Scheduler()
        assert len(scheduler.priority_heap) == 0
        assert len(scheduler.cached_scheduled_tasks) == 0
    
    def test_schedule_single_task(self):
        """Test scheduling a single task"""
        scheduler = Scheduler()
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(17, 0))
        
        pet = Pet(name="Buddy", pet_type="dog")
        task = Task(task_type="feeding", priority=1, duration=30)
        pet.add_requirement(task)
        
        scheduled = scheduler.schedule(owner, pet)
        assert len(scheduled) == 1
        assert scheduled[0] == task
    
    def test_schedule_respects_priority(self):
        """Test that scheduler respects task priority (lower value = higher importance)"""
        scheduler = Scheduler()
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(17, 0))
        
        pet = Pet(name="Buddy", pet_type="dog")
        task1 = Task(task_type="feeding", priority=2, duration=30)
        task2 = Task(task_type="exercise", priority=1, duration=60)
        task3 = Task(task_type="grooming", priority=3, duration=45)
        
        pet.add_requirement(task1)
        pet.add_requirement(task2)
        pet.add_requirement(task3)
        
        scheduled = scheduler.schedule(owner, pet)
        
        # Should be ordered by priority: task2 (1), task1 (2), task3 (3)
        assert scheduled[0].get_priority() == 1
        assert scheduled[1].get_priority() == 2
        assert scheduled[2].get_priority() == 3
    
    def test_get_scheduled_tasks(self):
        """Test retrieving scheduled tasks"""
        scheduler = Scheduler()
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(17, 0))
        
        pet = Pet(name="Buddy", pet_type="dog")
        task = Task(task_type="feeding", priority=1, duration=30)
        pet.add_requirement(task)
        
        scheduler.schedule(owner, pet)
        scheduled = scheduler.get_scheduled_tasks()
        
        assert len(scheduled) == 1
    
    def test_has_no_conflicts_initially(self):
        """Test that scheduler has no conflicts initially"""
        scheduler = Scheduler()
        assert scheduler.has_conflicts() is False
    
    def test_has_conflicts_with_overlapping_times(self):
        """Test conflict detection with overlapping task times.

        has_conflicts() reads all_scheduled_tasks (cross-pet pool),
        so we populate that directly to force an overlap scenario.
        task1 runs 10:00-10:30, task2 starts at 10:15 — they overlap.
        """
        scheduler = Scheduler()

        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=30)
        task1.set_scheduled_time(time(10, 0))
        task2.set_scheduled_time(time(10, 15))

        scheduler.all_scheduled_tasks = [task1, task2]

        assert scheduler.has_conflicts() is True

    def test_no_conflicts_with_non_overlapping_times(self):
        """Test no conflicts when tasks are back-to-back with no overlap.

        task1 runs 10:00-10:30, task2 starts at 11:00 — gap between them.
        """
        scheduler = Scheduler()

        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=30)
        task1.set_scheduled_time(time(10, 0))
        task2.set_scheduled_time(time(11, 0))

        scheduler.all_scheduled_tasks = [task1, task2]

        assert scheduler.has_conflicts() is False
    
    def test_schedule_multiple_tasks(self):
        """Test scheduling multiple tasks"""
        scheduler = Scheduler()
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(17, 0))
        
        pet = Pet(name="Buddy", pet_type="dog")
        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=60)
        task3 = Task(task_type="grooming", priority=3, duration=45)
        
        pet.add_requirement(task1)
        pet.add_requirement(task2)
        pet.add_requirement(task3)
        
        scheduled = scheduler.schedule(owner, pet)
        assert len(scheduled) == 3


class TestIntegration:
    """Integration tests for the full system"""
    
    def test_complete_workflow(self):
        """Test complete workflow: create owner, pet, tasks, and schedule"""
        # Create owner
        owner = Owner(name="Alice")
        owner.add_availability_window(time(8, 0), time(12, 0))
        owner.add_availability_window(time(14, 0), time(18, 0))
        
        # Create pet
        pet = Pet(name="Max", pet_type="dog")
        pet.add_health_problem("sensitive stomach")
        owner.add_pet(pet)
        
        # Create tasks
        feeding_task = Task(task_type="feeding", priority=1, duration=20)
        exercise_task = Task(task_type="exercise", priority=2, duration=60)
        meds_task = Task(task_type="medication", priority=1, duration=15)
        
        pet.add_requirement(feeding_task)
        pet.add_requirement(exercise_task)
        pet.add_requirement(meds_task)
        
        # Schedule
        scheduler = Scheduler()
        schedule = scheduler.schedule(owner, pet)
        
        assert len(schedule) == 3
        assert schedule[0].get_priority() == 1
        assert len(owner.get_pets()) == 1
        assert len(owner.get_availability_windows()) == 2
    
    def test_pet_care_tracking(self):
        """Test tracking pet care activities"""
        pet = Pet(name="Fluffy", pet_type="cat")

        # Initial state
        assert not pet.has_been_fed()

        # Feed the pet
        pet.feed()
        assert pet.has_been_fed()
        fed_time = pet.get_last_fed_time()
        assert fed_time is not None

        # Exercise the pet
        pet.exercise()
        exercise_time = pet.get_last_exercise_time()
        assert exercise_time is not None

        # Add health info
        pet.add_health_problem("diabetes")
        assert "diabetes" in pet.get_health_problems()


class TestSortByTime:
    """Tests for Scheduler.sort_by_time()

    sort_by_time() takes any list of Task objects and returns a NEW list
    sorted by scheduled_start_time ascending. Tasks with no time (None)
    go to the end. The original list must not be mutated.
    """

    def test_sorts_tasks_in_chronological_order(self):
        """Tasks added in reverse time order come out sorted earliest-first."""
        scheduler = Scheduler()

        # Create three tasks and assign times out of order
        t1 = Task(task_type="Walk",    priority=1, duration=30)
        t2 = Task(task_type="Feeding", priority=2, duration=15)
        t3 = Task(task_type="Meds",    priority=3, duration=10)

        t1.set_scheduled_time(time(10, 0))   # 10:00
        t2.set_scheduled_time(time(8, 0))    # 08:00  ← earliest
        t3.set_scheduled_time(time(9, 0))    # 09:00

        # Pass them in wrong order — sort_by_time must fix it
        result = scheduler.sort_by_time([t1, t3, t2])

        # Expect 08:00 → 09:00 → 10:00
        assert result[0].get_scheduled_time() == time(8, 0)
        assert result[1].get_scheduled_time() == time(9, 0)
        assert result[2].get_scheduled_time() == time(10, 0)

    def test_none_times_placed_at_end(self):
        """A task with no scheduled time should sort after all timed tasks."""
        scheduler = Scheduler()

        timed   = Task(task_type="Feeding", priority=1, duration=15)
        no_time = Task(task_type="Grooming", priority=2, duration=45)

        timed.set_scheduled_time(time(9, 0))
        # no_time has no scheduled_start_time (None)

        result = scheduler.sort_by_time([no_time, timed])

        # timed task must come first; None task at the end
        assert result[0] == timed
        assert result[1] == no_time

    def test_does_not_mutate_original_list(self):
        """sort_by_time must return a new list, leaving the input unchanged."""
        scheduler = Scheduler()

        t1 = Task(task_type="Walk",    priority=1, duration=30)
        t2 = Task(task_type="Feeding", priority=2, duration=15)
        t1.set_scheduled_time(time(10, 0))
        t2.set_scheduled_time(time(8, 0))

        original = [t1, t2]
        result = scheduler.sort_by_time(original)

        # Original order must be untouched
        assert original[0] == t1
        assert original[1] == t2
        # Result is a different object
        assert result is not original

    def test_already_sorted_list_unchanged(self):
        """A list already in order should come out in the same order."""
        scheduler = Scheduler()

        t1 = Task(task_type="Walk",    priority=1, duration=30)
        t2 = Task(task_type="Feeding", priority=2, duration=15)
        t1.set_scheduled_time(time(8, 0))
        t2.set_scheduled_time(time(9, 0))

        result = scheduler.sort_by_time([t1, t2])

        assert result[0] == t1
        assert result[1] == t2


class TestRecurrence:
    """Tests for Task.mark_complete() recurrence logic.

    When a task has frequency="daily" or "weekly", mark_complete() should:
      - Set the task's own status to "complete"
      - Return a NEW Task with due_date = today + 1 day (daily) or + 7 days (weekly)
      - The new task must be "pending" and preserve type, priority, duration, pet_name

    When frequency=None, mark_complete() returns None (one-off task).
    """

    def test_one_off_task_returns_none(self):
        """mark_complete() on a task with no frequency returns None."""
        task = Task(task_type="Vaccination", priority=1, duration=20)
        result = task.mark_complete()

        assert result is None
        assert task.get_status() == "complete"

    def test_daily_task_creates_next_occurrence(self):
        """Daily task produces a new task due tomorrow."""
        task = Task(task_type="Feeding", priority=1, duration=15, frequency="daily")
        next_task = task.mark_complete()

        assert next_task is not None
        # Due date must be exactly one day after today
        assert next_task.due_date == date.today() + timedelta(days=1)

    def test_weekly_task_creates_next_occurrence(self):
        """Weekly task produces a new task due in 7 days."""
        task = Task(task_type="Grooming", priority=3, duration=45, frequency="weekly")
        next_task = task.mark_complete()

        assert next_task is not None
        assert next_task.due_date == date.today() + timedelta(weeks=1)

    def test_recurring_task_preserves_fields(self):
        """Next occurrence must carry over type, priority, duration, pet_name."""
        task = Task(
            task_type="Morning Walk",
            priority=2,
            duration=30,
            frequency="daily",
            pet_name="Mochi",
        )
        next_task = task.mark_complete()

        assert next_task is not None   # guard: confirms recurrence fired
        assert next_task.get_type()     == "Morning Walk"
        assert next_task.get_priority() == 2
        assert next_task.get_duration() == 30
        assert next_task.pet_name       == "Mochi"
        assert next_task.frequency      == "daily"

    def test_recurring_task_starts_pending(self):
        """Auto-generated next task must start with status 'pending'."""
        task = Task(task_type="Feeding", priority=1, duration=15, frequency="daily")
        next_task = task.mark_complete()

        assert next_task is not None
        assert next_task.get_status() == "pending"

    def test_recurring_task_has_new_id(self):
        """Next occurrence must be a distinct Task with its own unique ID."""
        task = Task(task_type="Feeding", priority=1, duration=15, frequency="daily")
        next_task = task.mark_complete()

        assert next_task is not None
        assert next_task.get_task_id() != task.get_task_id()


class TestScheduleAll:
    """Tests for Scheduler.schedule_all() and cross-pet conflict detection.

    schedule_all() runs every pet's tasks through ONE shared window pool.
    This prevents two pets from being assigned the same time slot.
    """

    def _make_owner(self):
        """Helper: owner with a single 8:00–17:00 window."""
        owner = Owner(name="Jordan")
        owner.add_availability_window(time(8, 0), time(17, 0))
        return owner

    def test_schedule_all_returns_dict_keyed_by_pet_name(self):
        """schedule_all() must return {pet_name: [tasks]} for each pet."""
        owner = self._make_owner()

        dog = Pet(name="Mochi", pet_type="dog")
        dog.add_requirement(Task(task_type="Walk", priority=1, duration=30))
        owner.add_pet(dog)

        cat = Pet(name="Whiskers", pet_type="cat")
        cat.add_requirement(Task(task_type="Feeding", priority=1, duration=10))
        owner.add_pet(cat)

        scheduler = Scheduler()
        result = scheduler.schedule_all(owner)

        assert "Mochi"    in result
        assert "Whiskers" in result

    def test_no_cross_pet_time_conflicts(self):
        """Two pets with equal-priority tasks must not share a time slot."""
        owner = self._make_owner()

        dog = Pet(name="Dog", pet_type="dog")
        dog.add_requirement(Task(task_type="Walk",    priority=1, duration=30))

        cat = Pet(name="Cat", pet_type="cat")
        cat.add_requirement(Task(task_type="Feeding", priority=1, duration=30))

        owner.add_pet(dog)
        owner.add_pet(cat)

        scheduler = Scheduler()
        scheduler.schedule_all(owner)

        # The shared pool means no two tasks can overlap
        assert scheduler.has_conflicts() is False

    def test_filter_by_pet_returns_only_that_pets_tasks(self):
        """filter_by_pet() must return only the tasks belonging to the named pet."""
        owner = self._make_owner()

        dog = Pet(name="Mochi", pet_type="dog")
        dog.add_requirement(Task(task_type="Walk",    priority=1, duration=30))
        dog.add_requirement(Task(task_type="Feeding", priority=2, duration=15))

        cat = Pet(name="Whiskers", pet_type="cat")
        cat.add_requirement(Task(task_type="Feeding", priority=1, duration=10))

        owner.add_pet(dog)
        owner.add_pet(cat)

        scheduler = Scheduler()
        scheduler.schedule_all(owner)

        mochi_tasks    = scheduler.filter_by_pet("Mochi")
        whiskers_tasks = scheduler.filter_by_pet("Whiskers")

        # Mochi has 2 tasks, Whiskers has 1
        assert len(mochi_tasks)    == 2
        assert len(whiskers_tasks) == 1
        # No Whiskers task leaked into Mochi's results
        assert all(t.pet_name == "Mochi"    for t in mochi_tasks)
        assert all(t.pet_name == "Whiskers" for t in whiskers_tasks)

    def test_filter_by_pet_unknown_name_returns_empty(self):
        """Filtering by a pet name that was never scheduled returns []."""
        owner = self._make_owner()
        dog = Pet(name="Mochi", pet_type="dog")
        dog.add_requirement(Task(task_type="Walk", priority=1, duration=30))
        owner.add_pet(dog)

        scheduler = Scheduler()
        scheduler.schedule_all(owner)

        assert scheduler.filter_by_pet("Ghost") == []

    def test_reset_clears_all_state(self):
        """reset() must wipe all accumulated tasks so a fresh schedule starts clean."""
        owner = self._make_owner()
        dog = Pet(name="Mochi", pet_type="dog")
        dog.add_requirement(Task(task_type="Walk", priority=1, duration=30))
        owner.add_pet(dog)

        scheduler = Scheduler()
        scheduler.schedule_all(owner)
        assert len(scheduler.all_scheduled_tasks) > 0

        scheduler.reset()
        assert scheduler.all_scheduled_tasks    == []
        assert scheduler.cached_scheduled_tasks == []
        assert scheduler.cached_skipped_tasks   == []
