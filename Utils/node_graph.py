import nuke
import os

gt_file = "/Users/davishardy/Downloads/sys_rf_arnold/output.0001-5.exr"
input_file = "/Users/davishardy/Downloads/sys_rf_arnold/output.0001-5.exr"
data_directory = "/Users/davishardy/SCAD/Sophomore/Spring/VSFX_270/P6/temp_train/"

# check if file path exists
# get padding
# get begining and end
# check if both sequences begining and ends are the same
# check is sequence is complete
# Create nodes and link them together

# Create nodes
gt_read = nuke.nodes.Read(name="Ground_Truth", file= gt_file)
input_read = nuke.nodes.Read(name="Input", file= input_file)
cc_trainer = nuke.nodes.CopyCat(name="Train", inputs= [input_read, gt_read])
cc_trainer["useGPUIfAvailable"].setValue("true")
cc_trainer["dataDirectory"].setValue(data_directory)   # Attach parm
cc_trainer["modelSize"].setValue("Small") # Attach parm
cc_trainer["epochs"].setValue(100)  # Attach parm

cc_trainer["imageInterval"].setValue(100)
# cc_trainer["isCachingEnabled"].setValue("false")  # Talking to Foundry about this
cc_trainer["modelSize"].setValue("Medium")
cc_trainer["cropSize"].setValue(256)

cc_trainer["batchSizeType"].setValue("Auto")
# cc_trainer["batchSize"].setValue(1)  # Manual Batch Size

cc_trainer["checkpointInterval"].setValue(1000)

# nuke.execute(cc_trainer, 1, 1)
# nuke.scriptSaveAs
