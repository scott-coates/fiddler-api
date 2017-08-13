import tasktiger
from tasktiger import Task

from src.libs.key_value_utils.key_value_provider import get_key_value_client


def get_shared_tiger_connection():
  conn = get_key_value_client()

  tiger = tasktiger.TaskTiger(connection=conn)

  return tiger


def retry_tasks(queue='default', state='error'):
  tiger = get_shared_tiger_connection()
  n, tasks = Task.tasks_from_queue(tiger, queue, state)
  for task in tasks:
    task.retry()

  return n
