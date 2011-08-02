from pycommon.actors.actor import ThreadedActor, ActorRef
from pycommon.actors.manager import Manager
import multiprocessing
import signal
import time
import os
from proc_actor import process_actor

def pytest_funcarg__qm(request):
    return request.cached_setup(
        setup=create_queue_manager,
        teardown=lambda x: x.stop(),
        scope='session')

class _threaded_actor(ThreadedActor):

    def reply(self, msg):
        sender = ActorRef(msg['reply_to'])
        sender.send({'tag': 'answer',
                     'answer': 5})

    def queue(self, msg):
        sender = ActorRef(msg['reply_to'])
        sender.send({'tag': 'answer',
                     'answer': 2})

    def act(self):
        q = []
        while not q:
            self.receive({
                'reply': 'reply',
                'queue': 'queue',
                'stop': lambda msg: q.append(1)})


def create_queue_manager():
    qm = Manager()
    qm.start()
    t = _threaded_actor('t')
    process_actor()
    #p = _process_actor('p')
    return qm
