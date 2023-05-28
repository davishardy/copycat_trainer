# Utility to find all the frames within a folder with the specific frames
import nuke

def validate_inputs(nodes, start_frame, end_frame):
    widths = []
    heights = []

    for node in nodes:
        for frame in range(start_frame, end_frame):
            width = nuke.toNode(node).metadata("input/width", frame)
            height = nuke.toNode(node).metadata("input/height", frame)

            try:
                type(width) and type(height) == "int"
            except ValueError:
                print("Height and Width of frames weren't found")
            else:
                widths.append(width)
                heights.append(height)

    widths = set(widths)
    heights = set(heights)

    if len(widths) and len(heights) == 1:
        return True
    else:
        return False


# a = validate_inputs(["Read1", "Read2"], 0, 5)
