from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI
import AnimBatchSave
import pymel.core


def get_maya_window():
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)
    
class SaveAnimDialog(QtWidgets.QDialog):
    
    def __init__(self):
        maya_main = get_maya_window()
        
        super(SaveAnimDialog, self).__init__(maya_main)
        
        self.setWindowTitle("Save Animation Batch")
        
        self.setMinimumWidth(400)
        self.setMinimumHeight(100)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        
    def create_widgets(self):
        self.char_text = QtWidgets.QLabel()
        self.char_text.setText("character:")
        self.char_path = QtWidgets.QLineEdit()
        self.char_file_btn = QtWidgets.QPushButton()
        self.char_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.directory_text = QtWidgets.QLabel()
        self.directory_text.setAlignment(QtCore.Qt.AlignHCenter)
        self.directory_text.setText("Select Directories")
        
        self.anim_text = QtWidgets.QLabel()
        self.anim_text.setText("get anim from:")
        self.anim_dir = QtWidgets.QLineEdit()
        self.anim_file_btn = QtWidgets.QPushButton()
        self.anim_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.save_text = QtWidgets.QLabel()
        self.save_text.setText("save files to:")
        self.save_dir = QtWidgets.QLineEdit()
        self.save_file_btn = QtWidgets.QPushButton()
        self.save_file_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        
        self.run_btn = QtWidgets.QPushButton("Run")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
        
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        char_layout = QtWidgets.QHBoxLayout(self) 
        anim_layout = QtWidgets.QHBoxLayout(self) 
        save_layout = QtWidgets.QHBoxLayout(self) 
        btn_layout = QtWidgets.QHBoxLayout(self)
        
        char_layout.addWidget(self.char_text)
        char_layout.addWidget(self.char_path)
        char_layout.addWidget(self.char_file_btn)
        
        anim_layout.addWidget(self.anim_text)
        anim_layout.addWidget(self.anim_dir)
        anim_layout.addWidget(self.anim_file_btn)

        save_layout.addWidget(self.save_text)
        save_layout.addWidget(self.save_dir)
        save_layout.addWidget(self.save_file_btn)
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addSpacing(20)
        main_layout.addLayout(char_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.directory_text)
        main_layout.addLayout(anim_layout)
        main_layout.addLayout(save_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)
        
    
    def create_connections(self):
        self.char_file_btn.clicked.connect(self.browse_char_file)
        self.anim_file_btn.clicked.connect(self.browse_anim_dir)
        self.save_file_btn.clicked.connect(self.browse_save_dir)
        self.run_btn.clicked.connect(self.run_batch_function)
        self.cancel_btn.clicked.connect(self.close)

        
    def browse_char_file(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", None, "Maya Files (*.ma *.mb")
        if fileName[0]:
            self.char_path.setText(fileName[0])
    
    def browse_anim_dir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", None,
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                       | QtWidgets.QFileDialog.DontResolveSymlinks)
        if dir:
            self.anim_dir.setText(dir)

    def browse_save_dir(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", None,
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                       | QtWidgets.QFileDialog.DontResolveSymlinks)
        if dir:
            self.save_dir.setText(dir)


    def run_batch_function(self):
        print "running batch function"
        AnimBatchSave.run_batch(self.char_path.text(), self.anim_dir.text(), self.save_dir.text())
 

try:
    ui_obj.close()
    ui_obj.deleteLater()
    
except:
    pass
    
ui_obj = SaveAnimDialog()
ui_obj.show()
