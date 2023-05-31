# Function to create node graph, nuke file, and python file for training
# Created by Davis Hardy
# Created on 2023-5-16
# Version 1.3.0

# Import modules
import nuke
import os
from datetime import datetime

# Create nodes


def create_python(gt_file, input_file, gpu, data_directory, model_size, epochs, image_interval, model_size, crop_size, checkpoint_interval, nuke_file, python_file):
    py_command = []
    # Create read nodes
    py_command.append(f'gt_read = nuke.nodes.Read(name="Ground_Truth", file= {gt_file})')
    py_command.append(f'input_read = nuke.nodes.Read(name="Input", file= {input_file})')
    # Create CopyCat node
    py_command.append(f'cc_trainer = nuke.nodes.CopyCat(name="Train", inputs= [input_read, gt_read])')
    # Edit CopyCat node parameters
    py_command.append(f'cc_trainer["useGPUIfAvailable"].setValue({gpu})')
    py_command.append(f'cc_trainer["dataDirectory"].setValue({data_directory})')
    py_command.append(f'cc_trainer["modelSize"].setValue({model_size})')
    py_command.append(f'cc_trainer["epochs"].setValue({epochs})')
    py_command.append(f'cc_trainer["imageInterval"].setValue({image_interval})')
    # cc_trainer["isCachingEnabled"].setValue("false")  # Talking to Foundry about this
    py_command.append(f'cc_trainer["modelSize"].setValue({model_size})')
    py_command.append(f'cc_trainer["cropSize"].setValue({crop_size})')
    py_command.append(f'cc_trainer["batchSizeType"].setValue("Auto")')  # Leaving unimplemented due to isues
    # cc_trainer["batchSize"].setValue(1)  # Manual Batch Size, Issues with implementation
    py_command.append(f'cc_trainer["checkpointInterval"].setValue({checkpoint_interval})')
    # Save nuke file for training and further use
    nuke.scriptSaveAs(nuke_file)

    # Write python file with commands
    with open(python_file, 'w') as f:
        f.write(f"# File that creates node graph\n")
        f.write("# Created with CopyCat trainer\n")
        for line in py_command:
            f.write(f"{line}\n")
        f.write(f'Created on {datetime.now()}')
        f.write("End of file")
