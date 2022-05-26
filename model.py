import random
from matplotlib import pyplot
import json 
import math
import numpy as np
import seaborn as sns
import warnings
from tabulate import tabulate
from contextlib import redirect_stdout
import pandas as pds
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

ROUNDING = 3
ROUNDING_FORMAT = '.3f'

RESOURCES = 'resources/'
GRAPH_PATH = RESOURCES + 'graphs/'
DATA_PATH = RESOURCES + 'data/'
TABLES_PATH = RESOURCES + 'tables/'
LATEX_PATH = RESOURCES + 'latex/'
BOX_PATH = GRAPH_PATH + 'box/'
DIST_PATH = GRAPH_PATH + 'dist/'

def determine_class_amount(data_set):
    return 1+ round(math.log(len(data_set), 2))

def determine_class_size(data_set, number_classes, min, max):
    range = max - min
    return range/number_classes

def get_median(data_set):
    lenght = len(data_set)

    middle = int(math.trunc(lenght/2))

    if lenght == 0:
        return lenght
    if lenght % 2 == 0:
        return (data_set[middle] + data_set[middle - 1]) / 2
    else:
        return data_set[middle]

def get_Qx(data_set, x):
    lenght = len(data_set)

    qx = int(math.trunc(x*lenght/4))

    if lenght == 0:
        return lenght
    if lenght % 2 == 0:
        return (data_set[qx] + data_set[qx - 1]) / 2
    else:
        return data_set[qx]


def get_average(list):
    if len(list) == 0: return 0
    return sum(list)/len(list)

def most_frequent(List):
    dict = {}
    count, itm = 0, ''
    for item in reversed(List):
        dict[item] = dict.get(item, 0) + 1
        if dict[item] >= count :
            count, itm = dict[item], item
    return(itm)
 
def variance_sample(list):
    n = len(list)
    if n <= 1:
        return 0
    avg = get_average(list)
    sigma = 0
    for value in list:
        sigma += (avg - value) ** 2
    return (sigma/(n-1))

def variance_population(list):
    n = len(list)
    if n <= 1:
        return 0
    avg = get_average(list)
    sigma = 0
    for value in list:
        sigma += (avg - value) ** 2
    return (sigma/n)

def error_estimate(list, std_deviation):
    n = len(list)
    if n <= 1:
        return 0
    return std_deviation/math.sqrt(n)

def coeff_variation(std_deviation, avg):
    if (avg == 0): return 0
    return std_deviation/avg * 100

def save_boxplot(df, x, file_name):
    sns.set_theme(style="whitegrid")

    box_plot = sns.boxplot(data=df, x=x, y="PRE_VENDA", hue="ESTADO")
    add_median_labels(box_plot, ROUNDING_FORMAT)
   
    path = BOX_PATH + file_name
    pyplot.savefig(path, )
    pyplot.figure().clear()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()

def add_median_labels(ax, fmt='.1f'):
    lines = ax.get_lines()
    boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
    lines_per_box = int(len(lines) / len(boxes))
    for median in lines[4:len(lines):lines_per_box]:
        x, y = (data.mean() for data in median.get_data())
        # choose value depending on horizontal or vertical plot orientation
        value = x if (median.get_xdata()[1] - median.get_xdata()[0]) == 0 else y
        text = ax.text(x, y, f'{value:{fmt}}', ha='center', va='center',
                       fontweight='bold', color='white')
        # create median-colored border around white text for contrast
        text.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground=median.get_color()),
            path_effects.Normal(),
        ])

def save_dist(df, x, file_name):
    # sns.set_theme(style="whitegrid")

    sns.displot(df, x="PRE_VENDA", hue="ESTADO", col=x)
   
    path = DIST_PATH + file_name
    pyplot.savefig(path, )
    pyplot.figure().clear()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()

def create_graphs(df, x, file_name):
    save_boxplot(df, x, file_name)
    save_dist(df, x, file_name)

# Dados obtidos em 
# https://preco.anp.gov.br/
# Referentes aos dados de 01-05-22 a 07-05-22
# file = open(DATA_PATH + "anp-data.json")
# data = json.load(file)

df = pds.read_json(DATA_PATH + "anp-data.json")

create_graphs(df, "BANDEIRA", "Bandeira")
create_graphs(df, "REGIÃO", "Região")
create_graphs(df, "ESTADO", "Estados")
