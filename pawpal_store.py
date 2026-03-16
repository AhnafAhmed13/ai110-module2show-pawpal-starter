from pawpal_system import Owner, Pet, Task, Scheduler


class PawPalStore:
    def __init__(self):
        self._owners: dict[str, Owner] = {}

    # --- Owners ---

    def get_owner_names(self) -> list[str]:
        return list(self._owners.keys())

    def create_owner(self, name: str) -> str | None:
        """Returns an error string on failure, None on success."""
        if name in self._owners:
            return f"Owner '{name}' already exists."
        self._owners[name] = Owner(name)
        return None

    # --- Pets ---

    def get_pets(self, owner_name: str) -> list[dict]:
        owner = self._owners.get(owner_name)
        if not owner:
            return []
        return [{"name": p.name, "species": p.species} for p in owner.pets]

    def add_pet(self, owner_name: str, pet_name: str, species: str) -> str | None:
        """Returns an error string on failure, None on success."""
        owner = self._owners.get(owner_name)
        if not owner:
            return "Owner not found."
        if any(p.name == pet_name for p in owner.pets):
            return f"Pet '{pet_name}' already exists."
        owner.add_pet(Pet(pet_name, species))
        return None

    # --- Tasks ---

    def get_tasks(self, owner_name: str) -> list[dict]:
        owner = self._owners.get(owner_name)
        if not owner:
            return []
        return [
            {"pet": p.name, "title": t.title, "duration_minutes": t.duration, "priority": t.priority}
            for p in owner.pets
            for t in p.tasks
        ]

    def add_task(self, owner_name: str, pet_name: str, title: str, duration: int, priority: str) -> str | None:
        """Returns an error string on failure, None on success."""
        owner = self._owners.get(owner_name)
        if not owner:
            return "Owner not found."
        pet = next((p for p in owner.pets if p.name == pet_name), None)
        if not pet:
            return "Pet not found."
        pet.add_task(Task(title=title, duration=duration, priority=priority))
        return None

    # --- Schedule ---

    def set_available_time(self, owner_name: str, minutes: int) -> None:
        owner = self._owners.get(owner_name)
        if owner:
            owner.available_time = minutes

    def generate_schedule(self, owner_name: str) -> dict:
        owner = self._owners.get(owner_name)
        if not owner:
            return {"scheduled": [], "excluded": []}
        task_to_pet = {id(t): p.name for p in owner.pets for t in p.tasks}
        scheduled = Scheduler(owner).create_schedule()
        scheduled_ids = {id(t) for t in scheduled}
        excluded = [t for p in owner.pets for t in p.tasks if id(t) not in scheduled_ids]

        def to_dict(t):
            return {"pet": task_to_pet.get(id(t), ""), "title": t.title, "duration_minutes": t.duration, "priority": t.priority}

        return {
            "scheduled": [to_dict(t) for t in scheduled],
            "excluded": [to_dict(t) for t in excluded],
        }
