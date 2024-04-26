from PyQt6.QtWidgets import QFileDialog, QCheckBox


class CustomSaveDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(CustomSaveDialog, self).__init__(*args, **kwargs)
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)

        self.openCheckBox = QCheckBox("Open file after saving")
        self.openCheckBox.setChecked(True)

        layout = self.layout()
        layout.addWidget(self.openCheckBox, 4, 0, 1, -1)

    def getOpenAfterSave(self):
        return self.openCheckBox.isChecked()
