# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:20:51 2021

@author: Reza-G510
"""
import os
from scipy.interpolate import UnivariateSpline
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import numpy as np
import datetime
from Messages import Messages
import string
import matplotlib.pyplot as plt
from Canvas_Table import Canvas_Table

from PyQt5 import QtWidgets
from Canvas_OD import Canvas_OD
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.patches import Rectangle

from Data import Data

class Methods(Messages):
    
    
    def __init__(self):
        self.result_fit_dtime = {}
        self.result_fit_params = {}
        self.result_matrix = np.zeros((8,12)) 
        # Makign a table to put in the other tab

        super().__init__()
        
        
    def reset_time_window(self):
        self.dict_time_window = {}
        for key in self.dict_default_time_window:
            self.dict_time_window[key] = self.dict_default_time_window[key]
            
        for key in self.wells_panel.radio_buttons:
            value_temp = self.wells_panel.radio_buttons[key]
            #If a well is selected updates the dictionary of time windows and plot the selected part on the OD_canvas in red
            if value_temp.isChecked():
                self.plot_selection_in_red(key)


        self.plot_derivatives()
                
        
        
    def set_s(self,value):
        for key in self.wells_panel.radio_buttons:
            if self.wells_panel.radio_buttons[key].isChecked():
                self.dict_s[key] =  value*0.001
            
    # Object method. If called plots the OD curve of the respective button or well and calls self.plot_derivatives to show the derivatives of the OD curve
    def plot_OD(self):
        try:
            # # is the name of the button which called this method
            # sender = self.sender()
            # well_name = str(sender.text())
            for key in self.wells_panel.radio_buttons:
                if self.wells_panel.radio_buttons[key].isChecked():
                    well_name = key
            data = self.fit_panel.data_object.data_dict[well_name]
            time = self.fit_panel.data_object.time
            # The try statement prevents an error if the user clicks on a well button without loading the data beforehand. 
            # #Calls the method for plotting derivatives
            # self.plot_derivatives()
            # If the user has asked for the same time window for all wells skips to the next part.
            if not self.tab.btn_same_time_window.isChecked():
                self.canvas_OD.ax1.cla()
                self.canvas_OD.ax1.plot(time, data, label = 'Growth curve')
                self.canvas_OD.ax1.set_xlabel('Time - minutes')
                self.canvas_OD.ax1.set_ylabel('OD')
                # The try statement prevents an error if the user clicks on a well button. 
                # Without it the selected time window will not be plotted if the well is not present in self.dict_time_window
    
                try:
                    self.canvas_OD.ax1.plot(time[self.dict_time_window[well_name][0]:self.dict_time_window[well_name][1]], 
                                            data[self.dict_time_window[well_name][0]:self.dict_time_window[well_name][1]], 'r', linewidth = 2, label = 'Selection for fitting')
                    self.canvas_OD.ax1.set_xlabel('Time - minutes')
                    self.canvas_OD.ax1.set_ylabel('OD')
                except KeyError:
                    pass
                
                try:
                    fitted_time = time[self.dict_time_window[well_name][0]:self.dict_time_window[well_name][1]]
                    fitted_params = self.result_fit_params[well_name]
                    self.canvas_OD.ax1.plot(fitted_time, self.model(fitted_time, fitted_params), 'k--', linewidth = 2, label = 'Fitted curve')
                    self.canvas_OD.ax1.set_xlabel('Time - minutes')
                    self.canvas_OD.ax1.set_ylabel('OD')
                except KeyError:
                    pass
                self.canvas_OD.ax1.legend()
                self.canvas_OD.draw()
                
            else:
                self.canvas_OD.ax1.cla()
                self.canvas_OD.ax1.plot(time, data)
                self.canvas_OD.ax1.plot(time[self.same_time_window[0]:self.same_time_window[1]], data[self.same_time_window[0]:self.same_time_window[1]], 'r', linewidth = 2)
                try:
                    fitted_time = time[self.same_time_window[0]:self.same_time_window[1]]
                    fitted_params = self.result_fit_params[well_name]
                    self.canvas_OD.ax1.plot(fitted_time, self.model(fitted_time, fitted_params), 'k--', linewidth = 2)
                    self.canvas_OD.ax1.set_xlabel('Time - minutes')
                    self.canvas_OD.ax1.set_ylabel('OD')
                except KeyError:
                    pass
                self.canvas_OD.ax1.set_xlabel('Time - minutes')
                self.canvas_OD.ax1.set_ylabel('OD')
                self.canvas_OD.draw()
            self.plot_derivatives()
        except AttributeError:
            self.error_msg_no_data.exec_()
            
    
            
    def multi_select_plot_OD(self):
        sender = self.sender()
        sender_name = str(sender.text()) 
        
        if 'Plot row' in sender_name:
                for col in range(1,13):
                    if sender.isChecked():
                        self.tab.wells_panel_mplots.check_boxes[f'{sender_name[-1]}{col}'].setChecked(True)
                    elif not sender.isChecked():
                        self.tab.wells_panel_mplots.check_boxes[f'{sender_name[-1]}{col}'].setChecked(False)
        elif 'Col' in sender_name:
            for row in self.alphabet:
                if sender.isChecked():
                    self.tab.wells_panel_mplots.check_boxes[f'{row}{sender_name[3:]}'].setChecked(True)
                elif not sender.isChecked():
                    self.tab.wells_panel_mplots.check_boxes[f'{row}{sender_name[3:]}'].setChecked(False)
                
        self.multi_plot_OD()
        
        
        
        
    def plot_dict(self):
        time = self.fit_panel.data_object.time
        for key in self.tab.wells_panel_mplots.check_boxes:
            data = self.fit_panel.data_object.data_dict[key]
            self.dict_multi_plot[key], = self.tab.canvas_multiple_plots.ax1.plot(time, data)
            self.dict_multi_plot[key].set_visible(False)
        
        
    # Object method. If called plots the OD curve of the respective button or well and calls self.plot_derivatives to show the derivatives of the OD curve
    def multi_plot_OD(self):
        plot_labels = set()
        plot_handles = set()
        for key in self.tab.wells_panel_mplots.check_boxes:
            if self.tab.wells_panel_mplots.check_boxes[key].isChecked():
                print(key)
                self.dict_multi_plot[key].set_visible(True)
                plot_labels.add(key)
                plot_handles.add(self.dict_multi_plot[key])
            elif not self.tab.wells_panel_mplots.check_boxes[key].isChecked():
                self.dict_multi_plot[key].set_visible(False)
                plot_labels.discard(key)
                plot_handles.discard(self.dict_multi_plot[key])

        self.tab.canvas_multiple_plots.ax1.set_xlabel('Time - minutes')
        self.tab.canvas_multiple_plots.ax1.set_ylabel('OD')
        self.tab.canvas_multiple_plots.ax1.legend(handles = plot_handles, labels = plot_labels)
        self.tab.canvas_multiple_plots.draw()

            
    def deselect_all(self):
        for key in self.tab.wells_panel_mplots.check_boxes:
                self.tab.wells_panel_mplots.check_boxes[key].setChecked(False)
                
        for key in self.tab.wells_panel_mplots.row_select:
            self.tab.wells_panel_mplots.row_select[key].setChecked(False)
            
        for key in self.tab.wells_panel_mplots.col_select:
            self.tab.wells_panel_mplots.col_select[key].setChecked(False)
            
        self.multi_plot_OD()
            
    # The method to plot the derivatives of OD and select a time window       
    def plot_derivatives(self):
        for key in self.wells_panel.radio_buttons:
            if self.wells_panel.radio_buttons[key].isChecked():
                chosen_well = key
                
        try:
            data = self.fit_panel.data_object.data_dict[chosen_well]
            time = self.fit_panel.data_object.time
            fit = UnivariateSpline(time, data, k = 5, s= self.dict_s[chosen_well])
            fit1d = fit.derivative(n = 1)
            fit2d = fit.derivative(n = 2)
            self.tab.canvas_derivative.time = time
            norm_fit1d = fit1d(time)/np.max(fit1d(time))
            norm_fit2d = fit2d(time)/np.max(fit2d(time))
            self.tab.canvas_derivative.ax1.cla()
            self.tab.canvas_derivative.ax1.plot(time ,  norm_fit1d)
            self.tab.canvas_derivative.ax1.plot(time ,  norm_fit2d)
            self.tab.canvas_derivative.ax1.plot(time ,  0*time, 'k')
            
            self.tab.canvas_derivative.ax2.cla()
            self.tab.canvas_derivative.ax2.plot(time ,  data, 'k')
            self.tab.canvas_derivative.ax2.plot(time ,  fit(time), ':r')
            
            self.tab.canvas_derivative.ax1.legend(['1st derivative', '2nd derivative'])
            self.tab.canvas_derivative.ax2.legend(['Measured growth curve','Spline fit to the growth curve'])
            self.tab.canvas_derivative.ax2.set_xlabel('Time - minutes')
            self.tab.canvas_derivative.ax2.set_ylabel('OD')
            self.tab.canvas_derivative.ax1.set_xlabel('Time - minutes')
            self.tab.canvas_derivative.ax1.set_ylabel('OD')
            self.tab.slider.setSliderPosition(round(self.dict_s[chosen_well]/self.s_multiplier))
            # Draw a rectangle on the selected area of the 2nd derivative
            if not self.tab.btn_same_time_window.isChecked():
                try:
                    min_time = time[self.dict_time_window[chosen_well][0]]
                    max_time = time[self.dict_time_window[chosen_well][1]]
                    self.tab.canvas_derivative.ax1.add_patch(Rectangle((min_time, np.min(norm_fit2d)), 
                                                                   max_time - min_time, 
                                                                   np.abs(np.min(norm_fit2d)) + 
                                                                   np.max(norm_fit2d), 
                                                                   fill=True, zorder=2, alpha = 0.1))
                    
                except KeyError:
                    pass
                
            else:
                min_time = time[self.same_time_window[0]]
                max_time = time[self.same_time_window[1]]
                self.tab.canvas_derivative.ax1.add_patch(Rectangle((min_time, np.min(norm_fit2d)), 
                                                                               max_time - min_time, 
                                                                               np.abs(np.min(norm_fit2d)) + 
                                                                               np.max(norm_fit2d), 
                                                                               fill=True, zorder=2, alpha = 0.1))
                        
            self.tab.canvas_derivative.draw()
        except AttributeError:
            self.error_msg_no_data.exec_()
        
        
        
        
    def plot_selection_in_red(self, well_name):
        if not self.tab.btn_same_time_window.isChecked():
            try:
                [min_index, max_index] = self.dict_time_window[well_name]
            except KeyError:
                pass

        else:
            try:
                [min_index, max_index] = self.same_time_window
            except KeyError:
                pass
            
        data = self.fit_panel.data_object.data_dict[well_name]
        time = self.fit_panel.data_object.time
        self.canvas_OD.ax1.cla()
        self.canvas_OD.ax1.plot(time, data, label = 'Growth curve')
        self.canvas_OD.ax1.plot(time[min_index:max_index], data[min_index:max_index], 'r', linewidth = 2, label = 'Selection for fitting')
        self.canvas_OD.ax1.set_xlabel('Time - minutes')
        self.canvas_OD.ax1.set_ylabel('OD')
        self.canvas_OD.ax1.legend()
        self.canvas_OD.draw()
        self.plot_derivatives()
    
                

    # The slot called by a button to update the dictionary containing the selected time windows
    def update_time_window(self): 
        if not self.tab.btn_same_time_window.isChecked():
            try:
                min_index = self.tab.canvas_derivative.min_index
                max_index = self.tab.canvas_derivative.max_index
            except AttributeError:
                min_index = 0
                max_index = len(self.fit_panel.data_object.time)
            # self.wells_panel.radio_buttons is a dictionary containing the buttons associated to each well
            for key in self.wells_panel.radio_buttons:
                value_temp = self.wells_panel.radio_buttons[key]
                #If a well is selected updates the dictionary of time windows and plot the selected part on the OD_canvas in red
                if value_temp.isChecked():
                    self.dict_time_window[key] = [min_index, max_index]
                    self.plot_selection_in_red(key)
                    
        else:
            #If the dictinary is emty that is no time window is selected gives an error message
            if len(list(self.dict_time_window.keys())) == 0:
                self.error_message.exec_()
                self.btn_same_time_window.setChecked(False)
            else:
                    # try:
                    min_index = self.tab.canvas_derivative.min_index
                    max_index = self.tab.canvas_derivative.max_index
                    self.same_time_window = [min_index, max_index] 
                    self.plot_derivatives()
                    self.result_fit_params.clear()
                    for key in self.wells_panel.radio_buttons:
                        value_temp = self.wells_panel.radio_buttons[key]
                       #If a well is selected updates the dictionary of time windows and plot the selected part on the OD_canvas in red
                        if value_temp.isChecked():
                            self.plot_selection_in_red(key)
                    # except KeyError:
                    #     pass
           
 
    def run_brows(self):
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Single File', os.getcwd() , 'XML Files (*.xlsx)')

        try:
            self.fit_panel.data_object = Data(self.filename)
            
            self.tab.canvas_temp.ax1.cla()
            self.tab.canvas_temp.ax1.plot(self.fit_panel.data_object.time, self.fit_panel.data_object.temperature, '*k')
            self.tab.canvas_temp.ax1.set_xlabel('Time - minutes')
            self.tab.canvas_temp.ax1.set_ylabel('Temperature -- Celsius')
            self.tab.canvas_temp.draw()
            
            self.result_fit_params.clear()
            
            self.initialize_time_windows()
            self.final_OD()
            for row, letter in enumerate(self.alphabet):
                for col, number in enumerate(range(1,13)):
                    key = f'{letter}{number}'
                    self.tab.table_OD.setItem(row, col, QtWidgets.QTableWidgetItem(f'{self.dict_final_OD[key]}'))
            
            final_od_matrix = np.zeros((8,12))
            for row, letter in enumerate(self.alphabet):
                for col, number in enumerate(range(1,13)):
                    key = f'{letter}{number}'
                    final_od_matrix[row, col] = self.dict_final_OD[key]
                    
                    
            
            # for col in range(12):
            #     self.tab.table_OD.setItem(8, col, QtWidgets.QTableWidgetItem(f'{round(np.mean(final_od_matrix[:,col]),2)}'))  
            #     self.tab.table_OD.setItem(9, col, QtWidgets.QTableWidgetItem(f'{round(np.std(final_od_matrix[:,col]),2)}'))  
                
            # for row in range(8):
            #     self.tab.table_OD.setItem(row, 12, QtWidgets.QTableWidgetItem(f'{round(np.mean(final_od_matrix[row,:]),2)}'))  
            #     self.tab.table_OD.setItem(row, 13, QtWidgets.QTableWidgetItem(f'{round(np.std(final_od_matrix[row,:]),2)}'))  
            
            self.wells_panel.radio_buttons['A1'].setChecked(True)
            self.plot_dict()
            self.plot_OD()
        except (AttributeError, FileNotFoundError):
            self.error_msg_no_data.exec_()



    
    def correlation(self,a,k):
        # a is a 1d array
        # k is the shift in data against which the correlation of a is calculated.
        b = 0*a
        for i in range(len(a)):
            if i > 0:
                b[i-k] = a[i]         
        a_mean = np.mean(a)
        b_mean = np.mean(b)
        ab_mean = np.mean(a*b)
        a_var = np.std(a)
        b_var = np.std(b)
        res = (ab_mean-a_mean*b_mean)/(a_var*b_var)
        return res



    def initialize_time_windows(self):
        for letter in self.alphabet:
            for number in range(1,13):
                key = f'{letter}{number}'
                time = self.fit_panel.data_object.time
                data = self.fit_panel.data_object.data_dict[key]
                for step in range(1,100):
                    s = self.s_multiplier*step
                    fit = UnivariateSpline(time, data, k = 5, s= s)
                    fit2d = fit.derivative(n = 2)
                    correlation_const = self.correlation(fit2d(time),1)
                    if correlation_const >= 0.99:
                        self.dict_s[key] = s
                        norm_fit2d = fit2d(time)/np.max(fit2d(time))
                        res = argrelextrema(norm_fit2d, np.greater)
                        try:
                            res = res[0]
                            index = res[0]
                            for value in res:
                                if norm_fit2d[value] > norm_fit2d[index]:
                                    index = value
                            self.dict_default_time_window[key] = [0, index]
                            self.dict_time_window[key] = [0, index]
                        except IndexError:
                            pass
                        
                        break
                        

        
    def final_OD(self):
        for letter in self.alphabet:
            for number in range(1, 13):
                key = f'{letter}{number}'
                data = self.fit_panel.data_object.data_dict[key]
                mean_OD = np.mean(data[-5:])
                self.dict_final_OD[key] = round(mean_OD,2)
                
        

    #The model for exponential growth. There are three parameters, amp is the amplitude, rate the rate of 
    # growth multiplied by log(2) to convert it to doubling rate, and the bg as the background
    def model(self, taxis, params):
        amp = params[0]
        rate = params[1]
        bg = params[2]
        return amp*np.exp(taxis*rate*np.log(2)) + bg
            
    # The slot after selecting the button to run the fit process       
    def run_fit(self):
        self.result_fit_dtime = {}
        self.result_fit_params = {}
        alphabet = list(string.ascii_uppercase)[0:8]
        
        #The model for exponential growth. There are three parameters, amp is the amplitude, rate the rate of 
        # growth multiplied by log(2) to convert it to doubling rate, and the bg as the background
        def model(taxis, amp, rate, bg):
            return amp*np.exp(taxis*rate*np.log(2)) + bg
        # If the use has not asked for the same time window for all the wells proceeds
        if not self.tab.btn_same_time_window.isChecked():
            for key in self.dict_time_window:
                time_fit = self.fit_panel.data_object.time
                data_fit = self.fit_panel.data_object.data_dict[key]
                min_index_temp = self.dict_time_window[key][0]
                max_index_temp = self.dict_time_window[key][1]
                time_fit = time_fit[min_index_temp:max_index_temp]
                data_fit = data_fit[min_index_temp:max_index_temp]
                popt_temp, pcov_temp = curve_fit(model, time_fit, data_fit, p0 = [0.001, 1/90, 0.098], maxfev = 8000, bounds = ([0,0,0],[np.inf, np.inf, np.inf]))
                self.result_fit_dtime[key] = round(1/popt_temp[1],1)
                self. result_fit_params[key] = popt_temp
                
        elif self.tab.btn_same_time_window.isChecked():
            for letter in self.alphabet:
                for number in range(1,13):
                    key = f'{letter}{number}'
                    time_fit = self.fit_panel.data_object.time
                    data_fit = self.fit_panel.data_object.data_dict[key]
                    min_index_temp = self.same_time_window[0]
                    max_index_temp = self.same_time_window[1]
                    time_fit = time_fit[min_index_temp:max_index_temp]
                    data_fit = data_fit[min_index_temp:max_index_temp]
                    popt_temp, pcov_temp = curve_fit(model, time_fit, data_fit, p0 = [0.001, 1/90, 0.098], maxfev = 8000, bounds = ([0,0,0],[np.inf, np.inf, np.inf]))
                    self.result_fit_dtime[key] = round(1/popt_temp[1],1)
                    self. result_fit_params[key] = popt_temp

         
        self.text_file_name = str(datetime.datetime.now()) 
        self.text_file_name = self.text_file_name[0:-7] 
        self.text_file_name = self.text_file_name.replace(':', '-')
        self.text_file_name = self.text_file_name.replace(' ', '_')
        with open(f'fitting_results_{self.text_file_name}.txt','w') as text_file:
            text_file.write('The doubling times are in minutes\n')
            for key in self.result_fit_dtime:
                text_file.writelines(f'{key}:{self.result_fit_dtime[key]}\n')
        
          
        self.result_fit_dtime_values = self.result_fit_dtime.values()
        self.result_matrix = np.zeros((8,12))
        for key in self.result_fit_dtime:
            letter_part = key[0]
            col = int(key[1:])-1
            row = alphabet.index(letter_part)
            self.result_matrix[row, col] = self.result_fit_dtime[key]
        
        # Putting the doubling times in the table
        self.tab.table.clearContents()
        for row in range(8):
            for col in range(12):
                self.tab.table.setItem(row, col, QtWidgets.QTableWidgetItem(f'{self.result_matrix[row,col]}'))  
                
        
        #Check the template to extract the well's name and to calculate the mean and standard deviation of each strain
        wells_same_name_coords = dict()
        for row in range(8):
            for col in range(12):
                well_name = self.tab.table_template.item(row,col).text()
                dict_keys = list(wells_same_name_coords.keys())
                if well_name in dict_keys:
                    wells_same_name_coords[well_name].append([row,col])
                elif well_name not in dict_keys:
                    wells_same_name_coords[well_name] = []
                    wells_same_name_coords[well_name].append([row,col])
        
            
        
        self.tab.table_stats.clearContents()
        self.tab.table_stats.setAlternatingRowColors(True)
        self.tab.table_stats.setColumnCount(len(dict_keys))
        self.tab.table_stats.setRowCount(3)
        self.tab.table_stats.setVerticalHeaderLabels(['Name of strain', 'Mean of doubling time', 'Standard deviation of mean'])
        self.tab.table_stats.setHorizontalHeaderLabels([str(number) for number in range(1,1+len(dict_keys))])

        # Getting the name of each well with its coordinates. Then calculate the mean and std for all wells with the same name
        # The results are displayed in a new table.
        for col, key in enumerate(dict_keys):
            if key:
                coords = wells_same_name_coords[key]
                mean_list = []
                std_list = []
                for ii, jj in coords:
                        mean_list.append(self.result_matrix[ii,jj])
                        std_list.append(self.result_matrix[ii,jj])
                        
                mean = np.mean(mean_list)      
                std = np.std(std_list)
                self.tab.table_stats.setItem(0, col, QtWidgets.QTableWidgetItem(f'{key}'))
                self.tab.table_stats.setItem(1, col, QtWidgets.QTableWidgetItem(f'{round(mean,2)}'))
                self.tab.table_stats.setItem(2, col, QtWidgets.QTableWidgetItem(f'{round(std,2)}'))
            elif not key:
                coords = wells_same_name_coords[key]
                mean_list = []
                std_list = []
                for ii, jj in coords:
                        mean_list.append(self.result_matrix[ii,jj])
                        std_list.append(self.result_matrix[ii,jj])
                        
                mean = np.mean(mean_list)      
                std = np.std(std_list)
                self.tab.table_stats.setItem(0, col, QtWidgets.QTableWidgetItem('Wells with no Name'))
                self.tab.table_stats.setItem(1, col, QtWidgets.QTableWidgetItem(f'{round(mean,2)}'))
                self.tab.table_stats.setItem(2, col, QtWidgets.QTableWidgetItem(f'{round(std,2)}'))
        
        
   
        self.tab.layout_table_dtimes.addWidget(self.tab.table_stats)
        
        

                
        self.plot_OD()
        self.done_message.exec_()


