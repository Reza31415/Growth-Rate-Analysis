# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:20:51 2021

@author: Reza-G510
"""

from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import numpy as np
import datetime

class Methods():
    def __init__(self):
        
        pass
        
        
    # Object method. If called plots the OD curve of the respective button or well and calls self.plot_derivatives to show the derivatives of the OD curve
    def plot_OD(self):
        # is the name of the button which called this method
        sender = self.sender()
        self.well_name = str(sender.text())
        # The try statement prevents an error if the user clicks on a well button without loading the data beforehand. 
        try:
            #Calls the method for plotting derivatives
            self.plot_derivatives(self.well_name)
            # If the user has asked for the same time window for all wells skips to the next part.
            if not self.btn_same_time_window.isChecked():
                self.time, self.data = self.data_object.well_data(self.well_name)
                self.canvas_OD.ax1.cla()
                self.canvas_OD.ax1.plot(self.time, self.data)
                # The try statement prevents an error if the user clicks on a well button. 
                # Without it the selected time window will not be plotted if the well is not present in self.dict_time_window
                try:
                    self.canvas_OD.ax1.plot(self.time[self.dict_time_window[self.well_name][0]:self.dict_time_window[self.well_name][1]], 
                                            self.data[self.dict_time_window[self.well_name][0]:self.dict_time_window[self.well_name][1]], 'r')
                except KeyError:
                    pass
                self.canvas_OD.draw()
            else:
                self.time, self.data = self.data_object.well_data(self.well_name)
                self.canvas_OD.ax1.cla()
                self.canvas_OD.ax1.plot(self.time, self.data)
                self.canvas_OD.ax1.plot(self.time[self.same_time_window[0]:self.same_time_window[1]], self.data[self.same_time_window[0]:self.same_time_window[1]], 'r')
                self.canvas_OD.draw()
        except AttributeError:
            self.error_msg_no_data.exec_()
            
    # The method to plot the derivatives of OD and select a time window       
    def plot_derivatives(self,well_name):
        self.time, self.data = self.data_object.well_data(well_name)
        self.fit = UnivariateSpline(self.time, self.data, k=5, s= 0.005)
        self.fit1d = self.fit.derivative(n = 1)
        self.fit2d = self.fit.derivative(n = 2)
        self.canvas_derivative.time = self.time
        self.canvas_derivative.first_derivative = self.fit1d(self.time)/np.max(self.fit1d(self.time))
        self.canvas_derivative.second_derivative = self.fit2d(self.time)/np.max(self.fit2d(self.time))
        self.canvas_derivative.ax1.cla()
        self.canvas_derivative.ax1.plot(self.canvas_derivative.time ,  self.canvas_derivative.first_derivative)
        self.canvas_derivative.ax1.plot(self.canvas_derivative.time ,  self.canvas_derivative.second_derivative)
        self.canvas_derivative.draw()

    # The slot called by a button to update the dictionary containing the selected time windows
    def update_time_window(self):  
        try:
            self.min_index = self.canvas_derivative.min_index
            self.max_index = self.canvas_derivative.max_index
        except AttributeError:
            self.min_index = 0
            self.max_index = len(self.time)
        # self.wells_panel.radio_buttons is a dictionary containing the buttons associated to each well
        for key in self.wells_panel.radio_buttons:
            value_temp = self.wells_panel.radio_buttons[key]
            #If a well is selected updates the dictionary of time windows and plot the selected part on the OD_canvas in red
            if value_temp.isChecked():
                self.dict_time_window[value_temp.text()] = [self.min_index, self.max_index]
                self.well_name = key
                self.time, self.data = self.data_object.well_data(self.well_name)
                self.canvas_OD.ax1.cla()
                self.canvas_OD.ax1.plot(self.time, self.data)
                self.canvas_OD.ax1.plot(self.time[self.min_index:self.max_index], self.data[self.min_index:self.max_index], 'r')
                self.canvas_OD.draw()
    # The slot if the user chooses to have the same time window for all wells. The method takes the last element of the self.dict_time_window and uses it
    # as the shared time window
    def set_same_time_window(self):
        #If the dictinary is emty that is no time window is selected gives an error message
        if len(list(self.dict_time_window.keys())) == 0:
            self.error_message.exec_()
            self.btn_same_time_window.setChecked(False)
        else:
            key_temp = list(self.dict_time_window.keys())[-1]
            self.same_time_window = self.dict_time_window[key_temp]
    # A method to get the data after pushing the brows buttons.      
    def get_data(self):
        self.data_object = self.fit_panel.data_object
    # The slot after selecting the button to run the fit process       
    def run_fit(self):
        #The model for exponential growth. There are three parameters, amp is the amplitude, rate the rate of 
        # growth multiplied by log(2) to convert it to doubling rate, and the bg as the background
        def model(taxis, amp, rate, bg):
            return amp*np.exp(taxis*rate*np.log(2)) + bg
        self.result_fit = {}
        # If the use has not asked for the same time window for all the wells proceeds
        if not self.btn_same_time_window.isChecked():
            for key in self.dict_time_window:
                self.time_fit, self.data_fit = self.data_object.well_data(key)
                self.min_index_temp = self.dict_time_window[key][0]
                self.max_index_temp = self.dict_time_window[key][1]
                self.time_fit = self.time_fit[self.min_index:self.max_index_temp]
                self.data_fit = self.data_fit[self.min_index:self.max_index_temp]

                #Initial geuss
                self.popt_temp, self.pcov_temp = curve_fit(model, self.time_fit, self.data_fit, p0 = [0.001, 1/90, 0.098], maxfev = 8000)
                self.popt_temp = [self.popt_temp[0],1/self.popt_temp[1],self.popt_temp[2]]
                self.result_fit[key] = self.popt_temp
        else:
            for letter in self.alphabet:
                for number in range(1,13):
                    key_temp = f'{letter}{number}'
                    self.time_fit, self.data_fit = self.data_object.well_data(key_temp)
                    self.min_index_temp = self.same_time_window[0]
                    self.max_index_temp = self.same_time_window[1]
                    self.time_fit = self.time_fit[self.min_index:self.max_index_temp]
                    self.data_fit = self.data_fit[self.min_index:self.max_index_temp]
                    #Initial geuss
                    try:
                        self.popt_temp, self.pcov_temp = curve_fit(model, self.time_fit, self.data_fit, p0 = [0.001, 1/90, 0.098], maxfev = 8000)
                        self.popt_temp = [self.popt_temp[0],1/self.popt_temp[1],self.popt_temp[2]]
                        self.result_fit[key_temp] = round(self.popt_temp[1],1)
                    except RuntimeError:
                        pass
         
        self.text_file_name = str(datetime.datetime.now()) 
        self.text_file_name = self.text_file_name[0:-7] 
        self.text_file_name = self.text_file_name.replace(':', '-')
        with open(f'fitting_results  {self.text_file_name}.txt','w') as text_file:
            text_file.write('The doubling times are in minutes\n')
            for key in self.result_fit:
                text_file.writelines(f'{key}:{self.result_fit[key]}\n')
        self.done_message.exec_()