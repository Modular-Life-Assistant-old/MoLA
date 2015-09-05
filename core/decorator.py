def threaded(f):
    def inner(self, *args, **kwargs):
        self.fire(task(f, self, *args, **kwargs), 'worker')
    return inner
