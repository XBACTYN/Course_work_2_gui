import time

import matplotlib.colors
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, \
    QSizePolicy, QDoubleSpinBox, QTableWidgetItem

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
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
import json


#Проверка. Это экспериментальная ветка.

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Testing Qt")
        self.setGeometry(50, 50, 1200, 900)  # Первые двве координаты смешение окна, последние две-размеры окна.
        self.widget = QWidget()

        ... #Первый V второй H
        #self.main_lay = QVBoxLayout(self)
        #self.down_lay = QHBoxLayout(self)

        self.main_lay = QHBoxLayout(self)
        self.down_lay = QVBoxLayout(self)
        self.up_lay = QVBoxLayout(self)
        ...

        self.contr_tab = ControlTab(self)
        ...
        #.main_lay.addWidget(self.contr_tab)
        self.up_lay.addWidget((self.contr_tab))

        ...
        self.bar = QtWidgets.QProgressBar(self)
        self.bar.setTextVisible(True)

        ...
        #.main_lay.addWidget(self.bar)
        ...
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(['Эксперименты'])
        #self.table.resizeColumnsToContents()


        self.experiments = []

        ####
        self.pic_tab = PictureTab(self)
        ####
        self.table.cellClicked.connect(self.WriteAndLoad)


        self.contr_tab.start_bn.clicked.connect(self.Start)
        self.contr_tab.way_bn.clicked.connect(self.pic_tab.DrawWay)
        self.contr_tab.way_bn.setEnabled(False)

        self.config = {
            'input_file': 'input.txt',
            'output_file': 'output.txt',
            'matrix_size': 0,
            'exp_count': 0,
            'gradient': 0,
            'concentration': 0.0,
            'fill_type': 0,
            'trace_file': 'traced_way.txt'
        }
        # self.pic_tab.arr=self.Download_matrix('output.txt')
        # self.pic_tab.update()

        self.GetSettings()

        ...
        #self.down_lay.addWidget(self.table)
        #self.down_lay.addWidget(self.pic_tab)
        self.up_lay.addWidget(self.table)
        self.down_lay.addWidget(self.bar)
        self.down_lay.addWidget(self.pic_tab)
        ...

        ...
        #добавлен up
        self.main_lay.addLayout(self.up_lay)
        #verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.main_lay.addItem(verticalSpacer)
        self.main_lay.addLayout(self.down_lay)
        ...

        self.widget.setLayout(self.main_lay)
        self.setCentralWidget(self.widget)

        self.show()

    def Download_matrix(self, filename):
        matrix = []
        with open(filename, 'r') as f:
            for line in f:
                row = []
                for l in line[:-1].split(' '):
                    row.append(int(l))
                matrix.append(row)
        # print(matrix)
        return matrix

    def GetSettings(self):
        self.config['matrix_size'] = self.contr_tab.tab1.layout1.itemAt(0, 1).widget().value()
        self.config['exp_count'] = self.contr_tab.tab1.layout1.itemAt(1, 1).widget().value()
        self.config['gradient'] = self.contr_tab.tab1.layout1.itemAt(2, 1).widget().value()
        self.config['concentration'] = self.contr_tab.tab1.layout1.itemAt(3, 1).widget().value()
        self.config['fill_type'] = self.contr_tab.tab1.fill_type.currentIndex()
        #print(self.config)

    def Start(self):
        self.contr_tab.way_bn.setEnabled(False)
        self.GetSettings()

        if self.config['fill_type']==7:
            self.config['matrix_size'] = 7
        if self.config['fill_type']==8:
            self.config['matrix_size'] = 9

        self.TableFilling()

        self.contr_tab.way_bn.setEnabled(True)

    def CalculateData(self):
        proc1 = QProcess(self)
        proc1.start('PO', ['input.txt', str(self.config['matrix_size']), str(self.config['concentration']),
                           str(self.config['fill_type'])])

        proc1.waitForFinished(-1)
        print('1')
        proc2 = QProcess(self)
        proc2.start('clasters', ['input.txt', 'output.txt', str(self.config['matrix_size'])])
        proc2.waitForFinished(-1)
        print('2')

    def Way(self):
        proc3 = QProcess(self)
        proc3.start('dijkstra', ['output.txt', str(self.config['trace_file']),str(self.config['matrix_size'])])
        proc3.waitForFinished(-1)
        print('3')

    def TableFilling(self):
        self.contr_tab.start_bn.setEnabled(False)
        count = self.config['exp_count']
        self.experiments.clear()
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['Эксперименты'])
        self.table.setRowCount(count)
        self.bar.reset()
        self.bar.setMaximum(count)
        #Запихать это в потоки.
        for i in range(1,count+1):
            print('i ',i)
            self.CalculateData()
            self.Way()
            self.experiments.append(Experiment(i,self.Download_matrix(self.config['output_file']),
                                               self.Download_matrix(self.config['trace_file'])))
            print('wrote')
            self.table.setItem(i-1,0,QTableWidgetItem(i))
            print('table')
            self.bar.setValue(i)
            print('bar')
        self.contr_tab.start_bn.setEnabled(True)

    def WriteAndLoad(self):
        num = self.table.currentRow()
        print('num ',num)
        self.pic_tab.arr=self.experiments[num].arr
        self.pic_tab.way_arr = self.experiments[num].way_arr
        self.pic_tab.update()


class ControlTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Настройки")
        self.tabs.addTab(self.tab2, 'Запуск')
        self.start_bn = None
        self.tab1.layout1 = QFormLayout(self)
        self.tab1.label = QtWidgets.QLabel()
        self.tab1.fill_type = QtWidgets.QComboBox()
        self.tab1UI()
        self.tab2UI()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1UI(self):
        self.tab1.tablay = QHBoxLayout(self)
        # self.tab1.layout1 = QFormLayout(self)
        self.tab1.layout1.addRow("Размер матрицы", QSpinBox())
        self.tab1.layout1.addRow("Количество экспериментов", QSpinBox())
        self.tab1.layout1.addRow("Градиентная вероятность", QSpinBox())
        self.tab1.layout1.addRow("Концентрация", QDoubleSpinBox())
        self.tab1.tablay.addLayout(self.tab1.layout1)
        # self.tab1.label = QtWidgets.QLabel()
        self.tab1.label.setText("Тип заполнения")
        # self.tab1.fill_type = QtWidgets.QComboBox()
        self.tab1.fill_type.addItem("Случайное")
        self.tab1.fill_type.addItem("Шахматное")
        self.tab1.fill_type.addItem("Дождь")
        self.tab1.fill_type.addItem("Кольца")
        self.tab1.fill_type.addItem("Зебра горизонт")
        self.tab1.fill_type.addItem("Зебра вертикаль")
        self.tab1.fill_type.addItem("Буква H")
        self.tab1.fill_type.addItem("Крест 7x7")
        self.tab1.fill_type.addItem("Крест 9x9")

        #self.tab1.secondlay = QVBoxLayout(self)
        #self.tab1.secondlay.addWidget(self.tab1.label)
        #self.tab1.secondlay.addWidget(self.tab1.fill_type)
        #self.tab1.secondlay.setAlignment(Qt.AlignLeft)
        #self.tab1.secondlay.addStretch()
        self.tab1.layout1.addWidget(self.tab1.label)
        self.tab1.layout1.addWidget(self.tab1.fill_type)
        self.tab1.layout1.setAlignment(Qt.AlignLeft)
        self.tab1.tablay.setAlignment(Qt.AlignTop)
        self.tab1.tablay.addStretch()

        self.tab1.layout1.itemAt(0, 1).widget().setMaximum(500)
        self.tab1.layout1.itemAt(1, 1).widget().setMaximum(500)
        self.tab1.layout1.itemAt(2, 1).widget().setMaximum(500)
        self.tab1.layout1.itemAt(3, 1).widget().setMaximum(1)
        self.tab1.layout1.itemAt(3, 1).widget().setSingleStep(0.1)
        self.tab1.layout1.itemAt(1, 1).widget().setMinimum(1)
        self.tab1.setMaximumSize(450, 200)

        #self.tab1.tablay.addLayout(self.tab1.secondlay)
        self.tab1.setLayout(self.tab1.tablay)

    def tab2UI(self):
        self.tab2.tablay = QHBoxLayout(self)
        self.start_bn = QtWidgets.QPushButton('Старт')
        self.way_bn = QtWidgets.QPushButton('Путь')
        self.tab2.tablay.addWidget(self.start_bn)
        self.tab2.tablay.addWidget(self.way_bn)
        self.tab2.tablay.setAlignment(Qt.AlignTop)
        self.tab2.tablay.addStretch()
        self.tab2.setLayout(self.tab2.tablay)

    # @pyqtSlot()
    # def on_click(self):
    # print("\n")
    # for currentQTableWidgetItem in self.tableWidget.selectedItems():
    # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class Experiment:
    def __init__(self,number,arr,way):
        self.num = number
        self.arr = arr
        self.way_arr = way

class PictureTab(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.arr = []
        self.way_arr=[]
        self.heatmap = None
        self.cmap = None
        self.palette = ["#FFFFFF", "#169D53", "#F2F62A", "#5E17EB", "#F99514", "#2E3192", "#8FCE00", "#E342B2",
                        "#FF00FF", "#B6932B",
                        "#FEFF70", "#C90076", "#52E810", "#FFF775", "#FFB0C5", "#8E8EAF", "#20FDF0", "#01DA31",
                        "#006FF1", "#FFC000",
                        "#2AC6F2", "#FFD923", "#F92C2C", "#2AC6F2", "#FF27B6", "#6417FF", "#ECA5FF", "#808080",
                        "#660066", "#A83F38",
                        "#018065", "#068BBF", "#37A647", "#F2B705", "#A60A33", "#6F2A8C", "#D2E537", "#533E56",
                        "#4F0014", "#F2CB07",
                        "#5CA904", "#730BDD", "#340A5E", "#C84451", "#4AB0D9", "#D7F7F8", "#3F399E", "#FFF32D",
                        "#00F7FF", "#F2BE22", "#BEF222"]


        self.fig = plt.figure(figsize=(8, 8))
        self.Mpl = FigureCanvasQTAgg(self.fig)

        self.layout = QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()
        self.heat_tab = QWidget()
        # self.stat_tab = QWidget()
        # self.diag_tab = QWidget()
        self.tabs.addTab(self.heat_tab, "Решетка")
        # self.tabs.addTab(self.stat_tab,'Статистика')
        # self.tabs.addTab(self.diag_tab,'Графики')
        self.tabs.resize(300, 300)
        self.heat_tabUI()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def heat_tabUI(self):
        self.heat_tab.layout = QVBoxLayout(self)
        # self.Mpl = FigureCanvasQTAgg(self.fig)
        self.heat_tab.layout.addWidget(self.Mpl)
        self.heat_tab.setLayout(self.heat_tab.layout)

    def update(self):

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                #
                if self.arr[i][j] % 50 == 0 and self.arr[i][j] != 0:
                    self.arr[i][j] = 23
                else:
                    self.arr[i][j] = self.arr[i][j] % 50
                    #

        #print('colored way',self.arr)
        self.cmap = matplotlib.colors.LinearSegmentedColormap.from_list('my_map', colors=self.palette)
        self.heatmap = sns.heatmap(self.arr, annot=False, cbar=False, cmap=self.cmap, vmin=0, linecolor='black', linewidths=0.01,
                                   xticklabels=[], yticklabels=[])



    def DrawWay(self):
        for i in range(len(self.way_arr)):
            for j in range(len(self.way_arr[i])):
                if self.way_arr[i][j] ==-1:
                    continue
                else:
                    if self.way_arr[i][j]%50==0 and self.way_arr[i][j]!=0:
                        self.way_arr[i][j]= 23
                    else:
                        self.way_arr[i][j] = self.way_arr[i][j] % 50

        #cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_map', colors=self.palette)
        self.cmap.set_under(color='#FF0000')
        self.heatmap = sns.heatmap(self.way_arr, annot=False, cbar=False, cmap=self.cmap, vmin=0, linecolor='black',
                                   linewidths=0.01,
                                   xticklabels=[], yticklabels=[])



def start_app():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()