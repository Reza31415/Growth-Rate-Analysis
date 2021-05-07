# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 22:06:30 2021

@author: Reza-G510
"""

import sys 
from PyQt5 import QtWidgets, QtCore
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas as pd
import string
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
from matplotlib.widgets import SpanSelector
from scipy.optimize import curve_fit

matplotlib.use('Qt5Agg')

import Data

class Fit_Panel(QtWidgets.QMainWindow):
    def __init__(self):
        
        super().__init__()
        

        self.btn_start_fit = QtWidgets.QPushButton('Start fitting')
        self.btn_show_multiple_plots = QtWidgets.QCheckBox('Allow to plot multiple curves')
        self.btn_brows = QtWidgets.QPushButton('Brows')
        self.btn_brows.clicked.connect(self.run_brows)
        
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.btn_start_fit,0,0)
        self.layout.addWidget(self.btn_brows,0,1)
        self.layout.addWidget(self.btn_show_multiple_plots,1,0)
        
        
    def run_brows(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Single File', QtCore.QDir.rootPath() , 'Any File (*) ;; XML Files (*.xlsm)')
        self.data_object = Data.Data(self.filename)
        print(self.filename)


        

     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
