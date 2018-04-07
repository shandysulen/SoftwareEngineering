# -*- coding: utf-8 -*-
"""
Mouse Graph

@author: Alexandra
"""
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

loc = pd.read_csv('./data/mouseLoc.csv')
clicks = pd.read_csv('./data/mouseClicks.csv')

# g is type Figure, use matplotlib draw() to display
g = sns.kdeplot(loc.x, loc.y, cmap="Oranges", shade=True)
g = plt.scatter(clicks.x, clicks.y, c="w", marker="+")
