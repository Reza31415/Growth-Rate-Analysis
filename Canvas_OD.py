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

class Canvas_OD(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        super().__init__(self.fig)
        self.ax1 = self.fig.add_subplot(111)
        self.show()
            


        
        
        
