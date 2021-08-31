from PIL import Image
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QSpinBox, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = ''
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        # Spinboxes
        self.x_res_spin = QSpinBox()
        self.x_res_spin.setRange(0, 10000)
        self.y_res_spin = QSpinBox()
        self.y_res_spin.setRange(0, 10000)

        self.export_btn = QPushButton("Export and convert")
        self.export_btn.clicked.connect(self._clicked_export)
        self.res_label = QLabel()

        mainVlayout = QVBoxLayout()
        settingslayout = QHBoxLayout()
        label_layout = QVBoxLayout()
        spinbox_layout = QVBoxLayout()
        label_layout.addWidget(QLabel("X dpi:"))
        label_layout.addWidget(QLabel("Y dpi:"))
        spinbox_layout.addWidget(self.x_res_spin)
        spinbox_layout.addWidget(self.y_res_spin)
        settingslayout.addLayout(label_layout)
        settingslayout.addLayout(spinbox_layout)
        settingslayout.addWidget(self.export_btn)
        settingslayout.addStretch(1)
        mainVlayout.addWidget(self.imageLabel)
        mainVlayout.addLayout(settingslayout)
        central_widget = QWidget()
        central_widget.setLayout(mainVlayout)
        self.setCentralWidget(central_widget)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Resolution Editor")
        self.resize(400, 300)

    def open(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            self.filename = fileName
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            im = Image.open(fileName)
            width, height = im.size
            self.y_res_spin.setValue(width)
            self.x_res_spin.setValue(height)

    def _clicked_export(self):
        if self.filename != '':
            im = Image.open(self.filename)
            x = self.x_res_spin.value()
            y = self.y_res_spin.value()
            new_name = os.path.join("new", self.filename)
            new_name = os.path.basename(self.filename)
            im_resized = im.resize((x, y), Image.ANTIALIAS)
            im_resized.save(new_name, "PNG")
            # print(new_name)
            # im.save(new_name, dpi=(x, y))
        else:
            d = QDialog()
            # d.setText("No file selected!")
            b1 = QPushButton("ok", d)
            b1.move(50, 50)
            d.setWindowTitle("Dialog")
            d.setWindowModality(Qt.ApplicationModal)
            d.exec_()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.helpMenu)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = MainWindow()
    imageViewer.show()
    sys.exit(app.exec_())
