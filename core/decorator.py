from circuits import task, Worker


def threaded(f):
    def inner(self, *args, **kwargs):
        Worker().register(self)
        self.fire(task(f, self, *args, **kwargs))
    return inner
