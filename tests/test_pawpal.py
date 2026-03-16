from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Feed", description="Feed the pet", duration=5, priority=2)
    task.mark_complete()
    assert task.status == "Completed"


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog")
    task = Task(title="Walk", description="Walk the dog", duration=20, priority=1)
    pet.add_task(task)
    assert pet.get_task_count() == 1
