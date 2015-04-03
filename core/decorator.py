from circuits import task


def async(f):
    def inner(self, *args, **kwargs):
        return self.call(task(f, self, *args, **kwargs), 'worker')
    return inner


def mutex(f):
    def inner(self, *args, **kwargs):
        key = '%s-%s-%s' % (str(f), str(args), str(kwargs))

        if hasattr(self, 'mutex_decorator'):
            while key in self.mutex_decorator:
                yield

            self.mutex_decorator.append(key)

        else:
            self.mutex_decorator = [key]

        yield from f(self, *args, **kwargs)
        self.mutex_decorator.remove(key)
    return inner


def threaded(f):
    def inner(self, *args, **kwargs):
        self.fire(task(f, self, *args, **kwargs), 'worker')
    return inner
