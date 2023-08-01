import typing
from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QWidget

class Menu_Bar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.file_menu = QMenu('File')
        self.edit_menu = QMenu('Edit')
        self.addMenu(self.file_menu)
        self.addMenu(self.edit_menu)
        self.add_actions_to_file_menu()
        self.add_actions_to_edit_menu()

    #add some stuff to the file menu
    def add_actions_to_file_menu(self):
        self.file_menu.addAction(QAction('New', self))
        self.file_menu.addAction(QAction('Open', self))
        self.file_menu.addAction(QAction('Save', self))
        self.file_menu.addAction(QAction('Save As', self))
        self.file_menu.addAction(QAction('Export', self))
        self.file_menu.addAction(QAction('Quit', self))

    #add some stuff to the edit menu
    def add_actions_to_edit_menu(self):
        self.edit_menu.addAction(QAction('Undo', self))
        self.edit_menu.addAction(QAction('Redo', self))
        self.edit_menu.addAction(QAction('Cut', self))
        self.edit_menu.addAction(QAction('Copy', self))
        self.edit_menu.addAction(QAction('Paste', self))
        self.edit_menu.addAction(QAction('Delete', self))
        self.edit_menu.addAction(QAction('Select All', self))



    
class Menu_Bar_Handler:
    def __init__(self):
        pass

