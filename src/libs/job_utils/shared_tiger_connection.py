import tasktiger
from tasktiger import Task

from src.libs.key_value_utils.key_value_provider import get_key_value_client


def get_shared_tiger_connection():
  conn = get_key_value_client()

  tiger = tasktiger.TaskTiger(connection=conn)

  return tiger


