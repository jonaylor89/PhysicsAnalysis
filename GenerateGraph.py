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

from scipy.integrate import cumtrapz
import pandas as pd
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui


class Window(QtWidgets.QMainWindow):
    """ Class for the initial window for user to enter a filename """

    def __init__(self):
        super(Window, self).__init__()

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('Data Analysis')
        self.setWindowIcon(QtGui.QIcon('Images\WindowIcon.png'))

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
    """ Plots trajectory of roller coaster"""

    mpl.rcParams['legend.fontsize'] = 10

    fig1 = plt.figure(1)
    ax = fig1.gca(projection='3d')

    vx = cumtrapz(data['ax'].as_matrix(), data['time'].as_matrix(), initial=0)
    vy = cumtrapz(data['ay'].as_matrix(), data['time'].as_matrix(), initial=0)
    vz = cumtrapz(data['az'].as_matrix(), data['time'].as_matrix(), initial=0)
    vT = cumtrapz(data['aT'].as_matrix(), data['time'].as_matrix(), initial=0)

    px = cumtrapz(vx, data['time'].as_matrix(), initial=0)
    py = cumtrapz(vy, data['time'].as_matrix(), initial=0)
    pz = cumtrapz(vz, data['time'].as_matrix(), initial=0)
    pT = cumtrapz(vT, data['time'].as_matrix(), initial=0)

    # ax.plot(data['ax'], data['ay'], data['az'],
    #     label='Roller Coaster Curve')
    ax.plot(px, py, pz,
        label='Roller Coaster Curve')

    ax.legend()

    """ Plots x, y, z, and total acceleration versus time and shows graph """

    plt.figure(2)

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

    plt.figure(3)
    plt.clf()
    plt.plot(data['time'], vx, 'r-',
          label="'x' Velocity", alpha=0.7)
    plt.plot(data['time'], vy, 'b-',
          label="'y' Velocity", alpha=0.7)
    plt.plot(data['time'], vz, 'g-',
          label="'z' Velocity", alpha=0.7)
    plt.plot(data['time'], data['aT'], 'k-',
          label="Total Velocity", alpha=0.7)

    plt.title("Velocity vs Time")
    plt.ylabel('Velocity (m/s)')
    plt.xlabel('Time (s)')
    plt.legend(loc='upper left')

    plt.figure(4)
    plt.clf()
    plt.plot(data['time'], px, 'r-',
        label="'x' Position", alpha=0.7)
    plt.plot(data['time'], py, 'b-',
        label="'y' Position", alpha=0.7)
    plt.plot(data['time'], pz, 'g-',
        label="'z' Position", alpha=0.7)
    plt.plot(data['time'], pT, 'k-',
        label="Total Position", alpha=0.7)

    plt.title("Position vs Time")
    plt.ylabel('Position (m)')
    plt.xlabel('Time (s)')
    plt.legend(loc='upper left')

    plt.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()

    app.exec_()
