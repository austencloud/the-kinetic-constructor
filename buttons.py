from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from handlers import Handlers

class Button_Manager:

    def initButtons(self, artboard, artboard_view, grid, infoTracker, sequence_manager):
            self.artboard = artboard
            self.artboard_view = artboard_view
            self.grid = grid
            self.infoTracker = infoTracker
            self.sequence_manager = sequence_manager
           
            self.handlers = Handlers(self.artboard, self.artboard_view, self.grid, self.artboard, self.infoTracker, self)
            self.artboard.set_handlers(self.handlers)
            masterbtnlayout = QVBoxLayout()
            buttonlayout = QHBoxLayout()
            buttonstack = QVBoxLayout()
            buttonstack.setAlignment(Qt.AlignTop)
            masterbtnlayout.setAlignment(Qt.AlignTop)
            buttonlayout.addLayout(buttonstack)
            masterbtnlayout.addLayout(buttonlayout)

            self.updatePositionButton = QPushButton("Update Position")
            self.updatePositionButton.clicked.connect(lambda: self.handlers.updatePositionInJson(*self.artboard.getCurrentArrowPositions()))
            buttonstack.addWidget(self.updatePositionButton)

            self.selectAllButton = QPushButton("Select All")
            self.selectAllButton.clicked.connect(self.handlers.selectAll)
            buttonstack.addWidget(self.selectAllButton)

            add_to_sequence_button = QPushButton("Add to Sequence")
            add_to_sequence_button.clicked.connect(lambda _: self.sequence_manager.add_to_sequence(self.artboard))
            buttonstack.addWidget(add_to_sequence_button)

            self.deleteButton = QPushButton("Delete")
            self.deleteButton.clicked.connect(self.handlers.deleteArrow)
            buttonstack.addWidget(self.deleteButton)

            self.rotateRightButton = QPushButton("Rotate Right")
            self.rotateRightButton.clicked.connect(lambda: self.handlers.rotateArrow("right"))
            buttonstack.addWidget(self.rotateRightButton)

            self.rotateLeftButton = QPushButton("Rotate Left")
            self.rotateLeftButton.clicked.connect(lambda: self.handlers.rotateArrow("left"))
            buttonstack.addWidget(self.rotateLeftButton)

            self.mirrorButton = QPushButton("Mirror")
            self.mirrorButton.clicked.connect(lambda: self.handlers.mirrorArrow())
            buttonstack.addWidget(self.mirrorButton)

            self.bringForward = QPushButton("Bring Forward")
            self.bringForward.clicked.connect(self.handlers.bringForward)
            buttonstack.addWidget(self.bringForward)

            self.swapColors = QPushButton("Swap Colors")
            self.swapColors.clicked.connect(self.handlers.swapColors)
            buttonstack.addWidget(self.swapColors)

            self.exportAsPNGButton = QPushButton("Export to PNG")
            self.exportAsPNGButton.clicked.connect(self.handlers.exportAsPng)
            buttonstack.addWidget(self.exportAsPNGButton)

            self.exportAsSVGButton = QPushButton("Export to SVG")
            self.exportAsSVGButton.clicked.connect(self.handlers.exportAsSvg)
            buttonstack.addWidget(self.exportAsSVGButton)

            button_font = QFont('Helvetica', 14)
            button_width = 200

            self.deleteButton.setFont(button_font)
            self.rotateRightButton.setFont(button_font)
            self.rotateLeftButton.setFont(button_font)
            self.mirrorButton.setFont(button_font)
            self.bringForward.setFont(button_font)
            self.swapColors.setFont(button_font)
            self.exportAsPNGButton.setFont(button_font)
            self.exportAsSVGButton.setFont(button_font)
            self.updatePositionButton.setFont(button_font)
            self.selectAllButton.setFont(button_font)
            add_to_sequence_button.setFont(button_font)

            self.deleteButton.setFixedWidth(button_width)
            self.rotateRightButton.setFixedWidth(button_width)
            self.rotateLeftButton.setFixedWidth(button_width)
            self.mirrorButton.setFixedWidth(button_width)
            self.bringForward.setFixedWidth(button_width)
            self.swapColors.setFixedWidth(button_width)
            self.exportAsPNGButton.setFixedWidth(button_width)
            self.exportAsSVGButton.setFixedWidth(button_width)
            self.updatePositionButton.setFixedWidth(button_width)
            self.selectAllButton.setFixedWidth(button_width)
            add_to_sequence_button.setFixedWidth(button_width)

            return masterbtnlayout