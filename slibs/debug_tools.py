import functools

from slibs.printl import *

def not_implemented(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(bg_text(f"Function '{func.__name__}' ⟹   NOT YET IMPLEMENTED", RED))
    
    return wrapper

def not_fully_implemented():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(bg_text(f"Function '{func.__name__}' ⟹   NOT FULLY IMPLEMENTED", CYAN))
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator