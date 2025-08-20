import functools

from slibs.printl import bg_text, RED, YELLOW, CYAN

def not_implemented(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(bg_text(f"Function '{func.__name__}' ⟹   NOT YET IMPLEMENTED", RED))
    
    return wrapper

# ======================================================================================= #

def to_reimplement():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(bg_text(f"Function '{func.__name__}' ⟹   TO REIMPLEMENT", YELLOW))
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def not_fully_implemented():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(bg_text(f"Function '{func.__name__}' ⟹   NOT FULLY IMPLEMENTED", CYAN))
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator