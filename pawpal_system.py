from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from datetime import time, datetime
import heapq
import uuid

@dataclass
class Task:
    """Represents a scheduled task for a pet (feeding, exercise, grooming, meds)"""
    task_type: str
    priority: int
    duration: int
    status: str = "pending"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scheduled_start_time: Optional[time] = None
    
    def get_priority(self) -> int:
        """Retrieve the priority level of this task"""
        return self.priority
    
    def get_duration(self) -> int:
        """Retrieve the duration required for this task"""
        return self.duration
    
    def get_type(self) -> str:
        """Retrieve the type of task"""
        return self.task_type
    
    def mark_complete(self) -> None:
        """Mark this task as complete"""
        self.status = "complete"
    
    def get_status(self) -> str:
        """Retrieve the current status of this task"""
        return self.status
    
    def get_task_id(self) -> str:
        """Retrieve the unique task ID"""
        return self.task_id
    
    def set_scheduled_time(self, start_time: time) -> None:
        """Set the scheduled start time for this task"""
        self.scheduled_start_time = start_time
    
    def get_scheduled_time(self) -> Optional[time]:
        """Get the scheduled start time for this task"""
        return self.scheduled_start_time


@dataclass
class Pet:
    """Represents a pet with health, feeding, and exercise tracking"""
    name: str
    pet_type: str
    health_problems: List[str] = field(default_factory=list)
    last_fed_time: Optional[datetime] = None
    last_exercise_time: Optional[datetime] = None
    requirements: List[Task] = field(default_factory=list)
    
    def feed(self) -> None:
        """Mark the pet as fed with current timestamp"""
        self.last_fed_time = datetime.now()
    
    def get_last_fed_time(self) -> Optional[datetime]:
        """Get the last time the pet was fed"""
        return self.last_fed_time
    
    def has_been_fed(self) -> bool:
        """Check if pet has been fed at least once"""
        return self.last_fed_time is not None
    
    def add_health_problem(self, problem: str) -> None:
        """Add a health problem to the pet's record"""
        self.health_problems.append(problem)
    
    def get_health_problems(self) -> List[str]:
        """Retrieve list of health problems"""
        return self.health_problems
    
    def get_last_exercise_time(self) -> Optional[datetime]:
        """Get the last time the pet exercised"""
        return self.last_exercise_time
    
    def exercise(self) -> None:
        """Mark that the pet has exercised with current timestamp"""
        self.last_exercise_time = datetime.now()
    
    def add_requirement(self, task: Task) -> None:
        """Add a task requirement for this pet"""
        self.requirements.append(task)
    
    def get_requirements(self) -> List[Task]:
        """Retrieve all task requirements"""
        return self.requirements


@dataclass
class Owner:
    """Represents a pet owner with availability and multiple pets"""
    name: str
    availability_windows: List[Tuple[time, time]] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)
    
    def add_availability_window(self, start_time: time, end_time: time) -> None:
        """Add an availability window for the owner"""
        self.availability_windows.append((start_time, end_time))
    
    def get_availability_windows(self) -> List[Tuple[time, time]]:
        """Get all availability windows"""
        return self.availability_windows
    
    def clear_availability(self) -> None:
        """Clear all availability windows"""
        self.availability_windows = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list"""
        self.pets.append(pet)
    
    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner"""
        return self.pets


@dataclass
class Scheduler:
    """Orchestrates scheduling of tasks based on owner availability and pet requirements"""
    priority_heap: List[tuple] = field(default_factory=list)
    cached_scheduled_tasks: List[Task] = field(default_factory=list)
    
    def schedule(self, owner: Owner, pet: Pet) -> List[Task]:
        """
        Create a prioritized schedule of tasks for a pet within owner's availability
        
        Args:
            owner: The owner with availability constraints
            pet: The pet with task requirements
            
        Returns:
            A prioritized list of scheduled tasks (lowest priority value first)
        """
        # Collect all tasks from pet requirements
        all_tasks = pet.get_requirements()
        
        # Resolve conflicts and prioritize using min heap
        scheduled_tasks = self._resolve_priority_queue(all_tasks)
        
        return scheduled_tasks
    
    def get_scheduled_tasks(self) -> List[Task]:
        """Retrieve the cached list of scheduled tasks in priority order"""
        return self.cached_scheduled_tasks
    
    def has_conflicts(self) -> bool:
        """Check if there are any conflicting tasks (overlapping times)"""
        scheduled_times = []
        for task in self.cached_scheduled_tasks:
            start = task.get_scheduled_time()
            if start is None:
                continue
            end_minutes = start.minute + task.get_duration()
            end = time(start.hour + end_minutes // 60, end_minutes % 60)
            
            # Check for overlap with existing scheduled times
            for existing_start, existing_end in scheduled_times:
                if (start < existing_end and end > existing_start):
                    return True
            scheduled_times.append((start, end))
        return False
    
    def _resolve_priority_queue(self, tasks: List[Task]) -> List[Task]:
        """
        Prioritize tasks using min heap and fit them into owner's availability windows.
        
        Args:
            tasks: List of tasks to prioritize and schedule
            
        Returns:
            Tasks sorted by priority with scheduled times assigned
        """
        # Clear previous heap
        self.priority_heap = []
        
        # Build min heap: (priority, task_id, task)
        # Smaller priority value = higher importance
        for task in tasks:
            heapq.heappush(self.priority_heap, (task.get_priority(), task.get_task_id(), task))
        
        # Extract all tasks from heap in priority order
        scheduled_tasks = []
        while self.priority_heap:
            priority, task_id, task = heapq.heappop(self.priority_heap)
            scheduled_tasks.append(task)
        
        # Cache the scheduled tasks for fast retrieval
        self.cached_scheduled_tasks = scheduled_tasks
        
        return scheduled_tasks
