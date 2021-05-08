import shutil
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# import cv2
import os
import os.path as osp

import time
import logging

image_format = ['.jpg', '.JPG', '.png', '.PNG', '.JFIF', '.jpeg', '.JPEG', '.bmp']

background_none = "background-color:none"
background_yellow = "background-color:yellow"

logger = logging.getLogger("QT-classification")
stream_handler = logging.StreamHandler()
handlers = [stream_handler]
file_handler = logging.FileHandler("logger.log", 'w')
handlers.append(file_handler)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

for handler in handlers:
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

logger.setLevel(logging.INFO)


class mainWindow(QMainWindow):
    """
    Main window
    """

    def __init__(self):
        super(mainWindow, self).__init__()
        self.initUI()
        self.initInterParams()
        self.initFixedParams()

    def initInterParams(self):
        self._tmp_list = []
        self.ctrlPress = False

    def initFixedParams(self):
        self.display_image_size = 300
        self.file_path = '/'
        self.out_path = '/'

    def log_info(self, message):
        logger.info(message)

    def initUI(self):
        """
        Initialize the UI of main window.
        """
        # get the size of screen
        self.desktop = QApplication.desktop()
        self.height = self.desktop.height()
        self.width = self.desktop.width()

        # adjust the location of main window and set the title.
        self.resize(int(self.width * 0.9), int(self.height * 0.8))
        self.center()
        self.setWindowTitle("classification tool. v1.0 by Jessy Ye")

        # create the status bar and the text box
        self.status = self.statusBar()
        self.textbox = QLineEdit(self)

        # hide the edge of QLineEdit, set the location, font, and dis-editable
        self.textbox.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.textbox.move(50 + int(self.width * 0.8), 20)
        self.textbox.resize(int(self.width * 0.15), 200)
        self.textbox.setFocusPolicy(Qt.NoFocus)
        self.textbox.setFont(QFont("Arial", 15))
        self.textbox.setText("Classification tool")

        # create scroll area
        self.scroll_area_images = QScrollArea(self)
        self.scroll_area_images.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scroll_area_images.setWidget(self.scrollAreaWidgetContents)
        self.scroll_area_images.setGeometry(0, 50, int(self.width * 0.8), int(self.height * 0.9))
        self.vertocall = QVBoxLayout()

        # add buttons
        # directory selection button
        self.open_file_button = QPushButton(self)
        self.open_file_button.setGeometry(120 + int(self.width * 0.8), 150, 100, 30)
        self.open_file_button.setObjectName("open_pushbutton")
        self.open_file_button.setText("root directory")
        self.open_file_button.clicked.connect(self.open)

        # output path selection button
        self.output_pushbutton = QPushButton(self)
        self.output_pushbutton.setGeometry(250 + int(self.width * 0.8), 150, 100, 30)
        self.output_pushbutton.setObjectName("output_pushbutton")
        self.output_pushbutton.setText("output root")
        self.output_pushbutton.clicked.connect(self.setOutput)

        self.vertocall.addWidget(self.scroll_area_images)

        self.initClassesTextUI()

    def center(self):
        """
        set the main window Align center
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open(self):
        """
        Choose the root directory of images to be classified.
        """
        self.initInterParams()
        self.file_path = QFileDialog.getExistingDirectory(self, "Choose directory", self.file_path)
        self.setWindowTitle("classification tool. v1.0 by Jessy Ye    : " + self.file_path)
        self.clearLayout()  # initialize the scroll area
        time.sleep(0.01)
        self.startImgViewer()

    def setOutput(self):
        self.out_path = QFileDialog.getExistingDirectory(self, "Choose directory", self.out_path)

    def clearLayout(self):
        for i in range(self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater()

    def startImgViewer(self):
        """
        Load images to display on the scroll area
        """
        if self.file_path:
            photo_list = [osp.join(self.file_path, photo) for photo in os.listdir(self.file_path) if
                          osp.splitext(photo)[-1] in image_format]
            photo_list.sort()
            photo_num = len(photo_list)
            self.col = 0
            self.row = 0
            columns = self.getImageColumns()
            self.max_columns = columns
            if photo_num != 0:
                for i in range(photo_num):
                    image_id = photo_list[i]
                    pixmap = QPixmap(image_id)
                    self.addImage(pixmap, image_id)
                    QApplication.processEvents()  # Loading in real-time
            else:
                QMessageBox.information(self, "Note", "empty dir")
        else:
            QMessageBox.information(self, "Note", "Choose root directory")

    def getImageColumns(self):
        """
        Calculate the image numbers displayed on each row
        """
        scroll_area_images_width = self.scroll_area_images.width()
        if scroll_area_images_width > self.display_image_size:
            pic_of_columns = scroll_area_images_width // self.display_image_size
        else:
            pic_of_columns = 1
        return pic_of_columns - 2

    def addImage(self, pixmap, image_id):
        clickable_image = QClickableImage(self.display_image_size, self.display_image_size, pixmap, image_id)
        clickable_image.clicked.connect(self.leftClick)
        self.gridLayout.addWidget(clickable_image, self.row, self.col)

        # after add move to the next location
        if self.col < self.max_columns:
            self.col += 1
        else:
            self.col = 0
            self.row += 1

    def keyPressEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Control:
            self.ctrlPress = True

    def keyReleaseEvent(self, a0) -> None:
        if a0.key() == Qt.Key_Control:
            self.ctrlPress = False

    def leftClick(self):
        widget = self.sender()
        img_id = widget.image_id
        index = self.gridLayout.indexOf(widget)
        if self.ctrlPress:
            if (img_id, index) in self._tmp_list:
                self._tmp_list.remove((img_id, index))
                widget.setStyleSheet(background_none)
            else:
                self._tmp_list.append((img_id, index))
                widget.setStyleSheet(background_yellow)
        else:
            self.setBackgroundNone()
            self._tmp_list = [(img_id, index)]
            widget.setStyleSheet(background_yellow)

    def setBackgroundNone(self):
        for file, loc in self._tmp_list:
            self.gridLayout.itemAt(loc).widget().setStyleSheet(background_none)

    def initClassesTextUI(self):
        """
        Initialize the UI of classes line edit input, move and copy buttons.
        """

        buttonContents = QWidget(self)
        button_grid = QGridLayout()
        buttonContents.setLayout(button_grid)
        buttonContents.setGeometry(50 + int(self.width * 0.8), 200, 300, 800)
        class_cap = QLabel(self)
        class_cap.setText("classes names")
        class_cap.setFont(QFont("Arial", 14))
        class_cap.setGeometry(80 + int(self.width * 0.8), 180, 100, 30)

        for i in range(20):
            class_text = QLineEdit('')
            mv_button = QPushButton("move")
            mv_button.clicked.connect(self.moveExec)
            cp_button = QPushButton("copy")
            cp_button.clicked.connect(self.copyExec)

            button_grid.addWidget(class_text, i, 0)
            button_grid.addWidget(mv_button, i, 1)
            button_grid.addWidget(cp_button, i, 2)
        self.button_grid = button_grid

    def moveExec(self):
        """
        Move event. When click the move button, the bounded event are happened,
        the program will move the files have been chosen to the destination, and
        delete the image in the QT grid layout.
        """
        if self.out_path is not None:
            sender = self.sender()
            index = self.button_grid.indexOf(sender)  # locate the widget of sender
            row = index // 3
            text = self.button_grid.itemAtPosition(row, 0).widget().text()
            output_dir = osp.join(self.out_path, text)
            if not osp.exists(output_dir):
                os.makedirs(output_dir)
            for file, loc in self._tmp_list:
                dst = osp.join(output_dir, osp.basename(file))
                try:
                    shutil.move(file, dst)
                except Exception as e:
                    self.log_info(e)
                self.gridLayout.itemAt(loc).widget().deleteLater()
                self.log_info(f"move: {file} to {dst}")
        else:
            QMessageBox.information(self, "Note", "Please choose out root path")

    def copyExec(self):
        if self.out_path is not None:
            sender = self.sender()
            index = self.button_grid.indexOf(sender)  # locate the widget of sender
            row = index // 3
            text = self.button_grid.itemAtPosition(row, 0).widget().text()
            output_dir = osp.join(self.out_path, text)
            if not osp.exists(output_dir):
                os.makedirs(output_dir)
            for file, loc in self._tmp_list:
                dst = osp.join(output_dir, osp.basename(file))
                shutil.copy(file, dst)
                self.log_info(f"copy: {file} to {dst}")
        else:
            QMessageBox.information(self, "Note", "Please choose out root path")


class QClickableImage(QWidget):
    """
    Class for displayed image, a QLabel() on the top to show image, a QLabel() on the bottom to show image name.
    Using Qpixmap to adjust the image size.
    """
    image_id = ""
    clicked = pyqtSignal(object)

    def __init__(self, width=0, height=0, pixmap=None, image_id=""):
        QWidget.__init__(self)

        self.width = width
        self.height = height

        self.layout = QVBoxLayout(self)
        self.label2 = QLabel()
        self.label2.setObjectName("label2")

        if self.width and self.height:
            self.resize(self.width, self.height)
        if pixmap and image_id:
            pixmap = pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label1 = MyLabel(pixmap, image_id)
            self.label1.setObjectName("label1")
            self.layout.addWidget(self.label1)

        if image_id:
            self.image_id = image_id
            text = osp.basename(image_id)[:15]
            if len(image_id) > 15:
                text += "..."
            self.label2.setText(text)
            self.label2.resize(self.width, 30)
            self.label2.setWordWrap(True)
            self.label2.setAlignment(Qt.AlignCenter)

            self.label2.adjustSize()
            self.layout.addWidget(self.label2)
        self.setLayout(self.layout)

    def mousePressEvent(self, a0) -> None:
        if a0.buttons() == Qt.LeftButton:
            self.clicked.emit(self)


class MyLabel(QLabel):

    def __init__(self, pixmap=None, image_id=None):
        QLabel.__init__(self)
        self.pixmap = pixmap
        self.image_id = image_id
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # open right click

    def rightMenuShow(self, point):
        # add right click menu
        self.popMenu = QMenu()
        ch = QAction(u"redo", self)
        sc = QAction(u"delete", self)
        self.popMenu.addAction(ch)
        self.popMenu.addAction(sc)

        # binding event
        ch.triggered.connect(self.redo)
        sc.triggered.connect(self.delete)
        self.showContextMenu(QCursor.pos())

    def redo(self):
        pass

    def delete(self):
        pass

    def showContextMenu(self, pos):
        self.popMenu.move(pos)
        self.popMenu.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = mainWindow()
    main_window.show()
    sys.exit(app.exec_())
