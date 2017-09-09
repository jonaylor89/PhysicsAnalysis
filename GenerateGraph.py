"""

Author: John Naylor

Description:
    A window is created allowing
    the user to enter the filename
    to a csv file containing physics
    linear acceleration data. With the
    data, a line graph is generated
    with x, y, z, and total acceleration.

"""
import sys
import os

import pandas as pd
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui


class Window(QtWidgets.QMainWindow):
    """ Class for the initial window for user to enter a filename """

    def __init__(self):
        super(Window, self).__init__()

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('Data Analysis')
        self.setWindowIcon(QtGui.QIcon('WindowIcon.png'))

        self.btn = QtWidgets.QPushButton("Generate Graph", self)
        self.btn.clicked.connect(self.button_handler)
        self.btn.setAutoDefault(True)
        self.btn.move(200, 150)

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(110, 100)
        self.textbox.resize(280, 40)

        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet('color: red')

        self.show()

    def button_handler(self):
        """ Checks to see if the filename is in the right directory """

        textboxValue = self.textbox.text()

        if os.path.isfile('%s.csv' % textboxValue):
            self.label.setText("")
            df = pd.read_csv(textboxValue + ".csv")
            generate_graph(df)

        else:
            self.label.setText("File must be a csv file in the PhysicsAnalysis directory")
            self.label.adjustSize()


def generate_graph(data):
    """ Plots x, y, z, and total acceleration versus time and shows graph """

    plt.plot(data['time'], data['ax'], 'r-',
             label="'x' Acceleration", alpha=0.7)
    plt.plot(data['time'], data['ay'], 'b-',
             label="'y' Acceleration", alpha=0.7)
    plt.plot(data['time'], data['az'], 'g-',
             label="'z' Acceleration", alpha=0.7)
    plt.plot(data['time'], data['aT'], 'k-',
             label="Total Acceleration", alpha=0.7)

    plt.title("Acceleration vs Time")
    plt.ylabel('Acceleration (m/s^2)')
    plt.xlabel('Time (s)')

    plt.legend(loc='upper left')

    plt.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()

    app.exec_()
