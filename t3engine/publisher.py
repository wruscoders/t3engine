import functools


class pub_mixin():
    def __init__(self):
        self.publisher = publisher()

    def sub(self, observer):
        self.publisher.sub(observer)

    def unsub(self, observer):
        self.publisher.unsub(observer)


class publisher():
    def __init__(self):
        self.subs = []

    def sub(self, observer):
        if observer not in self.subs:
            self.subs.append(observer)

    def unsub(self, observer):
        if observer in self.subs:
            self.subs.remove(observer)

    def pub(self, fname, *args, **kwargs):
        for sub in self.subs:
            f = getattr(sub, fname, None)
            if callable(f):
                f(*args[1:], **kwargs)


def pub(f):
    @functools.wraps(f)
    def pub_action_wrapper(*args, **kwargs):
        args[0].publisher.pub(f.__name__, *args, **kwargs)
        return f(*args, **kwargs)

    return pub_action_wrapper
