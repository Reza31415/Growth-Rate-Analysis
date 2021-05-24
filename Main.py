# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 22:06:30 2021

@author: Reza-G510
"""

import sys 
import datetime
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


from Tab import Tab
import Wells_Panel
import Canvas_Plot
import Fit_Panel
import Data
import Canvas_OD
from Methods import Methods
from Messages import Messages
matplotlib.use('Qt5Agg')


  
class MainWindow(QtWidgets.QMainWindow, Methods, Messages):
    def __init__(self):
        super().__init__()
        self.dict_s = {}
        self.s_multiplier = 0.001
        self.dict_final_OD = {}
        self.dict_multi_plot = {}
        
        #Makes a list of alphabets from A to H
        self.alphabet = list(string.ascii_uppercase)[0:8]  
        #A dictionary of selected time windows for each well
        self.dict_time_window = {}  
        self.dict_default_time_window = {}
        #The parameter that sets the same time window for all wells
        self.same_time_window = []  
        #An object forming part of the GUI. It contains buttons to select different wells
        self.wells_panel = Wells_Panel.Wells_Panel('radio_button')  
        for letter in self.alphabet:
            for number in range(1,13):
                self.dict_s[f'{letter}{number}'] = 0.001
        #An object forming part of GUI. It contains buttons related to running the fitting process
        self.fit_panel = Fit_Panel.Fit_Panel()  
        #self.btn_show_heat_map = QtWidgets.QPushButton('Show the heat map of doubling times')
        self.fit_panel.btn_brows.clicked.connect(self.run_brows)
        self.fit_panel.btn_load_template.clicked.connect(self.load_template)
        self.fit_panel.btn_save_template.clicked.connect(self.save_template)
        self.fit_panel.btn_reset_tw.clicked.connect(self.reset_time_window)
        self.fit_panel.btn_save_results.clicked.connect(self.save_results)
        #If the brows button is pushed, after finding the file, it retirves the measurement data
        #self.fit_panel.btn_brows.clicked.connect(self.get_data) 
        
        #After clicking the related button the fitting process starts
        self.fit_panel.btn_start_fit.clicked.connect(self.run_fit)  
        #By default there is no time axis
        self.time = []  
        #By default there is no data
        self.data = []  
        #An object forming part of GUI. It makes the canvas on which the OD is plotted
        self.canvas_OD = Canvas_OD.Canvas_OD(width = 5, height = 5, dpi = 100) 

        #The toolbar associated with Canvas_OD
        self.toolbar1 = NavigationToolbar(self.canvas_OD, self)  
        # A vertical Qt layout which will hold canvas_OD and its associated toolbar
        self.layout1 = QtWidgets.QVBoxLayout() 
        self.layout1.addWidget(self.toolbar1)
        self.layout1.addWidget(self.canvas_OD)
    
        self.tab = Tab()
        #Connect the button updating the selected time window to the desired slot
        self.tab.btn_update_time_window.triggered.connect(self.update_time_window)
        #Calls the slot and the last element of self.dict_time_window is set as the same time window for all wells
        self.tab.btn_same_time_window.triggered.connect(self.update_time_window)
        self.tab.slider.valueChanged.connect(self.set_s)
        self.tab.btn_push.clicked.connect(self.deselect_all)
        self.tab.slider.valueChanged.connect(self.plot_derivatives)
        
        
        # A Qt grid layout which holds all the elements of GUI
        self.layout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.layout1,0,0)
        self.layout.addLayout(self.tab.tab_layout,0,1)
        self.layout.addLayout(self.wells_panel.layout_radio_button_panel,1,0)
        self.layout.addLayout(self.fit_panel.layout,1,1)
        #An empty widget which takes the grid layout
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # Shwoing the central widget
        self.show()

        for letter in self.alphabet:
            for number in range(1,13):
                self.wells_panel.radio_buttons[f'{letter}{number}'].clicked.connect(self.plot_OD)
                self.tab.wells_panel_mplots.check_boxes[f'{letter}{number}'].clicked.connect(self.multi_plot_OD)
                
                
        for letter in self.alphabet:
            self.tab.wells_panel_mplots.row_select[f'{letter}'].clicked.connect(self.multi_select_plot_OD)
            
        for number in range(1,13):
            self.tab.wells_panel_mplots.col_select[f'{number}'].clicked.connect(self.multi_select_plot_OD)
        
   


        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
