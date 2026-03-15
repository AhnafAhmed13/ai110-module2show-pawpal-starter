from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration: int
    priority: str


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, available_time: int = 30):
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass


def create_schedule(owner: Owner) -> list[Task]:
    pass
