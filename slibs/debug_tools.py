import functools
import warnings

from slibs.printl import *

def not_implemented(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(bg_text(f"Function '{func.__name__}' → NOT YET IMPLEMENTED", RED))
    
    return wrapper