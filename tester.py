from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])

output_file, _ = QFileDialog.getSaveFileName(None, "Save SVG", "", "SVG files (*.svg)")
print(f"output_file: {output_file}")

app.exec_()
