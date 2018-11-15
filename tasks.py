"""."""

import time

from billiard.exceptions import Terminated
from celery import Celery, Task, current_app
from celery.signals import task_revoked

app = Celery('tasks', backend='rpc://',
             broker='amqp://guest@localhost//')

app.conf.update(CELERY_RESULT_BACKEND='rpc')

class MyTask(Task):
    """."""

    def __init__(self):
        """."""
        self.current_second = None

@app.task
def add(x, y):
    """Quick task."""
    print('Adding {} plus {}.'.format(x, y))
    return x + y


@app.task(bind=True, base=MyTask)
def sleep_a_bit(self, second):
    """Long running task which sleeps for a given number of seconds."""
    current_second = 0
    for n in range(second):
        current_second = n + 1
        print('Working ... {}/{}.'.format(current_second, second))
        time.sleep(1)
    return 'I sleep all the {second} seconds ...'.format(second=second)


@task_revoked.connect()
def on_task_revoked(*args, **kwargs):
    """Handle the event of killing a task."""
    print('I want to know in which second ``sleep_a_bit`` stopped working...')
    print('I know which task id was  killed: {}'.format(kwargs['request'].id))
    print('I can not access the original task since '
          '``kwargs[\'request\'].task.current_second is not set.')
    # The task object is new since Celery can not guarantee the task to run
    # in the same thread or even process.
