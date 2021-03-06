import pandas as pd
import gzip
from pandas import DataFrame
from scipy.stats import uniform
from scipy.stats import randint
import numpy as np
import matplotlib.pyplot as plt
import pylab 
import scipy.stats as stats

def combine(source_one,source_two,source_three,source_four,source_five,metal):
    source_one = source_one[source_one['p_value'] <= 0.05]
    source_two = source_two[source_two['p_value'] <= 0.05]
    source_three = source_three[source_three['p_value'] <= 0.05]
    source_four = source_four[source_four['p_value'] <= 0.05]
    source_five = source_five[source_five['p_value'] <= 0.05]
    source_one = source_one[source_one['p_value'] <= 0.05]
    source_two = source_two[source_two['p_value'] <= 0.05]
    source_three = source_three[source_three['p_value'] <= 0.05]
    source_four = source_four[source_four['p_value'] <= 0.05]
    source_five = source_five[source_five['p_value'] <= 0.05]
    frames = [source_one,source_two,source_three,source_four,source_five]
    all_sources = pd.concat(frames)
    all_sources.rename(columns={'variant_id':'MarkerName'}, inplace=True)
    metal = metal[metal['P-value'] <= 0.05]
    metal = pd.merge(metal, all_sources, on='MarkerName', how='left')
    return metal 

    
def create_histogram(source,nbins):
    ax = source['p_value'].hist(bins=nbins)
    ax.figure.savefig('histogram.png')
    return ax



def manhattan_plot(source, height):
    plot_one = source[['p_value','chromosome']]
    plot_one['minuslog10pvalue'] = -np.log10(plot_one.p_value)
    plot_one.chromosome = plot_one.chromosome.astype('category')
    plot_one = plot_one.sort_values('chromosome')
    plot_one['ind'] = range(len(plot_one))
    plot_one_grouped = plot_one.groupby(('chromosome'))
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(111)
    colors = ['red','green','blue', 'yellow']
    x_labels = []
    x_labels_pos = []
    for num, (name, group) in enumerate(plot_one_grouped):
        group.plot(kind='scatter', x='ind', y='minuslog10pvalue',color=colors[num % len(colors)], ax=ax)
        x_labels.append(name)
        x_labels_pos.append((group['ind'].iloc[-1] - (group['ind'].iloc[-1] - group['ind'].iloc[0])/2))
    ax.set_xticks(x_labels_pos)
    ax.set_xticklabels(x_labels)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    ax.set_xlim([0, len(plot_one)])
    ax.set_ylim([0, height])
    ax.set_xlabel('Chromosome')
    ax.axhline(y=0.002,xmin=0,xmax=3,c="blue",linewidth=0.5,zorder=0)
    plt.savefig('manhattan.png')
    return 



def qq_plot(metal):
    metal.sort_values(by=['P-value'],inplace=True)
    metal['minuslog10pvalue'] = -np.log10(metal['P-value'])
    measurements = np.random.uniform()   
    fig = stats.probplot(metal['minuslog10pvalue'], dist="norm", plot=pylab)
    pylab.savefig('qq.png')
    pylab.show()
    return 


