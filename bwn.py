import sys
import time
import random
import serial
from PyQt5 import QtGui, QtWidgets, QtCore

width = 10
height = 10

framebuf = bytearray(12 * height)

ser = serial.Serial("/dev/ttyACM0", 9600)

class SerialThread(QtCore.QThread):
    def run(self):
        while True:
            line = ser.readline().decode("utf-8").rstrip()
            line_list = line.split()
            print(line_list)
            print(len(line_list))
            # if len(line_list) == 11:
            #   
            i = random.randint(0, height - 1)
            j = random.randint(0, width - 1)
            global framebuf
            newframe = framebuf
            newframe[i * 12 + j] = random.randint(0, 255)
            framebuf = newframe
            time.sleep(.001)
        

class BWNApp(QtWidgets.QWidget):
    
    def update_image(self):
        self.image = QtGui.QImage(framebuf, width, height, QtGui.QImage.Format_Grayscale8)
        self.pixmap = QtGui.QPixmap.fromImage(self.image).scaled(1600, 900)
        self.label.setPixmap(self.pixmap)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BWNACE")
        self.setGeometry(50, 50, 50, 50)
        self.label = QtWidgets.QLabel()
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.label, 1, 1)
        self.setLayout(self.layout)

        self.update_image()
        self.show()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1)

        self.thread = SerialThread()
        self.thread.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    inst = BWNApp()
    sys.exit(app.exec_())
