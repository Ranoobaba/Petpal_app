from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from datetime import date, time, datetime, timedelta
import heapq
import uuid
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@dataclass
class Task:
    """Represents a scheduled task for a pet (feeding, exercise, grooming, meds)"""
    task_type: str
    priority: int
    duration: int
    status: str = "pending"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scheduled_start_time: Optional[time] = None
    pet_name: Optional[str] = None
    frequency: Optional[str] = None   # "daily" | "weekly" | None
    due_date: date = field(default_factory=date.today)
    
    def get_priority(self) -> int:
        """Retrieve the priority level of this task"""
        return self.priority
    
    def get_duration(self) -> int:
        """Retrieve the duration required for this task"""
        return self.duration
    
    def get_type(self) -> str:
        """Retrieve the type of task"""
        return self.task_type
    
    def mark_complete(self) -> Optional["Task"]:
        """
        Mark this task as complete.

        If the task has a frequency, returns a new Task instance due on the
        next occurrence (today + 1 day for daily, + 7 days for weekly).
        Returns None for one-off tasks.
        """
        self.status = "complete"
        logger.info(f"Task '{self.task_type}' marked complete (frequency={self.frequency})")

        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        next_task = Task(
            task_type=self.task_type,
            priority=self.priority,
            duration=self.duration,
            frequency=self.frequency,
            due_date=self.due_date + delta,
            pet_name=self.pet_name,
        )
        logger.info(f"Next '{next_task.task_type}' auto-created — due {next_task.due_date}")
        return next_task
    
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
        logger.info(f"Pet '{self.name}' has been fed at {self.last_fed_time.strftime('%H:%M:%S')}")
    
    def get_last_fed_time(self) -> Optional[datetime]:
        """Get the last time the pet was fed"""
        return self.last_fed_time
    
    def has_been_fed(self) -> bool:
        """Check if pet has been fed at least once"""
        return self.last_fed_time is not None
    
    def add_health_problem(self, problem: str) -> None:
        """Add a health problem to the pet's record"""
        self.health_problems.append(problem)
        logger.warning(f"Health issue added for pet '{self.name}': {problem}")
    
    def get_health_problems(self) -> List[str]:
        """Retrieve list of health problems"""
        return self.health_problems
    
    def get_last_exercise_time(self) -> Optional[datetime]:
        """Get the last time the pet exercised"""
        return self.last_exercise_time
    
    def exercise(self) -> None:
        """Mark that the pet has exercised with current timestamp"""
        self.last_exercise_time = datetime.now()
        logger.info(f"Pet '{self.name}' has exercised at {self.last_exercise_time.strftime('%H:%M:%S')}")
    
    def add_requirement(self, task: Task) -> None:
        """Add a task requirement for this pet"""
        task.pet_name = self.name
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
        logger.info(f"Owner '{self.name}' now has pet '{pet.name}' ({pet.pet_type})")
    
    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner"""
        return self.pets


@dataclass
class Scheduler:
    """Orchestrates scheduling of tasks based on owner availability and pet requirements"""
    priority_heap: List[tuple] = field(default_factory=list)
    cached_scheduled_tasks: List[Task] = field(default_factory=list)
    cached_skipped_tasks: List[Task] = field(default_factory=list)
    all_scheduled_tasks: List[Task] = field(default_factory=list)
    
    def schedule(self, owner: Owner, pet: Pet) -> List[Task]:
        """
        Create a prioritized schedule of tasks for a pet within owner's availability.

        Applies priority boosts for overdue feeding and health conditions before
        scheduling. Merges overlapping availability windows. Accumulates results
        into all_scheduled_tasks for cross-pet conflict detection.

        Args:
            owner: The owner with availability constraints
            pet: The pet with task requirements

        Returns:
            A list of tasks that fit within availability, sorted by scheduled time
        """
        all_tasks = pet.get_requirements()
        self._apply_priority_boosts(all_tasks, pet)
        merged_availability = self._merge_windows(owner.get_availability_windows())
        scheduled_tasks = self._resolve_priority_queue(all_tasks, merged_availability)
        self.all_scheduled_tasks.extend(scheduled_tasks)
        return scheduled_tasks

    def schedule_all(self, owner: Owner) -> dict:
        """
        Schedule all pets' tasks into a single shared window pool.

        Prevents cross-pet conflicts by consuming window time globally — once a
        slot is used for one pet's task, it is unavailable to all other pets.

        Args:
            owner: The owner whose pets and availability windows are used

        Returns:
            Dict mapping pet name → list of scheduled tasks (sorted by time)
        """
        all_tasks = []
        for pet in owner.get_pets():
            self._apply_priority_boosts(pet.get_requirements(), pet)
            all_tasks.extend(pet.get_requirements())

        merged_availability = self._merge_windows(owner.get_availability_windows())
        scheduled = self._resolve_priority_queue(all_tasks, merged_availability)
        self.all_scheduled_tasks = scheduled

        result: dict = {}
        for task in scheduled:
            key = task.pet_name or "unknown"
            result.setdefault(key, []).append(task)
        return result

    def reset(self) -> None:
        """Clear all accumulated state before regenerating a full schedule"""
        self.priority_heap = []
        self.cached_scheduled_tasks = []
        self.cached_skipped_tasks = []
        self.all_scheduled_tasks = []
    
    def get_scheduled_tasks(self) -> List[Task]:
        """Retrieve the cached list of scheduled tasks in priority order"""
        return self.cached_scheduled_tasks

    def get_skipped_tasks(self) -> List[Task]:
        """Retrieve tasks that could not be scheduled in any availability window"""
        return self.cached_skipped_tasks

    def filter_by_status(self, status: str) -> List[Task]:
        """
        Filter all scheduled tasks (across all pets) by completion status.

        Args:
            status: "pending" or "complete"

        Returns:
            List of tasks whose status matches the given value
        """
        return [t for t in self.all_scheduled_tasks if t.get_status() == status]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """
        Filter all scheduled tasks to those belonging to a specific pet.

        Args:
            pet_name: The name of the pet to filter by

        Returns:
            List of tasks assigned to that pet, in their current order
        """
        return [t for t in self.all_scheduled_tasks if t.pet_name == pet_name]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort a list of tasks by their scheduled start time ascending.

        Tasks with no scheduled time (None) are placed at the end.

        Args:
            tasks: Any list of Task objects

        Returns:
            A new sorted list — the original list is not modified
        """
        return sorted(tasks, key=lambda t: t.get_scheduled_time() or time.max)

    @staticmethod
    def _merge_windows(windows: List[Tuple[time, time]]) -> List[Tuple[time, time]]:
        """
        Merge overlapping or adjacent availability windows into minimal spans.

        Prevents double-counting available time when the owner adds windows
        that overlap (e.g. 8:00–12:00 and 10:00–13:00 → 8:00–13:00).

        Args:
            windows: List of (start, end) time tuples, any order

        Returns:
            Sorted list of non-overlapping (start, end) tuples
        """
        if not windows:
            return []
        sorted_windows = sorted(windows)
        merged = [[sorted_windows[0][0], sorted_windows[0][1]]]
        for start, end in sorted_windows[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return [(s, e) for s, e in merged]

    def _apply_priority_boosts(self, tasks: List[Task], pet: Pet) -> None:
        """
        Boost task priorities based on pet health conditions and feeding state.

        - Overdue feeding (>6 hours since last fed): feeding task → priority 1
        - Health keyword match: lower priority number by 1 (min 1)
        """
        HEALTH_KEYWORDS = {
            "walk": {"knee", "joint", "arthritis", "hip"},
            "feed": {"diabetes", "kidney", "liver", "diet"},
        }
        last_fed = pet.get_last_fed_time()
        overdue_feeding = (
            last_fed is not None
            and (datetime.now() - last_fed).total_seconds() > 21600
        )
        for task in tasks:
            task_lower = task.get_type().lower()
            if "feed" in task_lower and overdue_feeding:
                task.priority = 1
                logger.info(f"Priority boosted: '{task.get_type()}' for '{pet.name}' — overdue feeding")
            for keyword, conditions in HEALTH_KEYWORDS.items():
                if keyword in task_lower:
                    for problem in pet.get_health_problems():
                        if any(c in problem.lower() for c in conditions):
                            task.priority = max(1, task.priority - 1)
                            logger.info(f"Priority boosted: '{task.get_type()}' for '{pet.name}' — health: {problem}")
                            break

    def has_conflicts(self) -> bool:
        """Check for overlapping tasks across all pets in the current schedule"""
        scheduled_times = []
        for task in self.all_scheduled_tasks:
            start = task.get_scheduled_time()
            if start is None:
                continue
            end_minutes = start.hour * 60 + start.minute + task.get_duration()
            end = time(end_minutes // 60, end_minutes % 60)
            for existing_start, existing_end in scheduled_times:
                if start < existing_end and end > existing_start:
                    logger.error(f"Conflict: '{task.get_type()}' at {start} overlaps {existing_start}-{existing_end}")
                    return True
            scheduled_times.append((start, end))
        logger.debug("Conflict check passed: no overlapping tasks")
        return False
    
    def _resolve_priority_queue(
        self, tasks: List[Task], availability: List[Tuple[time, time]]
    ) -> List[Task]:
        """
        Prioritize tasks using a min heap and fit them into owner's availability windows.

        For each task (in priority order), we try to place it in the earliest
        window that has enough remaining minutes.  If no window can hold the
        task, it is skipped entirely (no partial completions).

        Args:
            tasks: List of tasks to prioritize and schedule
            availability: Owner's (start, end) time windows, already sorted

        Returns:
            Tasks that fit, ordered by their assigned start time
        """
        # Clear previous heap
        self.priority_heap = []

        # Build min heap: (priority, task_id, task)
        for task in tasks:
            heapq.heappush(
                self.priority_heap,
                (task.get_priority(), task.get_task_id(), task),
            )

        # Build a mutable list of windows tracking the next available start
        # Each entry: [current_start, window_end]  (both as total minutes since midnight)
        windows = []
        for start, end in sorted(availability):
            windows.append([start.hour * 60 + start.minute,
                            end.hour * 60 + end.minute])

        scheduled_tasks: List[Task] = []
        skipped_tasks: List[Task] = []

        while self.priority_heap:
            priority, task_id, task = heapq.heappop(self.priority_heap)
            duration = task.get_duration()
            placed = False
            for window in windows:
                if window[1] - window[0] >= duration:
                    start_hour, start_min = divmod(window[0], 60)
                    task.set_scheduled_time(time(start_hour, start_min))
                    window[0] += duration
                    scheduled_tasks.append(task)
                    placed = True
                    break
            if not placed:
                skipped_tasks.append(task)

        # Second pass: fill remaining window gaps with skipped tasks (bin-packing)
        still_skipped: List[Task] = []
        for task in skipped_tasks:
            duration = task.get_duration()
            placed = False
            for window in windows:
                if window[1] - window[0] >= duration:
                    start_hour, start_min = divmod(window[0], 60)
                    task.set_scheduled_time(time(start_hour, start_min))
                    window[0] += duration
                    scheduled_tasks.append(task)
                    placed = True
                    logger.info(f"'{task.get_type()}' placed in second-pass bin-packing")
                    break
            if not placed:
                still_skipped.append(task)
                logger.warning(f"Could not schedule '{task.get_type()}' (duration={task.get_duration()}min) — no window fits")

        scheduled_tasks.sort(key=lambda t: t.get_scheduled_time() or time.max)
        self.cached_scheduled_tasks = scheduled_tasks
        self.cached_skipped_tasks = still_skipped

        return scheduled_tasks
