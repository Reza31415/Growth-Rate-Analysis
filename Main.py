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

import Wells_Panel
import Canvas_Plot
import Fit_Panel
import Data
import Canvas_OD
from Methods import Methods
matplotlib.use('Qt5Agg')


  
class MainWindow(QtWidgets.QMainWindow, Methods):
    def __init__(self):
        super().__init__()
        #Makes a list of alphabets from A to H
        self.alphabet = list(string.ascii_uppercase)[0:8]  
        #A dictionary of selected time windows for each well
        self.dict_time_window = {}  
        #The parameter that sets the same time window for all wells
        self.same_time_window = []  
        #An object forming part of the GUI. It contains buttons to select different wells
        self.wells_panel = Wells_Panel.Wells_Panel()  
        #An object forming part of GUI. It contains buttons related to running the fitting process
        self.fit_panel = Fit_Panel.Fit_Panel()  
        #If the brows button is pushed, after finding the file, it retirves the measurement data
        self.fit_panel.btn_brows.clicked.connect(self.get_data) 
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
        #An object forming part of GUI. It makes a canvas on which the derivative of OD is shown
        self.canvas_derivative = Canvas_Plot.Canvas_Plot(width = 5, height = 5, dpi = 100) 
        #The toobar associated with canvas_derivative
        self.toolbar2 = NavigationToolbar(self.canvas_derivative, self)
        #Disabling displaying coordinates on the toolbar
        self.canvas_derivative.ax1.format_coord = lambda x, y: ""
        self.canvas_derivative.ax2.format_coord = lambda x, y: ""
        # Avertical Qt layout which will hold the canvas_derivative and its toolbar
        self.layout2 = QtWidgets.QVBoxLayout()
        self.layout2.addWidget(self.toolbar2)
        self.layout2.addWidget(self.canvas_derivative)
        #A button to update the selected time window in self.dict_time_window 
        self.btn_update_time_window = QtWidgets.QAction('Update the time window for current selection')
        #Connect the button updating the selected time window to the desired slot
        self.btn_update_time_window.triggered.connect(self.update_time_window)
        #Puts the button in the toolbar
        self.toolbar2.addAction(self.btn_update_time_window)
        #A button which sets the same time window for all wells
        self.btn_same_time_window = QtWidgets.QAction('Use the same time window for all')
        self.btn_same_time_window.setCheckable(True)
        #Calls the slot and the last element of self.dict_time_window is set as the same time window for all wells
        self.btn_same_time_window.triggered.connect(self.set_same_time_window)
        self.toolbar2.addAction(self.btn_same_time_window)
        # A Qt grid layout which holds all the elements of GUI
        self.layout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.layout1,0,0)
        self.layout.addLayout(self.layout2,0,1)
        self.layout.addLayout(self.wells_panel.layout_radio_button_panel,1,0)
        self.layout.addLayout(self.fit_panel.layout,1,1)
        #An empty widget which takes the grid layout
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # Shwoing the central widget
        self.show()
        ##############################################
        # Messages section!
        ##############################################
        #Will give an error if the user tries to set the same time window for all wells without selecting at least one time window
        self.error_message = QtWidgets.QMessageBox()
        self.error_message.setText('You should select at least one time window')
        self.error_message.setWindowTitle('Error!')
        # After fitting is done and the results are saved on disk, gives a message stating fitting is finished
        self.done_message = QtWidgets.QMessageBox()
        self.done_message.setText('Fitting is finished! The results are saved on disk.')
        self.done_message.setWindowTitle('Done!')
        # If the user tries to select a well without loading the data, gives an error message
        self.error_msg_no_data = QtWidgets.QMessageBox()
        self.error_msg_no_data.setText('Please click brows button and select the xlsx file!')
        self.error_msg_no_data.setWindowTitle('Error!')
        # Connecting the signal emmited by each well to the slot called self.plot_OD. Selecting each well plots its OD and its derivatives
        for letter in self.alphabet:
            for number in range(1,13):
                self.wells_panel.radio_buttons[f'{letter}{number}'].clicked.connect(self.plot_OD)
   
        
            
        
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
