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

import Wells_Panel
import Canvas_Plot
import Fit_Panel

matplotlib.use('Qt5Agg')

  
class Data(QtWidgets.QMainWindow):
    def __init__(self, filename):
        self.filename = filename
        self.alphabet = list(string.ascii_uppercase)[0:8]
        self.cols = ['0', 'time', 'temp']
        for i in self.alphabet:
            for j in range(12):
                self.cols.append(f'{i}{j+1}')
        self.df = pd.read_excel(self.filename, names = self.cols)
        
        #Reads which rows in the excel file the data starts and ends
        self.r1 = 30
        self.r2 = 360
        
        #Read the time axis
        self.time0 = []
        #Convert the time axis to minutes
        for element in self.df['time'][self.r1:self.r2]:
            try:
                self.time0.append(round(element.day*24*60 + element.hour*60 + element.minute + element.second/60,1))
            except AttributeError:
                self.time0.append(round(element.hour*60 + element.minute + element.second/60,1))
        
    def well_data(self, well_name):
        
        for i in self.alphabet:
            for j in range(12):
                self.cols.append(f'{i}{j+1}')

        
        #Reads which rows in the excel file the data starts and ends
        self.r1 = 30
        self.r2 = 360
        
        #Read the time axis
        self.time0 = []
        #Convert the time axis to minutes
        for element in self.df['time'][self.r1:self.r2]:
            try:
                self.time0.append(round(element.day*24*60 + element.hour*60 + element.minute + element.second/60,1))
            except AttributeError:
                self.time0.append(round(element.hour*60 + element.minute + element.second/60,1))
        #Get the data in a well
        data0 = self.df[well_name].values[self.r1:self.r2]
        self.data = np.array(data0, dtype = float)
        self.time = np.array(self.time0, dtype = float)
        return self.time, self.data

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
