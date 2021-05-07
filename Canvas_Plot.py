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

class Canvas_Plot(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        
        # self.time = time
        # self.first_derivative = first_derivative
        # self.second_derivative = second_derivative
        self.fig = Figure(figsize = (width, height), dpi = dpi)
        super().__init__(self.fig)
        
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        
        #Plot the 1st and 2nd derivative interactively so that we can select the exponential growth window
        self.line2, = self.ax2.plot([], [], '-')
        
        # set useblit True on gtkagg for enhanced performance
        self.span = SpanSelector(self.ax1, self.onselect, 'horizontal', useblit=True, rectprops=dict(alpha=0.5, facecolor='red'))
        self.show()
        
        
    def onselect(self, xmin, xmax):
          indmin, indmax = np.searchsorted(self.time, (xmin, xmax))
          indmax = min(len(self.time) - 1, indmax)
     
          thisx = self.time[indmin:indmax]
          thisy = self.first_derivative[indmin:indmax]
          self.line2.set_data(thisx, thisy)
          self.ax2.set_xlim(thisx[0], thisx[-1])
          self.ax2.set_ylim(thisy.min(), thisy.max())
          self.fig.canvas.draw_idle()
         
          #The indexes which show the exponential growth time window
          self.min_index = indmin
          self.max_index = indmax
          

        
        
        
