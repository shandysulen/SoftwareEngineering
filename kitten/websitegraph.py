# -*- coding: utf-8 -*-
"""
Website Graph

@author: Alexandra
"""
from matplotlib import cm
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# websites = pd.read_csv('./Websites.csv')

# example data, real data read in from csv
websites = 'Facebook', 'Reddit', 'Canvas', 'GitHub',
time = [12,11,3,30]

cmap=matplotlib.cm.Oranges(np.arange(0.2,1,.1))
my_circle=plt.Circle( (0,0), 0.7, color='white')
plt.pie(time, labels=websites, colors=cmap)
g=plt.gcf()   # Return current figure object
g.gca().add_artist(my_circle)
