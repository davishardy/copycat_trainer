# Utility to find all the frames within a folder with the specific frames
import nuke

cur_node = nuke.toNode("Read1")

widths = []
heights = []

for frame in range(1,20):
    a = cur_node.metadata("input/width", frame)
    b = cur_node.metadata("input/height", frame)


c = nuke.filename(cur_node)

