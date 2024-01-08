from celery.contrib.abortable import AbortableTask
from celery import shared_task, Task

from . import db
from .models import LongRunningTask
from .snowflake_connector import SnowFlake


class TaskStatus:
    SCHEDULED = "SCHEDULED"
    STARTED = "STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    ABORTED_BY_USER = "ABORTED_BY_USER"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@shared_task(name="long_running_task", retry_kwargs={'max_retries': 0}, bind=True, base=AbortableTask)
def long_running_task_celery(self: Task, connection_id: int) -> object:

    task_id = self.request.id
    snowflake = SnowFlake(connection_id=connection_id)

    con = snowflake.connect()
    if con is None:
        raise ConnectionError(f"No Connection With {connection_id=}")
    connection_identifier = snowflake.identifier
    task = LongRunningTask(
        task_id=task_id, status=TaskStatus.STARTED, connection_name=connection_identifier, output=None)
    db.session.add(task)
    db.session.commit()
