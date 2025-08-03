from threading import local

_thread_locals = local()

def get_current_user():
    """
    Returns the user object for the current request.
    """
    return getattr(_thread_locals, 'user', None)

def set_current_user(user):
    """
    Sets the user object for the current request.
    """
    _thread_locals.user = user