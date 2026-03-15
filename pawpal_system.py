from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    description: str
    duration: int
    priority: int
    status: str


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str, available_time: int = 30):
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def create_schedule(self) -> list[Task]:
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        sorted_tasks = sorted(all_tasks, key=lambda t: t.priority)

        schedule = []
        remaining_time = self.owner.available_time
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                schedule.append(task)
                remaining_time -= task.duration
        return schedule
