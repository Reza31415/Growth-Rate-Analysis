# -*- coding: utf-8 -*-
"""
Created on Tue May 11 00:29:28 2021

@author: Reza-G510
"""
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


import string


from Canvas_Plot import Canvas_Plot
from Canvas_OD import  Canvas_OD
from Methods import Methods
from Wells_Panel import Wells_Panel

class Tab(QtWidgets.QMainWindow, Methods):
    def __init__(self):
        super().__init__()
        # Making a tab widget. 
        self.tab = QtWidgets.QTabWidget()  
        self.tab.setMovable(True)
        # Elements of plot derivative tab
        # +++++++++++++++++++++++++++++++
        #An object forming part of GUI. It makes a canvas on which the derivative of OD is shown
        self.canvas_derivative = Canvas_Plot(width = 5, height = 5, dpi = 100) 
        #The toobar associated with canvas_derivative
        self.toolbar_canvas_derivative = NavigationToolbar(self.canvas_derivative, self)
        #Disabling displaying coordinates on the toolbar
        self.canvas_derivative.ax1.format_coord = lambda x, y: ""
        self.canvas_derivative.ax2.format_coord = lambda x, y: ""
        # Avertical Qt layout which will hold the canvas_derivative and its toolbar
        self.layout_canvas_derivative = QtWidgets.QVBoxLayout()
        self.layout_canvas_derivative.addWidget(self.toolbar_canvas_derivative)
        self.layout_canvas_derivative.addWidget(self.canvas_derivative)
        
        self.slider = QtWidgets.QSlider()
        self.slider.setRange(1, 100)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(50)
        
        
        self.layout_slider = QtWidgets.QHBoxLayout()
        self.layout_slider.addLayout(self.layout_canvas_derivative)
        self.layout_slider.addWidget(self.slider)
        # Makign a widget to put the layout2 in it
        self.tab_plot_derivatives = QtWidgets.QWidget()
        self.tab_plot_derivatives.setLayout(self.layout_slider)
        
        
        #A button to update the selected time window in self.dict_time_window 
        self.btn_update_time_window = QtWidgets.QAction('Update the time window for current selection')
        #Puts the button in the toolbar
        self.toolbar_canvas_derivative.addAction(self.btn_update_time_window)
        #A button which sets the same time window for all wells
        self.btn_same_time_window = QtWidgets.QAction('Use the same time window for all')
        self.btn_same_time_window.setCheckable(True)
        self.toolbar_canvas_derivative.addAction(self.btn_same_time_window)
        # End of the elements of plot derivative tab
        # +++++++++++++++++++++++++++++++
        
        
        # Elements of table tab. This table holds the the strain name of each well
        # +++++++++++++++++++++++++++
        self.table_template = QtWidgets.QTableWidget()
        self.table_template.setAlternatingRowColors(True)
        self.table_template.setRowCount(8)
        self.table_template.setColumnCount(12)
        self.table_template.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_template.setVerticalHeaderLabels(list(string.ascii_uppercase)[0:8])
        self.table_template.setHorizontalHeaderLabels([str(number) for number in range(1,13)])
        for row in range(8):
            for col in range(12):
                self.table_template.setItem(row,col,QtWidgets.QTableWidgetItem())
        # self.table_template.setItem(0,0,QtWidgets.QTableWidgetItem('Double click to edit'))
        self.label_template = QtWidgets.QLabel()
        self.label_template.setText('The above table is a template to give each well a name, for example, the name of strain in that well. Double click on each well to edit.')
        
        # End of elements of table tab
        # +++++++++++++++++++++++++++
        
        
        self.table_stats = QtWidgets.QTableWidget()
        
        
        # Elements of table tab. This table holds the doubling times
        # +++++++++++++++++++++++++++
        self.table = QtWidgets.QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setRowCount(8)
        self.table.setColumnCount(12)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setVerticalHeaderLabels(list(string.ascii_uppercase)[0:8])
        self.table.setHorizontalHeaderLabels([str(number) for number in range(1,13)])
        
        self.label_dtime = QtWidgets.QLabel()
        self.label_dtime.setText('The doubling times are in minutes')
        
        self.layout_table_dtimes = QtWidgets.QVBoxLayout()
        

        
        self.layout_table_dtimes.addWidget(self.table_template)
        self.layout_table_dtimes.addWidget(self.label_template)
        self.layout_table_dtimes.addWidget(self.table)
        self.layout_table_dtimes.addWidget(self.label_dtime)
        
        self.table_dtimes_widget = QtWidgets.QWidget()
        self.table_dtimes_widget.setLayout(self.layout_table_dtimes)
        # End of elements of table tab
        # +++++++++++++++++++++++++++
        
        # Start of a grid of QLabel to show the statistics of each strain
        # +++++++++++++++++++++++++++++++++++++++
        

        
       
        
        
        # End of statistics for each strain
        # +++++++++++++++++++++++++++++++
        
        # Elements of table tab. This table holds the final OD
        # +++++++++++++++++++++++++++
        self.table_OD = QtWidgets.QTableWidget()
        self.table_OD.setAlternatingRowColors(True)
        self.table_OD.setRowCount(8)
        self.table_OD.setColumnCount(12)
        self.table_OD.setVerticalHeaderLabels(list(string.ascii_uppercase)[0:8])
        self.table_OD.setHorizontalHeaderLabels([str(number) for number in range(1,13)])
        self.label_OD = QtWidgets.QLabel()
        self.label_OD.setText('The table shows the average of last five data point as the final OD')
        self.layout_table_OD = QtWidgets.QVBoxLayout()
        self.layout_table_OD.addWidget(self.table_OD)
        self.layout_table_OD.addWidget(self.label_OD)
        self.table_OD_widget = QtWidgets.QWidget()
        self.table_OD_widget.setLayout(self.layout_table_OD)
        # End of elements of table tab
        # +++++++++++++++++++++++++++
        
        # Elements of temperature plot tab
        # ++++++++++++++++++++++++++++++++
        self.canvas_temp = Canvas_OD(width = 5, height = 5, dpi = 100) 
        self.canvas_temp.ax1.plot([], [])
        self.toolbar_canvas_temp = NavigationToolbar(self.canvas_temp, self)
        self.layout_canvas_temp = QtWidgets.QVBoxLayout()
        self.layout_canvas_temp.addWidget(self.toolbar_canvas_temp)
        self.layout_canvas_temp.addWidget(self.canvas_temp)
        self.widget_layout_canvas_temp = QtWidgets.QWidget()
        self.widget_layout_canvas_temp.setLayout(self.layout_canvas_temp)
        # End of elements of temperature plot tab
        # ++++++++++++++++++++++++++++++
        
        
        # Elements of multiple plots tab
        #++++++++++++++++++++++++++++++++
        self.canvas_multiple_plots = Canvas_OD(width = 5, height = 5, dpi = 100) 
        self.canvas_multiple_plots.ax1.plot([], [])
        self.toolbar_canvas_multiple_plots = NavigationToolbar(self.canvas_multiple_plots, self)
        self.wells_panel_mplots = Wells_Panel('check_box')
        
        self.btn_push = QtWidgets.QPushButton('Deselect all')
        self.layout_canvas_multiple_plots = QtWidgets.QVBoxLayout()
        self.layout_canvas_multiple_plots.addWidget(self.toolbar_canvas_multiple_plots)
        self.layout_canvas_multiple_plots.addWidget(self.canvas_multiple_plots)
        self.layout_canvas_multiple_plots.addLayout(self.wells_panel_mplots.layout_check_button_panel)
        self.layout_canvas_multiple_plots.addWidget(self.btn_push)
        self.widget_layout_canvas_multiple_plots = QtWidgets.QWidget()
        self.widget_layout_canvas_multiple_plots.setLayout(self.layout_canvas_multiple_plots)
        
        
        
        # End of elements of multiple plots tab
        # ++++++++++++++++++++++++++++++++++++++++++
        
       
        # Adding the tab_widget to the tab. The tab object only accepts widgets, not layouts!
        self.tab.addTab(self.tab_plot_derivatives, 'Plot of derivatives')
        self.tab.addTab(self.table_dtimes_widget, 'Doubling times')
        self.tab.addTab(self.widget_layout_canvas_temp, 'Plot of temperature')
        self.tab.addTab(self.widget_layout_canvas_multiple_plots, 'Multiple plots')
        self.tab.addTab(self.table_OD_widget, 'Final OD')
        #To show the tab I put it in a layout
        self.tab_layout = QtWidgets.QVBoxLayout()
        self.tab_layout.addWidget(self.tab)
        
        
        
        


                
                
                