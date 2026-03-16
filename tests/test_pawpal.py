from pawpal_system import Task, Pet, Owner, Scheduler
from pawpal_store import PawPalStore


# ── Task ──────────────────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task(title="Feed", duration=5, priority="low")
    task.mark_complete()
    assert task.status == "Completed"


def test_task_default_status_is_todo():
    task = Task(title="Walk", duration=20, priority="high")
    assert task.status == "Todo"


def test_task_str_includes_title_duration_priority():
    task = Task(title="Brush", duration=10, priority="medium")
    s = str(task)
    assert "Brush" in s
    assert "10" in s
    assert "medium" in s


def test_task_default_duration_and_priority():
    task = Task(title="Nap")
    assert task.duration == 10
    assert task.priority == "low"


# ── Pet ───────────────────────────────────────────────────────────────────────

def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog")
    task = Task(title="Walk", duration=20, priority="high")
    pet.add_task(task)
    assert pet.get_task_count() == 1


def test_new_pet_has_zero_tasks():
    pet = Pet(name="Luna", species="Cat")
    assert pet.get_task_count() == 0


def test_add_multiple_tasks():
    pet = Pet(name="Max", species="Dog")
    pet.add_task(Task(title="Walk", duration=20, priority="high"))
    pet.add_task(Task(title="Feed", duration=5, priority="medium"))
    pet.add_task(Task(title="Groom", duration=15, priority="low"))
    assert pet.get_task_count() == 3


def test_pet_str_includes_name_and_species():
    pet = Pet(name="Mochi", species="Cat")
    s = str(pet)
    assert "Mochi" in s
    assert "Cat" in s


# ── Owner ─────────────────────────────────────────────────────────────────────

def test_owner_default_available_time():
    owner = Owner("Alice")
    assert owner.available_time == 60


def test_owner_custom_available_time():
    owner = Owner("Bob", available_time=120)
    assert owner.available_time == 120


def test_add_pet_to_owner():
    owner = Owner("Carol")
    owner.add_pet(Pet("Rex", "Dog"))
    assert len(owner.pets) == 1


def test_get_pet_returns_correct_pet():
    owner = Owner("Dave")
    owner.add_pet(Pet("Whiskers", "Cat"))
    found = owner.get_pet("Whiskers", "Cat")
    assert found is not None
    assert found.name == "Whiskers"


def test_get_pet_wrong_species_returns_none():
    owner = Owner("Eve")
    owner.add_pet(Pet("Spot", "Dog"))
    assert owner.get_pet("Spot", "Cat") is None


def test_get_pet_missing_returns_none():
    owner = Owner("Frank")
    assert owner.get_pet("Ghost", "Dog") is None


def test_get_all_tasks_across_pets():
    owner = Owner("Grace")
    dog = Pet("Rex", "Dog")
    cat = Pet("Luna", "Cat")
    dog.add_task(Task("Walk", 20, "high"))
    cat.add_task(Task("Feed", 5, "medium"))
    cat.add_task(Task("Play", 10, "low"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    assert len(owner.get_all_tasks()) == 3


def test_get_all_tasks_no_pets_returns_empty():
    owner = Owner("Hank")
    assert owner.get_all_tasks() == []


# ── Scheduler ─────────────────────────────────────────────────────────────────

def test_scheduler_returns_tasks_that_fit():
    owner = Owner("Iris", available_time=30)
    pet = Pet("Buddy", "Dog")
    pet.add_task(Task("Walk", 20, "high"))
    pet.add_task(Task("Feed", 5, "medium"))
    owner.add_pet(pet)
    schedule = Scheduler(owner).create_schedule()
    assert len(schedule) == 2


def test_scheduler_excludes_tasks_that_dont_fit():
    owner = Owner("Jake", available_time=10)
    pet = Pet("Biscuit", "Dog")
    pet.add_task(Task("Walk", 20, "high"))   # too long
    pet.add_task(Task("Feed", 5, "medium"))  # fits
    owner.add_pet(pet)
    schedule = Scheduler(owner).create_schedule()
    titles = [t.title for t in schedule]
    assert "Walk" not in titles
    assert "Feed" in titles


def test_scheduler_orders_by_priority_high_first():
    owner = Owner("Karen", available_time=60)
    pet = Pet("Pip", "Cat")
    pet.add_task(Task("Low task", 5, "low"))
    pet.add_task(Task("High task", 5, "high"))
    pet.add_task(Task("Med task", 5, "medium"))
    owner.add_pet(pet)
    schedule = Scheduler(owner).create_schedule()
    assert schedule[0].title == "High task"
    assert schedule[1].title == "Med task"
    assert schedule[2].title == "Low task"


def test_scheduler_empty_tasks_returns_empty():
    owner = Owner("Leo", available_time=60)
    owner.add_pet(Pet("Ghost", "Cat"))
    schedule = Scheduler(owner).create_schedule()
    assert schedule == []


def test_scheduler_exact_time_fit():
    owner = Owner("Mia", available_time=25)
    pet = Pet("Dot", "Dog")
    pet.add_task(Task("Walk", 20, "high"))
    pet.add_task(Task("Feed", 5, "medium"))
    owner.add_pet(pet)
    schedule = Scheduler(owner).create_schedule()
    assert sum(t.duration for t in schedule) == 25


def test_scheduler_zero_available_time_schedules_nothing():
    owner = Owner("Ned", available_time=0)
    pet = Pet("Chip", "Dog")
    pet.add_task(Task("Feed", 5, "medium"))
    owner.add_pet(pet)
    schedule = Scheduler(owner).create_schedule()
    assert schedule == []


# ── PawPalStore ───────────────────────────────────────────────────────────────

def test_store_create_owner_succeeds():
    store = PawPalStore()
    error = store.create_owner("Alice")
    assert error is None
    assert "Alice" in store.get_owner_names()


def test_store_create_duplicate_owner_returns_error():
    store = PawPalStore()
    store.create_owner("Alice")
    error = store.create_owner("Alice")
    assert error is not None


def test_store_get_owner_names_empty():
    store = PawPalStore()
    assert store.get_owner_names() == []


def test_store_add_pet_succeeds():
    store = PawPalStore()
    store.create_owner("Bob")
    error = store.add_pet("Bob", "Rex", "dog")
    assert error is None
    pets = store.get_pets("Bob")
    assert any(p["name"] == "Rex" for p in pets)


def test_store_add_duplicate_pet_returns_error():
    store = PawPalStore()
    store.create_owner("Carol")
    store.add_pet("Carol", "Luna", "cat")
    error = store.add_pet("Carol", "Luna", "cat")
    assert error is not None


def test_store_add_pet_unknown_owner_returns_error():
    store = PawPalStore()
    error = store.add_pet("Nobody", "Rex", "dog")
    assert error is not None


def test_store_get_pets_unknown_owner_returns_empty():
    store = PawPalStore()
    assert store.get_pets("Nobody") == []


def test_store_add_task_succeeds():
    store = PawPalStore()
    store.create_owner("Dave")
    store.add_pet("Dave", "Buddy", "dog")
    error = store.add_task("Dave", "Buddy", "Walk", 20, "high")
    assert error is None
    tasks = store.get_tasks("Dave")
    assert any(t["title"] == "Walk" for t in tasks)


def test_store_add_task_unknown_owner_returns_error():
    store = PawPalStore()
    error = store.add_task("Nobody", "Buddy", "Walk", 20, "high")
    assert error is not None


def test_store_add_task_unknown_pet_returns_error():
    store = PawPalStore()
    store.create_owner("Eve")
    error = store.add_task("Eve", "Ghost", "Walk", 20, "high")
    assert error is not None


def test_store_get_tasks_includes_pet_name():
    store = PawPalStore()
    store.create_owner("Frank")
    store.add_pet("Frank", "Mochi", "cat")
    store.add_task("Frank", "Mochi", "Feed", 5, "medium")
    tasks = store.get_tasks("Frank")
    assert tasks[0]["pet"] == "Mochi"


def test_store_get_tasks_unknown_owner_returns_empty():
    store = PawPalStore()
    assert store.get_tasks("Nobody") == []


def test_store_generate_schedule_returns_scheduled_and_excluded_keys():
    store = PawPalStore()
    store.create_owner("Grace")
    store.add_pet("Grace", "Rex", "dog")
    store.add_task("Grace", "Rex", "Walk", 20, "high")
    store.set_available_time("Grace", 60)
    result = store.generate_schedule("Grace")
    assert "scheduled" in result
    assert "excluded" in result


def test_store_generate_schedule_respects_available_time():
    store = PawPalStore()
    store.create_owner("Hank")
    store.add_pet("Hank", "Dot", "dog")
    store.add_task("Hank", "Dot", "Walk", 30, "high")
    store.add_task("Hank", "Dot", "Bath", 60, "low")
    store.set_available_time("Hank", 30)
    result = store.generate_schedule("Hank")
    assert any(t["title"] == "Walk" for t in result["scheduled"])
    assert any(t["title"] == "Bath" for t in result["excluded"])


def test_store_generate_schedule_unknown_owner_returns_empty():
    store = PawPalStore()
    result = store.generate_schedule("Nobody")
    assert result == {"scheduled": [], "excluded": []}
