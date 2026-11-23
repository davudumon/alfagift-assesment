import pytest
from pydantic import ValidationError

from app.schemas import TaskCreate, TaskUpdate


def test_task_create_accepts_valid_payload():
    task = TaskCreate(title="Write report", description="Prepare a summary", status="Todo")

    assert task.title == "Write report"
    assert task.status == "Todo"


def test_task_create_rejects_empty_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="   ", description="")


def test_task_create_rejects_unknown_status():
    with pytest.raises(ValidationError):
        TaskCreate(title="Write report", status="Blocked")


def test_task_update_supports_partial_payload():
    task = TaskUpdate(status="Done")

    assert task.status == "Done"
    assert task.title is None
