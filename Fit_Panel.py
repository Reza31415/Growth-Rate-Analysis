# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 22:06:30 2021

@author: Reza-G510
"""

import sys 
import os
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

from Messages import Messages

class Fit_Panel(QtWidgets.QMainWindow, Messages):
    def __init__(self):
        
        super().__init__()
        

        self.btn_start_fit = QtWidgets.QPushButton('Start fitting')
        self.btn_brows = QtWidgets.QPushButton('Brows')
        self.btn_reset_tw = QtWidgets.QPushButton('Reset time windows')

        
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.btn_start_fit,0,0)
        self.layout.addWidget(self.btn_brows,0,1)
        self.layout.addWidget(self.btn_reset_tw, 1,0)
        
        


        

     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
