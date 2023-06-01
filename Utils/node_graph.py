# Function to create node graph, nuke file, and python file for training
# Created by Davis Hardy
# Created on 2023-5-16
# Version 1.3.0

# Import modules
# import nuke
import os
from datetime import datetime
import platform
import sys

# Load Nuke module
cur_sys = platform.system()
if cur_sys == "Darwin":
    sys.path.append('/Applications/Nuke13.2v6/Nuke13.2v6.app/Contents/MacOS/plugins/nuke_internal')
elif cur_sys == "Linux":
    sys.path.append('/Applications/Nuke13.2v6/Nuke13.2v6.app/Contents/MacOS/plugins/nuke_internal')
elif cur_sys == "Windows":
    sys.path.append(r'C:\Program Files\Nuke13.2v2\Lib\site-packages')
else:
    pass


# Create nodes
def create_python(gt_file, input_file, gpu, data_directory, model_size, epochs, image_interval, crop_size, checkpoint_interval, nuke_file, python_file):
    py_command = []
    # Create read nodes
    py_command.append(f'gt_read = nuke.nodes.Read(name="Ground_Truth", file= "{gt_file}")')
    py_command.append(f'input_read = nuke.nodes.Read(name="Input", file= "{input_file}")')
    # Create CopyCat node
    py_command.append(f'cc_trainer = nuke.nodes.CopyCat(name="Train", inputs= [input_read, gt_read])')
    # Edit CopyCat node parameters
    py_command.append(f'cc_trainer["useGPUIfAvailable"].setValue("{gpu}")')
    py_command.append(f'cc_trainer["dataDirectory"].setValue("{data_directory}")')
    py_command.append(f'cc_trainer["modelSize"].setValue({model_size})')
    py_command.append(f'cc_trainer["epochs"].setValue({epochs})')
    py_command.append(f'cc_trainer["imageInterval"].setValue({image_interval})')
    # cc_trainer["isCachingEnabled"].setValue("false")  # Talking to Foundry about this
    py_command.append(f'cc_trainer["modelSize"].setValue("{model_size}")')
    py_command.append(f'cc_trainer["cropSize"].setValue({crop_size})')
    py_command.append(f'cc_trainer["batchSizeType"].setValue("Auto")')  # Leaving unimplemented due to isues
    # cc_trainer["batchSize"].setValue(1)  # Manual Batch Size, Issues with implementation
    py_command.append(f'cc_trainer["checkpointInterval"].setValue({checkpoint_interval})')
    # Save nuke file for training and further use
    # nuke.scriptSaveAs(nuke_file)

    # Write python file with commands
    with open(python_file, 'w') as f:
        f.write(f"# File that creates node graph\n")
        f.write("# Created with CopyCat trainer\n")
        for line in py_command:
            f.write(f"{line}\n")
        f.write(f'Created on {datetime.now()}\n')
        f.write("End of file\n")


def python_loc(nuke_script_dir):
    nk_file_loc = os.path.dirname(nuke_script_dir)
    python_file_loc = os.path.join(nk_file_loc, "train.py")
    return python_file_loc

def nuke_execute():
    """
    Generates OS specific command
    Inputs: None
    Outputs:
    """
    if cur_sys == "Linux":
        nuke_execute_arg = "/usr/local/foundry/Nuke13.2v2/Nuke13.2 --nukex -i -t -gpu 0 -F 1-1 -X"

    if cur_sys == "Windows":
        nuke_execute_arg = r"C:\Program Files\Nuke13.2v2\Nuke13.2.exe --nukex -i -t -gpu 0 -F 1-1 -X"

    if cur_sys == "Darwin":
        nuke_execute_arg = "open -a /Applications/Nuke13.2v6/NukeX13.2v6.app --args --nukex -i -t -gpu 0 -F 1-1 -X"

    return nuke_execute_arg