

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


    def contextMenuEvent(self, event):
        clicked_item = self.scene.itemAt(event.pos())


        if isinstance(clicked_item, Arrow):
            arrow_menu = QMenu(self.scene)

            delete_action = QAction('Delete', self.scene)
            delete_action.triggered.connect(self.arrow_manipulator.delete_arrow)
            arrow_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self.scene)
            rotate_right_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("right"))
            arrow_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self.scene)
            rotate_left_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("left"))
            arrow_menu.addAction(rotate_left_action)

            mirror_action = QAction('Mirror', self.scene)
            mirror_action.triggered.connect(lambda: self.arrow_manipulator.mirrorArrow())
            arrow_menu.addAction(mirror_action)

            bring_forward_action = QAction('Bring Forward', self.scene)
            bring_forward_action.triggered.connect(self.arrow_manipulator.bringForward)
            arrow_menu.addAction(bring_forward_action)

        elif isinstance(clicked_item, Staff):
            staff_menu = QMenu(self.scene)

            delete_action = QAction('Delete', self.scene)
            delete_action.triggered.connect(self.arrow_manipulator.delete_arrow)
            staff_menu.addAction(delete_action)

            rotate_right_action = QAction('Rotate Right', self.scene)
            rotate_right_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("right"))
            staff_menu.addAction(rotate_right_action)

            rotate_left_action = QAction('Rotate Left', self.scene)
            rotate_left_action.triggered.connect(lambda: self.arrow_manipulator.rotateArrow("left"))
            staff_menu.addAction(rotate_left_action)
        
        else: 
            graphboard_menu = QMenu(self.scene)

            swap_colors_action = QAction('Swap Colors', self.scene)
            swap_colors_action.triggered.connect(self.arrow_manipulator.swapColors)
            graphboard_menu.addAction(swap_colors_action)

            select_all_action = QAction('Select All', self.scene)
            select_all_action.triggered.connect(self.arrow_manipulator.selectAll)
            graphboard_menu.addAction(select_all_action)

            add_to_sequence_action = QAction('Add to Sequence', self.scene)
            add_to_sequence_action.triggered.connect(lambda _: self.sequence_manager.add_to_sequence(self.graphboard))
            graphboard_menu.addAction(add_to_sequence_action)

            export_as_png_action = QAction('Export to PNG', self.scene)
            export_as_png_action.triggered.connect(self.handlers.exporter.exportAsPng)
            graphboard_menu.addAction(export_as_png_action)

            export_as_svg_action = QAction('Export to SVG', self.scene)
            export_as_svg_action.triggered.connect(self.handlers.exporter.exportAsSvg)
            graphboard_menu.addAction(export_as_svg_action)

            graphboard_menu.exec_(event.globalPos())








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

