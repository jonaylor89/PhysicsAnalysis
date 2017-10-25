import sys
import random
from scipy.integrate import cumtrapz
import pandas as pd
import matplotlib
import os
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QFileDialog, QGridLayout, QSizePolicy, QMessageBox, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class TwoCanvas(MyMplCanvas):
    def update_graph(self, data):
        self.axes.plot(data['time'], data['ax'], 'r-',
                 label="'x' Acceleration", alpha=0.7)
        self.axes.plot(data['time'], data['ay'], 'b-',
                 label="'y' Acceleration", alpha=0.7)
        self.axes.plot(data['time'], data['az'], 'g-',
                 label="'z' Acceleration", alpha=0.7)
        self.axes.plot(data['time'], data['aT'], 'k-',
                 label="Total Acceleration", alpha=0.7)

        # self.axes.title("Acceleration vs Time")
        # self.axes.ylabel('Acceleration (m/s^2)')
        # self.axes.xlabel('Time (s)')
        # self.axes.legend(loc='upper left')

        self.draw()


class ThreeCanvas(MyMplCanvas):
    def update_graph(self, data):
        vx = cumtrapz(data['ax'].as_matrix(), data['time'].as_matrix(), initial=0)
        vy = cumtrapz(data['ay'].as_matrix(), data['time'].as_matrix(), initial=0)
        vz = cumtrapz(data['az'].as_matrix(), data['time'].as_matrix(), initial=0)

        self.axes.clf()
        self.axes.plot(data['time'], vx, 'r-',
                 label="'x' Velocity", alpha=0.7)
        self.axes.plot(data['time'], vy, 'b-',
                 label="'y' Velocity", alpha=0.7)
        self.axes.plot(data['time'], vz, 'g-',
                 label="'z' Velocity", alpha=0.7)
        self.axes.plot(data['time'], data['aT'], 'k-',
                 label="Total Velocity", alpha=0.7)

        # self.axes.title("Acceleration vs Time")
        # self.axes.ylabel('Acceleration (m/s^2)')
        # self.axes.xlabel('Time (s)')
        # self.axes.legend(loc='upper left')

        self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 1200, 600)
        self.setWindowTitle('Data Analysis')
        self.setWindowIcon(
            QtGui.QIcon(
                os.path.join(LOCAL_PATH, 'Images/WindowIcon.png')
            )
        )

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Open', self.open_file_name_dialog,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Quit', self.fileQuit,
                QtCore.Qt.CTRL + QtCore.Qt.Key_Q)

        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QGridLayout(self.main_widget)
        self.one = MyMplCanvas(self.main_widget, width=4, height=4, dpi=100)
        self.two = TwoCanvas(self.main_widget, width=4, height=4, dpi=100)
        self.three = ThreeCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.four = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(self.one, 0, 0)
        l.addWidget(self.two, 0, 1)
        l.addWidget(self.three, 1, 0)
        l.addWidget(self.four, 1, 1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.show()

        # self.statusBar().showMessage("All hail matplotlib!", 2000)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

        if fileName.endswith(".csv"):
            self.dataframe = pd.read_csv(fileName)
            self.two.update_graph(self.dataframe)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
"""
EmbedingMPL.py example
Copyright 2015 BoxControL

This program is a simple example of a Qt5 application embedding matplotlib
canvases. It is base on example from matplolib documentation, and initially was
developed from Florent Rougon and Darren Dale.

http://matplotlib.org/examples/user_interfaces/embedding_in_qt4.html

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation.
"""
                          )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("PyQt5 Matplot Example")
    aw.show()
    app.exec_()
