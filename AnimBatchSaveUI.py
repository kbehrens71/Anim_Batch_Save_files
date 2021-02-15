'''
Author - Kaitlyn Behrens
Date - 2/7/2021

This is the UI for AnimBatchSave, the tool that applies a batch of motion capture
animation to a given character.

Place this file in your Maya scripts folder (Documents/Maya/<Maya_Version>), and run
the following code:


import AnimBatchSaveUI

try:
    
    ui_obj.close()
    ui_obj.deleteLater()
    
except:
    
    pass
    
ui_obj = AnimBatchSaveUI.BatchSaveDialog()
ui_obj.show()

'''


# Import statements
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI

# Import the batch animation save script
import AnimBatchSave


# Get Maya window
def get_maya_window():
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)



# Create a class for the dialog box
class BatchSaveDialog(QtWidgets.QDialog):
    def __init__(self):

        # Get Maya window
        maya_main = get_maya_window()

        # Parent dialog to Maya window
        super(BatchSaveDialog, self).__init__(maya_main)

        # Set dialog box title, height, and width
        self.setWindowTitle("Save Animation Batch")
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        # Create widgets, layout, and connections
        self.create_widgets()
        self.create_layouts()
        self.create_connections()



    # Create widgets
    def create_widgets(self):

        # Form the label, input box, and file explorer button for character file
        self.char_text = QtWidgets.QLabel()
        self.char_text.setText("character:")
        self.char_input = QtWidgets.QLineEdit()
        self.char_file_btn = QtWidgets.QPushButton()
        self.char_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # Create header for directory section
        self.directory_text = QtWidgets.QLabel()
        self.directory_text.setAlignment(QtCore.Qt.AlignHCenter)
        self.directory_text.setText("Select Directories")

        # Form the label, input box, and file explorer button for animation directory
        self.anim_text = QtWidgets.QLabel()
        self.anim_text.setText("get anim from:")
        self.anim_input = QtWidgets.QLineEdit()
        self.anim_file_btn = QtWidgets.QPushButton()
        self.anim_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # Form the label, input box, and file explorer button for save directory
        self.save_text = QtWidgets.QLabel()
        self.save_text.setText("save files to:")
        self.save_input = QtWidgets.QLineEdit()
        self.save_file_btn = QtWidgets.QPushButton()
        self.save_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # Form the run and cancel buttons
        self.run_btn = QtWidgets.QPushButton("Run")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")



    # Create layouts
    def create_layouts(self):

        # Set the main layout as vertical
        main_layout = QtWidgets.QVBoxLayout(self)

        # Set all layouts within main layout as horizontal
        char_layout = QtWidgets.QHBoxLayout(self)
        anim_layout = QtWidgets.QHBoxLayout(self)
        save_layout = QtWidgets.QHBoxLayout(self)
        btn_layout = QtWidgets.QHBoxLayout(self)

        # Add the character label, input box, and file button to the character layout
        char_layout.addWidget(self.char_text)
        char_layout.addWidget(self.char_input)
        char_layout.addWidget(self.char_file_btn)

        # Add the animation label, input box, and file button to the animation layout
        anim_layout.addWidget(self.anim_text)
        anim_layout.addWidget(self.anim_input)
        anim_layout.addWidget(self.anim_file_btn)

        # Add the save label, input box, and file button to the save layout
        save_layout.addWidget(self.save_text)
        save_layout.addWidget(self.save_input)
        save_layout.addWidget(self.save_file_btn)

        # Add the run and cancel buttons to the button layout
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.cancel_btn)

        # Add all layouts to the main layout
        main_layout.addSpacing(20)
        main_layout.addLayout(char_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.directory_text)
        main_layout.addLayout(anim_layout)
        main_layout.addLayout(save_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)



    # Create connections between buttons and their actions
    def create_connections(self):

        # Connect file explorer buttons to their respective file browsing functions
        self.char_file_btn.clicked.connect(self.browse_char_file)
        self.anim_file_btn.clicked.connect(self.browse_anim_dir)
        self.save_file_btn.clicked.connect(self.browse_save_dir)

        # Connect the run button to the batch save function and the cancel button to the close function
        self.run_btn.clicked.connect(self.run_batch_function)
        self.cancel_btn.clicked.connect(self.close)



    # Browse files for the character file
    def browse_char_file(self):

        # Open file explorer and save selection
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", None, "Maya Files (*.ma *.mb")
        
        # If the selection isn't empty, set it as the text in the character input box
        if fileName[0]:
            self.char_input.setText(fileName[0])



    # Browse files for the animation directory
    def browse_anim_dir(self):

        # Open file explorer and save selection
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", None, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
       
        # If the selection isn't empty, set it as the text in the animation input box
        if dirName:
            self.anim_input.setText(dirName)



    # Browse files for the save directory
    def browse_save_dir(self):

        # Open file explorer and save selection
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", None, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        
        # If the selection isn't empty, set it as the text in the save input box
        if dirName:
            self.save_input.setText(dirName)



    # Run the batch save function from imported file
    def run_batch_function(self):
        print "running batch function"
        AnimBatchSave.connect_rig_to_anims(self.char_input.text(), self.anim_input.text(), self.save_input.text())
 
