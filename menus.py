

from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from arrow import Arrow
from staff import Staff


class Context_Menu_Handler:
    def __init__(self, scene, handlers, sequence_manager, arrow_manipulator, exporter):
        self.scene = scene
        self.handlers = handlers
        self.sequence_manager = sequence_manager
        self.arrow_manipulator = arrow_manipulator
        self.exporter = exporter


    def create_context_menu(self, event, selected_items):
        menu = QMenu()
        if len(selected_items) == 2:
            menu.addAction("Align horizontally", self.align_horizontally)
            menu.addAction("Align vertically", self.align_vertically)
        menu.addAction("Move", self.show_move_dialog)
        menu.addAction("Delete", self.handlers.delete_arrow)
        menu.exec_(event.screenPos())

    def show_move_dialog(self):
        dialog = QDialog()
        layout = QFormLayout()

        # Create the input fields
        self.up_input = QSpinBox()
        self.down_input = QSpinBox()
        self.left_input = QSpinBox()
        self.right_input = QSpinBox()

        # Add the input fields to the dialog
        layout.addRow("Up:", self.up_input)
        layout.addRow("Down:", self.down_input)
        layout.addRow("Left:", self.left_input)
        layout.addRow("Right:", self.right_input)

        # Create the buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the buttons to their slots
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # Add the buttons to the dialog
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # Show the dialog and wait for the user to click a button
        result = dialog.exec_()

        # If the user clicked the OK button, move the arrows
        if result == QDialog.Accepted:
            self.move_arrows()

    def move_arrows(self):
        items = self.scene().selectedItems()
        for item in items:
            item.moveBy(self.right_input.value() - self.left_input.value(), self.down_input.value() - self.up_input.value())

    def align_horizontally(self):
        items = self.scene().selectedItems()
        average_y = sum(item.y() for item in items) / len(items)
        for item in items:
            item.setY(average_y)

    def align_vertically(self):
        items = self.scene().selectedItems()
        average_x = sum(item.x() for item in items) / len(items)
        for item in items:
            item.setX(average_x)


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

