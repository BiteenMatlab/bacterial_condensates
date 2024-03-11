# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 17:50:10 2023

@author: azaldegc
"""

import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np
import pandas as pd
import sys
import scipy.stats as ss


def filepull(directory):
    '''Finds images files in directory and returns them'''
    # create list of image files in directory
    filenames = [img for img in glob.glob(directory)]   
    
    return filenames


directory = sys.argv[1]
filenames = filepull(directory)
font_size = 15
dfs = []
samples= ['cI_agg', 'PopTag_SL', 'PopTag_LL', 'McdB', 'McdB_FL', 'mCherry']
colors = ['royalblue', 'darkgreen', 'darkorange', 'purple', 'gold', 'gray']

for file in filenames:
    
    df = pd.read_csv(file,index_col=None)
    dfs.append(df)
 
all_data = pd.concat(dfs)
all_data = all_data.reset_index()



fig, axes = plt.subplots(figsize=(4.5,3))

for jj, sample in enumerate(samples):
    
    sample_data = all_data[all_data['Label']==sample]
    out_data = []
    print(sample)
    if sample!= 'McdB_FL':                                                                                      
        for rep in range(3):
            rep_data = sample_data[sample_data['Replicate']==rep+1]
            percent_cells_focus = []
            for ii in range(6):
                timepoint_data = rep_data[rep_data['Time']==ii]
            
                n_cells_focus = len(timepoint_data[timepoint_data['Focus']>0].to_numpy())
                print(n_cells_focus, len(timepoint_data))
                percent_cells_focus.append((n_cells_focus / len(timepoint_data))*100)
           
            out_data.append(np.asarray(percent_cells_focus))
            print(percent_cells_focus, len(timepoint_data))
    if sample== 'McdB_FL':                                                                                      
        for rep in range(2):
            rep_data = sample_data[sample_data['Replicate']==rep+1]
            percent_cells_focus = []
            for ii in range(6):
                timepoint_data = rep_data[rep_data['Time']==ii]
            
                n_cells_focus = len(timepoint_data[timepoint_data['Focus']>0].to_numpy())
                print(n_cells_focus, len(timepoint_data))
                percent_cells_focus.append((n_cells_focus / len(timepoint_data))*100)
           
            out_data.append(np.asarray(percent_cells_focus))
            print(percent_cells_focus, len(timepoint_data))
        
    mean_tp = np.mean(np.array(out_data),0)
    stdev_tp = np.std(np.array(out_data),0)
    x=[0,1,2,3,4,5]
    axes.plot(x, mean_tp, color=colors[jj], linewidth=3)
    axes.fill_between(x,mean_tp - stdev_tp, mean_tp + stdev_tp, alpha=0.20, 
                         linewidth=1,color=colors[jj])
    print()
axes.set_xlim(0, 5)
axes.set_xlabel('Time (h)', fontsize=font_size)
axes.set_ylabel('Cells with a fluorescent focus (%)', fontsize=font_size)
axes.tick_params(axis='x',labelsize=font_size)
axes.tick_params(axis='y',labelsize=font_size)
fig.tight_layout()
plt.savefig(directory[:-5] + 'time_series.png', dpi=300)
plt.show()
    
    
        