# Funtions to validate that sequence are the same size and shape
# Created by Davis Hardy
# Created on 2023-5-16
# Version 1.1.0

# Import modules
import nuke
import os
import glob
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
import cv2  # Has to be below the env variable so it loads with that the EXR capabilities


def file_elements(full_path):
    """
    Extracts file name elements from the full path of a file
    Inputs: Full file path
    Outputs: tuple of file name elements
    """
    try:
        os.path.exists(full_path)

    except ValueError:
        print("file doesn't exist")

    else:
        base_name = os.path.basename(full_path)
        base_name_elements = base_name.split(".")

        try:
            len(base_name_elements) == 3

        except ValueError:
            return None

        else:
            return (base_name_elements[0], base_name_elements[1], base_name_elements[2])


def validate_inputs(paths):
    """
    Validates if all the frames are the same size
    Inputs: Paths to start frames of both sequences
    Outputs: Boolean
    """

    widths = []
    heights = []

    frames_in_path = []

    for path in paths:
        path_dir = os.path.dirname()
        path_elements = file_elements(path)
        included_frames = glob.glob(os.path.join(path_dir, path_elements[0], "*"))

        frames_in_path.append(len(included_frames))

        for frame in included_frames:
            cur_frame = cv2.imread(frame, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)  # Allows for reading of EXR's
            dimensions = cur_frame.shape

            widths.append(dimensions[1])
            heights.append(dimensions[0])
    
    # Creates sets to get rid of duplicate outputs
    widths = set(widths)
    heights = set(heights)
    frame_quantity = set(frames_in_path)
    
    if len(widths) and len(heights) and len(frame_quantity) == 1:
        return True
    else:
        return False
