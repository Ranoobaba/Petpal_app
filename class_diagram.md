# PawPal+ Class Diagram


classDiagram
    class Owner {
        -name: string
        -availability_start: time
        -availability_end: time
        -pets: list~Pet~
        +set_availability(start_time, end_time)
        +get_availability()
        +add_pet(pet)
        +get_pets(): list~Pet~
    }

    class Pet {
        -name: string
        -type: string
        -health_problems: list
        -is_fed: boolean
        -needs_exercise: boolean
        -requirements: list~Task~
        +feed()
        +has_been_fed(): boolean
        +add_health_problem(problem)
        +get_health_problems(): list
        +needs_exercise(): boolean
        +exercise()
        +add_requirement(task)
        +get_requirements(): list
    }

    class Task {
        -task_type: string
        -priority: int
        -duration: int
        -status: string
        +get_priority(): int
        +get_duration(): int
        +get_type(): string
        +mark_complete()
        +get_status(): string
    }

    class Scheduler {
        -tasks: list~Task~
        +schedule(owner, pet): list~Task~
        +get_scheduled_tasks(): list~Task~
        +has_conflicts(): boolean
        -resolve_priority_queue(): list~Task~
    }

    Owner "1" --> "*" Pet
    Pet "1" --> "*" Task
    Scheduler "1" --> "*" Task

## Class Responsibilities Summary:

**Owner**: Manages owner information and availability window
**Pet**: Tracks pet state (health, feeding, exercise) and requirements
**Task**: Represents individual scheduled activities (feeding, exercise, grooming, meds)
**Scheduler**: Orchestrates scheduling logic using priority queue to organize tasks within owner's availability

This follows the systematic approach we discussed—each class has methods derived from its responsibilities in your system design.
