import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import cv2
import os
import os.path as osp

root = "/Users/fiberhome/Downloads/paint_data/image"
out = "/Users/fiberhome/Downloads/paint_data/label_debug"

file_list = os.listdir(root)
file_list = [osp.join(root, file) for file in file_list]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lb1 = QLabel('Zetcode', self)
        lb1.move(15, 10)

        lb2 = QLabel('tutorials', self)
        lb2.move(35, 40)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Absolute")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Example()
    # window.setWindowTitle('Hello World!')
    # window.show()

    sys.exit(app.exec_())
