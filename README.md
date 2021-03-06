# Introduction
This is a GUI made using PyQt5 to calculate the doubling time of yeast while they grow exponentially. 
You must have PyQt5, Numpy, Scipy, Matplotlib, openpyxl, and Pandas installed to use this GUI. To run the GUI, execute the code in the `main.py`file.
The GUI reads the xlsx files exported by Biotek Gen5 software.
If you modify the code in Data.py, you can use xlsx files formatted in a different way.

![Screenshot of the GUI](https://github.com/Reza31415/Growth-Rate-Analysis/blob/main/Docs/Screenshots/Main%20Window2.png)

# Model
The GUI fits the selected part of the growth curve to `amp*2^(k*t) + bg` in which the *amp* is the amplitude, the *k* is the doubling time, and the *bg* is the background level noise.
# Usage
## Loading the file
By clicking on the **Import Data** button a dialogue will appear in the directory in which the Python files are located, then you can find the xlsx file.
## Initial Calculations
After loading the file, the GUI calculates the time window during which the growth rate is exponential. It detects this region by:

1- First fitting the growth rate with spline of degree five to get a smooth curve.

2- Calculating the second derivative of growth rate. When the growth stops being exponential the second derivative reaches its maximum. A time window is chosen begining from zero till the time at which the second derivative reaches its maximum.
## Elements of GUI
### Plot of the growth curve
After initial calculation of the desired time window, on the left hand side of the screen the plot of the growth curve is seen. On the bottom of this plot you see an array of buttons. Upon clicking on them, the data associated with the selected well is displayed.
### The Tabs: plot of derivatives
On the right hand side of the screen, five tabs appear. You can reorder the tabs if desired by dragging them to left or right.
The first tab show the normalized first and second derivative of the growth rate and the fitted spline curve to the growth curve. On the top plot you can select a time window and then by pressing **Update the time window for current selection** someone can change the default calculated time window for the current window. If someone chooses to press **Use the same time window for all** then the chosen time window will be used for all other wells too.
By clicking the **Reset time windows** on the panel on right, the time windows reset to the default calculated ones. If someone is not happy with the smoothness of the second derivative, then can use the *slider* on the right to achieve a smoother curve to find where the second derivative reaches its maximum. 
### The Tabs: Doubling times.
The first table is a template to name each single well. This name could be the name of the strain in that well. After fitting, a new table will appear in which the stattistics of the doubling time for wells sharing the same name is shown.
After pressing **Start fit** button, the doubling times are shown here in minutes in the table below the template. The average and standard deviations of each column or row is also displayed. Each time the **Start fit** is pressed the doubling times are also saved on disk.
### The Tabs: Plot of temperature
This tab plots the measured temperature in celcius.
### The Tabs: Multiple plots
Here someone may choose to plot multiple growth curves by selecting the corresponding well. It is also possible to plot a whole row or column. Pressing **Deselect all** deselect the chosen wells and clear the plot.
### The Tabs: Final OD
This tab displays the avearge of the last five points as the final optical density of the growth curve. The average and standard deviation of each row and column is also displayed.



