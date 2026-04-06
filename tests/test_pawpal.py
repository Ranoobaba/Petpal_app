import pytest
from datetime import time, datetime, timedelta
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
        """Test conflict detection with overlapping task times"""
        scheduler = Scheduler()
        owner = Owner(name="John")
        owner.add_availability_window(time(9, 0), time(17, 0))
        
        pet = Pet(name="Buddy", pet_type="dog")
        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=30)
        
        pet.add_requirement(task1)
        pet.add_requirement(task2)
        
        scheduler.schedule(owner, pet)
        
        # Set overlapping times
        task1.set_scheduled_time(time(10, 0))
        task2.set_scheduled_time(time(10, 15))
        
        # Note: has_conflicts checks cached_scheduled_tasks
        # After schedule(), tasks should be in cache
        # Setting times manually for this test
        scheduler.cached_scheduled_tasks = [task1, task2]
        
        assert scheduler.has_conflicts() is True
    
    def test_no_conflicts_with_non_overlapping_times(self):
        """Test no conflicts with non-overlapping times"""
        scheduler = Scheduler()
        
        task1 = Task(task_type="feeding", priority=1, duration=30)
        task2 = Task(task_type="exercise", priority=2, duration=30)
        
        task1.set_scheduled_time(time(10, 0))
        task2.set_scheduled_time(time(11, 0))
        
        scheduler.cached_scheduled_tasks = [task1, task2]
        
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
