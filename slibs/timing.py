"""
██      ██ ██████  ██████   █████  ██████  ██ ███████ ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██      ██      
██      ██ ██████  ██████  ███████ ██████  ██ █████   ███████ 
██      ██ ██   ██ ██   ██ ██   ██ ██   ██ ██ ██           ██ 
███████ ██ ██████  ██   ██ ██   ██ ██   ██ ██ ███████ ███████ 
"""

from datetime import datetime
import time

def compute_timestamp(is_date=False, ms_decimal_digits=3) -> str:
    now = datetime.now()
    
    time_str = now.strftime("%H:%M:%S")
    
    microseconds = now.microsecond
    milliseconds = microseconds / 1000
    ms_str = f"{milliseconds:.{ms_decimal_digits}f}".zfill(ms_decimal_digits + 2)
    
    time_str = f"{time_str}:{ms_str}"
    
    if is_date:
        date_str = now.strftime("%d/%m/%y")
        return f"{date_str} {time_str}"
    else:
        return time_str
    
def compute_date() -> str:
    now = datetime.now()

    return str(now.strftime("%Y-%m-%d"))

def wait_ms(ms) -> None:
    time.sleep(ms/1000)

    return


