# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:23:21 2021

@author: rchoubeh
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10,100)

y = np.sin(x)
z = np.cos(x)

fig = plt.figure()
ax = fig.add_subplot(111)
a = ax.plot(x,y, label = 'sin')
ax.plot(x,z, label = 'cos')

handles, labels = ax.get_legend_handles_labels()

print(handles)

print(a)

print(labels)