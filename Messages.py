# -*- coding: utf-8 -*-
"""
Created on Fri May  7 22:40:33 2021

@author: Reza-G510
"""
from PyQt5 import QtWidgets

class Messages():
    def __init__(self):
        
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