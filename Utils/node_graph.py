import nuke
import os

gt_file = "/Users/davishardy/Downloads/sys_rf_arnold/output.0001-5.exr"
input_file = "/Users/davishardy/Downloads/sys_rf_arnold/output.0001-5.exr"

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
cc_trainer["epochs"].setValue(100)
cc_trainer["imageInterval"].setValue(200)
cc_trainer["isCachingEnabled"].setValue("false")
