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
        #Reads which rows in the excel file the data starts and ends
        

                

        self.data_dict = {}
        self.temperature = []
        self.time = []
        self.filename = filename
        self.alphabet = list(string.ascii_uppercase)[0:8]
        
        # Gives header names to columns
        self.cols = ['0', 'time', 'temp']
        for i in self.alphabet:
            for j in range(12):
                self.cols.append(f'{i}{j+1}')
                
        self.df = pd.read_excel(self.filename, names = self.cols)
        
        collect = []
        count = 0
        for index, i in enumerate(self.df['temp']):
            if (type(i) == float or type(i) == int):
                if not np.isnan(i) and count == 0:
                    count = 1
                    collect.append(index)
                elif not np.isnan(i):
                    collect.append(index)
                elif np.isnan(i) and count == 1:
                    break
                
        self.r1 = collect[0]
        self.r2 = collect[-1]      
        self.temperature = self.df['temp'].values[self.r1:self.r2]

        #Read the time axis
        self.time_temp = []
        #Convert the time axis to minutes
        for element in self.df['time'][self.r1:self.r2]:
            try:
                self.time_temp.append(round(element.day*24*60 + element.hour*60 + element.minute + element.second/60,1))
            except AttributeError:
                self.time_temp.append(round(element.hour*60 + element.minute + element.second/60,1))
        self.time = np.array(self.time_temp, dtype = float)

        for letter in self.alphabet:
            for number in range(12):
                key = f'{letter}{number+1}'
                data_temp = self.df[key].values[self.r1:self.r2]
                self.data_temp = np.array(data_temp, dtype = float)
                self.data_dict[key] = self.data_temp
        
        
        
        


    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
