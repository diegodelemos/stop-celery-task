# Stop a celery task get state from killed task on signal handler...

## Prerequisites

You should have a RabbitMQ service running, the quickest way is to run it
through Docker:

```console
$ docker run -d --hostname the-rabbitmq --name the-rabbitmq rabbitmq:3
1b4053895f7c03421d4230ccb17473a065e8150013b2b28d27dffdeeca62f3eb
```

## How to run the toy example

Create a virtual environment to make sure dependencies are controlled:
```console
$ mkvirtualenv playground
(playground) $ pip install celery  # currently 4.2.1
```

Clone the repo, go inside the project an run the Celery application:
```console
$ celery -A tasks worker --loglevel=info
celery@mb-rodrigdi.dyndns.cern.ch v4.2.1 (windowlicker)
Darwin-18.0.0-x86_64-i386-64bit 2018-11-15 11:23:45
[config]
.> app:         tasks:0x103580790
.> transport:   amqp://guest:**@localhost:5672//
.> results:     rpc://
.> concurrency: 12 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery


[tasks]
  . tasks.add
  . tasks.sleep_a_bit

[2018-11-15 11:23:46,205: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2018-11-15 11:23:46,223: INFO/MainProcess] mingle: searching for neighbors
[2018-11-15 11:23:47,265: INFO/MainProcess] mingle: all alone
[2018-11-15 11:23:47,286: INFO/MainProcess] celery@mb-rodrigdi.dyndns.cern.ch ready.
```

On a different shell, we are going to start a new task and kill it...:
```console
$ pip install ipython
$ ipython
ipython
Python 2.7.15 (default, Aug 22 2018, 16:36:18)
Type "copyright", "credits" or "license" for more information.

IPython 5.8.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.
In [1]: from tasks import sleep_a_bit

In [2]: from celery.task.control import revoke

In [3]: my_task_id = 'try_number_1'

In [4]: res = sleep_a_bit.apply_async((10,), task_id=my_task_id)

In [5]: revoke(my_task_id, terminate=True)

```

##