# The main script that enables cli / gui and usage

# import nuke
import sys
import os
import platform

def main():
    # Check the OS and assign a path to the application

    cur_os = platform.system()
    machine_id = platform.node()
    

    if "nb-r" or "mt-r" in machine_id:
        if cur_os == "Darwin":
            pass #Mac
        elif cur_os == "Linux":
            pass #Linux
        else:
            pass # windows
    else:
        # Running on a non-monty computer
        pass
    
    # Assign inputs to copycat knobs

main()
