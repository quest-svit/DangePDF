COVID PLOT

Corona Tracker Python App


Covid Plot is a python based App which can plot the counts of Active , Recovered and Death cases due to COVID-19 in the selected country.

It can plot different Plots like - Bar Chart, Pie Chart, Horizontal Bar Chart, Box Plot and Area Plot.

It uses data from Johns Hopkins University CSSE Data at
https://github.com/CSSEGISandData/COVID-19


Python Version:
Python 2.7.17 and Python 3.6.9


How to use?
1. Download the data file from the above github repository for the date you want to plot.
2. Save it in the data folder
3. Edit the name of the file -
    pd.read_csv('../data/corona_Tracker_09-24-2020.csv')
4. Run from the src folder
    python webserver.py
5. Open webbrowser
    http://0.0.0.0:8080/
