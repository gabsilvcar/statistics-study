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

DATA_PATH = RESOURCES + 'data/'

LATEX_PATH = RESOURCES + 'latex/'
DESC_TEX_PATH = LATEX_PATH + 'dsc/'

GRAPH_PATH = RESOURCES + 'graphs/'
BOX_PATH = GRAPH_PATH + 'box/'
DIST_PATH = GRAPH_PATH + 'dis/'
DSCB_PATH = GRAPH_PATH + 'dsc/'

def determine_class_amount(data_set):
    return 1+ round(math.log(len(data_set), 2))

def determine_class_size(number_classes, min, max):
    range = max - min
    return range/number_classes

def save_boxplot(df, x, file_name):
    sns.set_theme(style="whitegrid")

    box_plot = sns.boxplot(data=df, x=x, y="PRE_VENDA", hue="ESTADO")
    add_median_labels(box_plot, ROUNDING_FORMAT)
   
    path = BOX_PATH + file_name
    pyplot.savefig(path, )
    pyplot.figure().clear()

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
    sns.set_theme(style="whitegrid")

    sns.displot(df, x="PRE_VENDA", hue="ESTADO", col=x, kde=True, bins="sturges")

    path = DIST_PATH + file_name
    pyplot.savefig(path, )
    pyplot.figure().clear()

def save_describe(df):
    sp = df[df.ESTADO=='SP']
    pr = df[df.ESTADO == 'PR']

    bandeiras_SP = sp.PRE_VENDA[sp.BANDEIRA == "NACIONAIS"].describe().to_latex() + "\n" + sp.PRE_VENDA[sp.BANDEIRA == "OUTRAS"].describe().to_latex()
    bandeiras_PR = pr.PRE_VENDA[pr.BANDEIRA == "NACIONAIS"].describe().to_latex() + "\n" + pr.PRE_VENDA[pr.BANDEIRA == "OUTRAS"].describe().to_latex()
    save_txt(bandeiras_SP+bandeiras_PR, DESC_TEX_PATH+"Bandeira.tex")

    regioes_SP = sp.PRE_VENDA[sp.REGIÃO == "Interior"].describe().to_latex() + "\n" + sp.PRE_VENDA[sp.REGIÃO == "Metropolitana"].describe().to_latex()
    regioes_PR = pr.PRE_VENDA[pr.REGIÃO == "Interior"].describe().to_latex() + "\n" + pr.PRE_VENDA[pr.REGIÃO == "Metropolitana"].describe().to_latex()
    save_txt(regioes_SP+regioes_PR, DESC_TEX_PATH+"Região.tex")

    estados = sp.PRE_VENDA.describe().to_latex() + "\n" + pr.PRE_VENDA.describe().to_latex()
    save_txt(estados, DESC_TEX_PATH+"Estados.tex")

def save_txt(txt, path):
    f = open(path, "w")
    f.write(txt)
    f.close()

def create_graphs(df, x, file_name):
    save_boxplot(df, x, file_name)
    save_dist(df, x, file_name)

# Dados obtidos em https://preco.anp.gov.br/
# Referentes ao período de 01-05-22 a 07-05-22
df = pds.read_json(DATA_PATH + "anp-data.json")

create_graphs(df, "BANDEIRA", "Bandeira")
create_graphs(df, "REGIÃO", "Região")
create_graphs(df, "ESTADO", "Estados")

save_describe(df)
