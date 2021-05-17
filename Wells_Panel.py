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


class Wells_Panel(QtWidgets.QMainWindow):
    def __init__(self, button):
        
        super().__init__()
        
        alphabet = list(string.ascii_uppercase)[0:8]
        
        if button == 'radio_button':
        
            #Creates all the buttons from A1, A2, to ... H11, H12. In total 96 radio buttons
            self.radio_buttons = {}
            for row in alphabet:
                for col in range(1,13):
                    self.radio_buttons[f'{row}{col}'] = QtWidgets.QRadioButton(f'{row}{col}')
    
                    
            #Creating 8 horizontal layouts to have the buttons of each row. Each row has 12 buttons.
            self.layouts_radio_button = {}
            for i in alphabet:
                 self.layouts_radio_button[i] = QtWidgets.QHBoxLayout()
                 
            #Insering the buttons in each row in their respective horizontal layout   
            for letter in alphabet:
                for number in range(1,13):
                    self.layouts_radio_button[letter].addWidget(self.radio_buttons[f'{letter}{number}'])
            
    
         
            #Putting all the horizontla layouts in a single vertical layout
            self.layout_radio_button_panel = QtWidgets.QVBoxLayout()
            for letter in alphabet:
                self.layout_radio_button_panel.addLayout(self.layouts_radio_button[letter])
                
        elif button == 'check_box':
            
            #Creates all the buttons from A1, A2, to ... H11, H12. In total 96 radio buttons
            self.check_boxes = {}
            for row in alphabet:
                for col in range(1,13):
                    self.check_boxes[f'{row}{col}'] = QtWidgets.QCheckBox(f'{row}{col}')
    
            
            

         
            #Putting all the horizontla layouts in a single vertical layout
            self.layout_check_button_panel = QtWidgets.QGridLayout()
            for row, letter in enumerate(alphabet):
                for col, number in enumerate(range(1,13)):
                    self.layout_check_button_panel.addWidget(self.check_boxes[f'{letter}{number}'] ,row,col)



            self.col_select = {}
            for col in range(1,13):
                self.col_select[f'{col}'] = QtWidgets.QCheckBox(f'Col{col}')
                
            
            for col, number in enumerate(range(1,13)):
                self.layout_check_button_panel.addWidget(self.col_select[f'{number}'],8,col)
        

            self.row_select = {}
            for row in alphabet:
                self.row_select[f'{row}'] = QtWidgets.QCheckBox(f'Plot row {row}')
            
            
            for number, letter in enumerate(alphabet):
                self.layout_check_button_panel.addWidget(self.row_select[f'{letter}'],number,13)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
