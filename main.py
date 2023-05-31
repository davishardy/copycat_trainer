"""#!/usr/local/foundry/Nuke13.2v2/python"""

# GUI linking and main functions
# Created by Davis Hardy
# Created on 2023-5-16
# Version 1.0.0

# Import included modules
import sys
import os
import platform

# QT dependencies
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

import Utils.frame as frame_util
import Utils.node_graph as node_util


# Load Nuke module
cur_sys = platform.system()
if cur_sys == "Darwin":
    sys.path.append('/Applications/Nuke13.2v6/Nuke13.2v6.app/Contents/MacOS/plugins/nuke_internal')
elif cur_sys == "Linux":
    sys.path.append('/Applications/Nuke13.2v6/Nuke13.2v6.app/Contents/MacOS/plugins/nuke_internal')
elif cur_sys == "Windows":
    sys.path.append(r'C:\Program Files\Nuke13.2v2\Lib\site-packages')
else:
    print("Your system can't possibly have Nuke")


current_user = os.path.expanduser("~")


class MainWindow(QDialog):

    # Link buttons and load UI
    def __init__(self):
        super().__init__()
        loadUi("./Interface/trainer_v4.ui", self)

        self.gt_file_browse.clicked.connect(self.gt_browseimage)
        self.input_file_browse.clicked.connect(self.input_browseimage)
        self.data_dir_browse.clicked.connect(self.data_browsedir)
        self.script_path_browse.clicked.connect(self.script_browsedir)
        self.generate_button.clicked.connect(self.generate_nk_python)


    def gt_browseimage(self):
        # Taken from third assignment
        fname = QFileDialog.getOpenFileName(self, 'Open file', f'/home/{current_user}', 'Images (*.png, *.jpg, *.exr, *.tif)')
        self.gt_file_path.setText(fname[0])
        self.gt_filepath = "/Users/davishardy/SCAD/Sophomore/Spring/VSFX_313/Class_6/frames/frame.0001.exr" #fname[0]

    def input_browseimage(self):
        # Taken from third assignment
        fname = QFileDialog.getOpenFileName(self, 'Open file', f'/home/{current_user}', 'Images (*.png, *.jpg, *.exr, *.tif)')
        self.input_file_path.setText(fname[0])
        self.input_filepath = "/Users/davishardy/SCAD/Sophomore/Spring/VSFX_313/Class_6/frames/frame.0001.exr" #fname[0]

    def data_browsedir(self):
        # Taken from third assignment
        fname = QFileDialog.getOpenFileName(self, 'Open Directory', f'/home/{current_user}')
        self.data_dir_path.setText(fname[0])
        self.data_dir = "/Users/davishardy/SCAD/Sophomore/Spring/VSFX_313/Class_6/frames" #os.path.dirname(fname[0])

    def script_browsedir(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Directory', f'/home/{current_user}', 'Images (*.nk)')
        self.script_path.setText(fname[0])
        self.script_dir = "/Users/davishardy/SCAD/Sophomore/Spring/VSFX_313/Class_6/frames/test.nk" #os.path.dirname(fname[0])

    def generate_nk_python(self):
        if self.gpu_switch.isChecked() == True:
            self.gpu_on = "true"
        else:
            self.gpu_on = "false"


        self.epochs_value = int(self.epoch_value.text())
        self.contact_sheet_value = int(self.contact_sheet_quantity.text())
        self.checkpoint_value = int(self.checkpoint_quantity.text())
        self.model_size_modal = str(self.model_size.currentText())
        self.crop_size_modal = int(str(self.crop_size.currentText()))
        if frame_util.validate_inputs([self.gt_filepath, self.input_filepath]) == True:
            padding = frame_util.get_pad(self.gt_filepath)
            
            gt_elements = frame_util.file_elements(self.gt_filepath)
            gt_dir = os.path.dirname(self.gt_filepath)
            gt_with_pad = os.path.join(gt_dir, f"{gt_elements[0]}.{padding}.{gt_elements[2]}")

            input_elements = frame_util.file_elements(self.input_filepath)
            input_dir = os.path.dirname(self.input_filepath)
            input_with_pad = os.path.join(input_dir, f"{input_elements[0]}.{padding}.{input_elements[2]}")

            python_loc = node_util.python_loc(self.script_dir)

            node_util.create_python(gt_with_pad,
                                    input_with_pad,
                                    self.gpu_on,
                                    self.data_dir,
                                    self.model_size_modal,
                                    self.epochs_value,
                                    self.contact_sheet_value,
                                    self.crop_size_modal,
                                    self.checkpoint_value,
                                    self.script_dir,
                                    python_loc

            )
            nuke_command = f"{node_util.nuke_execute()} 'Train' {self.script_dir} {python_loc}"
            self.command_line_command.setText(nuke_command)



def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(win)
    widget.setFixedWidth(500)
    widget.setFixedHeight(496)
    widget.show()

    sys.exit(app.exec_())


main()
