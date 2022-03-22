from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, \
    QSizePolicy

from random import uniform
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

import sys
import random
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure


class Window (QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Testing Qt")
        self.setGeometry(400, 100, 800, 800) #Первые двве координаты смешение окна, последние две-размеры окна.

        self.widget = QWidget()
        self.main_lay = QVBoxLayout(self)
        self.down_lay = QHBoxLayout(self)

        self.contr_tab = ControlTab(self)
        #elf.setCentralWidget(self.contr_tab)
        self.main_lay.addWidget(self.contr_tab)
        self.bar = QtWidgets.QProgressBar(self)
        self.main_lay.addWidget(self.bar)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(['Эксперименты'])
        self.table.resizeColumnsToContents()
        self.pic_tab = PictureTab(self)
        self.down_lay.addWidget(self.table)
        self.down_lay.addWidget(self.pic_tab)

        self.main_lay.addLayout(self.down_lay)

        self.widget.setLayout(self.main_lay)
        self.setCentralWidget(self.widget)
        #m=self.mytab.randMatrix(5)
        #self.mytab.DrawMatrix(m)

        self.show()


class ControlTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1,"Настройки")
        self.tabs.addTab(self.tab2,'Детальный эксперимент')
        #self.tabs.resize(300, 300)
        self.tab1UI()
        self.tab2UI()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1UI(self):
        self.tab1.tablay = QHBoxLayout(self)
        self.tab1.layout1 = QFormLayout(self)
        self.tab1.layout1.addRow("Размер матрицы",QSpinBox())
        self.tab1.layout1.addRow("Количество экспериментов",QSpinBox())
        self.tab1.layout1.addRow("Градиентная вероятность", QSpinBox())
        self.tab1.layout1.addRow("Концентрация", QSpinBox())
        self.tab1.tablay.addLayout(self.tab1.layout1)
        self.tab1.label = QtWidgets.QLabel()
        self.tab1.label.setText("Тип заполнения")
        self.tab1.fill_type = QtWidgets.QComboBox()
        self.tab1.fill_type.addItem("Случайное")
        self.tab1.fill_type.addItem("Шахматное")
        self.tab1.fill_type.addItem("Дождь")
        self.tab1.fill_type.addItem("Кольца")
        self.tab1.secondlay = QVBoxLayout(self)
        self.tab1.secondlay.addWidget(self.tab1.label)
        self.tab1.secondlay.addWidget(self.tab1.fill_type)
        self.tab1.secondlay.setAlignment(Qt.AlignLeft)
        self.tab1.secondlay.addStretch()
        self.tab1.tablay.setAlignment(Qt.AlignTop)

        self.tab1.setMaximumSize(450,200)

        self.tab1.tablay.addLayout(self.tab1.secondlay)
        self.tab1.setLayout(self.tab1.tablay)

    def tab2UI(self):
        self.tab2.tablay = QHBoxLayout(self)
        self.start_bn = QtWidgets.QPushButton('Старт')
        self.tab2.tablay.addWidget(self.start_bn)
        self.tab2.tablay.setAlignment(Qt.AlignTop)
        self.tab2.tablay.addStretch()
        self.tab2.setLayout(self.tab2.tablay)

    #@pyqtSlot()
    #def on_click(self):
       #print("\n")
        #for currentQTableWidgetItem in self.tableWidget.selectedItems():
           # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.clb = []
        self.plot = []

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        self.layout().addWidget(self.canvas.toolbar)
        self.layout().addWidget(self.canvas)
        X = np.random.randn(10, 8)
        self.plot = sns.heatmap(X, cmap='PuBu', square=True, linewidth=0.1, linecolor=(0.1, 0.2, 0.2),
                                ax=self.axes, vmin=np.min(X), vmax=np.max(X))

class PictureTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.arr=[[]]
        self.fig =plt.figure(figsize=(6, 6))
        self.layout = QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()
        self.heat_tab = QWidget()
        self.stat_tab = QWidget()
        self.diag_tab = QWidget()
        self.tabs.addTab(self.heat_tab, "Решетка")
        self.tabs.addTab(self.stat_tab,'Статистика')
        self.tabs.addTab(self.diag_tab,'Графики')
        self.tabs.resize(300, 300)
        self.heat_tabUI()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def heat_tabUI(self):
        self.heat_tab.layout = QVBoxLayout(self)
        self.arr = self.randMatrix(50)  #
        #fig = plt.figure(figsize=(6, 6))
        heatmap = sns.heatmap(self.arr, annot=False, cbar=False, vmin=None, vmax=None, cmap='rainbow')
        heatmap.set(xticklabels=[])
        heatmap.set(yticklabels=[])
        heatmap.tick_params(bottom=False)
        heatmap.tick_params(left=False)
        self.Mpl = FigureCanvasQTAgg(self.fig)
        self.heat_tab.layout.addWidget(self.Mpl)
        self.heat_tab.setLayout(self.heat_tab.layout)

    def update(self):
        x = self.randMatrix(50)
        heatmap = sns.heatmap(x, annot=False, cbar=False, vmin=None, vmax=None, cmap='rainbow')

    def randMatrix(self, n):
        matrix = [[uniform(0, 1.0) for j in range(n)] for i in range(n)]
        print(matrix)
        return matrix

def start_app():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
