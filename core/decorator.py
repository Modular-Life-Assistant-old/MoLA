from circuits import task


def async(f):
    def inner(self, *args, **kwargs):
        return self.call(task(f, self, *args, **kwargs), 'worker')
    return inner


def threaded(f):
    def inner(self, *args, **kwargs):
        self.fire(task(f, self, *args, **kwargs), 'worker')
    return inner
