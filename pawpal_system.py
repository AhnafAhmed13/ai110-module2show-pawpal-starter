from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    description: str
    duration: int = 10
    priority: int = 1
    status: str = "Todo"

    def __str__(self) -> str:
        """Return a formatted string representation of the task."""
        return f"[{self.status}] {self.title} ({self.duration} min) — Priority {self.priority}"

    def mark_complete(self) -> None:
        """Mark the task status as Completed."""
        self.status = "Completed"

@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __str__(self) -> str:
        """Return a formatted string representation of the pet."""
        return f"{self.name} ({self.species})"

    def add_task(self, task: Task) -> None:
        """Append a task to the pet's task list."""
        self.tasks.append(task)

    def print_tasks(self) -> None:
        """Print all tasks for this pet along with the total task count."""
        print(f"{self.name}'s Tasks:")
        for t in self.tasks:
            print('-', t)
        print(f"Task count: {self.get_task_count()}")

    def get_task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)


class Owner:
    def __init__(self, name: str, available_time: int = 30):
        """Initialize an Owner with a name and available time in minutes."""
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to the owner's pet list."""
        self.pets.append(pet)

    def print_pets(self) -> None:
        """Print all pets belonging to this owner."""
        print(f"{self.name}'s Pets:")
        for t in self.pets:
            print('-', t)


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the Scheduler with an owner whose tasks will be scheduled."""
        self.owner = owner

    def create_schedule(self) -> list[Task]:
        """Return a priority-sorted list of tasks that fit within the owner's available time."""
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        sorted_tasks = sorted(all_tasks, key=lambda t: t.priority, reverse=True)

        schedule = []
        remaining_time = self.owner.available_time
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                schedule.append(task)
                remaining_time -= task.duration
        return schedule
