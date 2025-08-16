import sys
import platform

from slibs.printl import fg_text, RED

match platform.system():
    case "Linux":
        from slibs.linux_exec   import * 
    case "Darwin":   
        from slibs.macos_exec   import *
    case "Windows":
        from slibs.windows_exec import *
    case _:          
        print(fg_text(f"OS NOT recognized ⟹ aborting SW execution"), RED)
        sys.exit(1) # @NOTE: fail return