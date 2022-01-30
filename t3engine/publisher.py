""" Implements the observer pattern as a mixin using decoraators.

A class may inherit from pub_mixin to allow selected methods to
be observed by external subscribers. The inheriting class may
wrap functions using the @pub decorator to provide subscribers
notification when those methods are called.

Subscribers should pass an object that implements methods with the
same name as the decorated methods of the class to which they are
subscribing. Whenever the decorated functions are called, the
observers corresponding method will be called with the same arguments.
The provider may send additional state information with notifications.
Consult the documentation for the subscribed class to see what
additional information is provided, if any.
"""

import functools

class pub_mixin():
    """ An inheritable mixin that provides hooks for the observer pattern.

    Classes wishing to be observable can inherit from this mixin to
    implement the observer pattern. The class inheriting this mixin
    must call super().__init__() to be propertly initialized.
    """

    def __init__(self):
        self.publisher = publisher()

    def sub(self, observer):
        """Subscribe an observer to receive notifications.
        Args:
            observer: An object that has implemented functions whose
            signatures match the @pub decorated functions it wishes
            to observe. After subscribing, the corresponding
            methods of the observer will be called each time the
            methods are called on the provider.
        """
        self.publisher.sub(observer)

    def unsub(self, observer):
        """Unsubscribe an observer from receiving notifications."""
        self.publisher.unsub(observer)


class publisher():
    """An instance is added to an inherited object.

    This class is added to the inherited class as the 'publisher'
    attribute. It implements the observer pattern.
    """
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
    """ Decorator wraps functions that should provide notifications
    to observers when executed.

    Returns: A wrapped version of the decorated function.
    """
    @functools.wraps(f)
    def pub_action_wrapper(*args, **kwargs):
        args[0].publisher.pub(f.__name__, *args, **kwargs)
        return f(*args, **kwargs)

    return pub_action_wrapper
