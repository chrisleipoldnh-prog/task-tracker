from schemas import TaskCreate, TaskUpdate


def test_create_task():
    task = TaskCreate(title="Learn CI/CD")
    assert task.title == "Learn CI/CD"


def test_update_task_completed():
    task = TaskUpdate(completed=True)
    assert task.completed is True
    assert task.title is None
