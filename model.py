# example of a bimodal data sample
from matplotlib import pyplot
import json 
import math
import numpy as np
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

ROUNDING = 2

def getMin(dataset1, dataset2):
    min_value1 = float(min(dataset1))
    min_value2 = float(min(dataset2))
    return min(min_value1, min_value2)

def getMax(dataset1, dataset2):
    max_value1 = float(max(dataset1))
    max_value2 = float(max(dataset2))
    return max(max_value1, max_value2)

def determine_class_amount(data_set):
    return math.trunc(math.log(len(data_set), 2)) 

def determine_class_size(data_set, number_classes, min, max):
    range = max - min
    return round(range/number_classes, ROUNDING)
    
def create_hist(data_set, color, label):
    max_value = float(max(data_set))
    min_value = float(min(data_set))

    number_classes = determine_class_amount(data_set)
    class_size = determine_class_size(data_set, number_classes, min_value, max_value)

    kwargs = dict(bins=number_classes, color=color, label=label)

    sns.distplot(data_set, **kwargs)

def create_graph(label):
    pyplot.grid(axis='y', alpha=0.75)
    pyplot.xlabel('Valor (em R$)')
    pyplot.ylabel('Frequencia')
    pyplot.title(label)
    pyplot.ylim(0,2)
    pyplot.xlim(5,10)
    pyplot.legend();
    pyplot.xticks(np.arange(5, 10, 0.25))
    manager = pyplot.get_current_fig_manager()
    manager.window.showMaximized()
    fig = pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)

def get_price(set): 
    return set['PRE_VENDA'].replace(",", ".")

def save_graph(dataset1, dataset2, color1, color2, label1, label2, title, file_name):
    create_hist(dataset1, color1, label1) 
    create_hist(dataset2, color2, label2) 

    create_graph(title)
    path = 'resources/' + file_name
    pyplot.savefig(path, )

    pyplot.figure().clear()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()

# Dados obtidos em 
# https://preco.anp.gov.br/
# Referentes aos dados de 01-05-22 a 07-05-22
file = open("anp-data.json")
data = json.load(file)

interior = []
metropolis = []

nacional = []
outras = []

parana = []
sp3 = []

for set in data:

    if set["REGIÃO"] == "Interior":
        interior.append(get_price(set))
    else: 
        metropolis.append(get_price(set))

    if set["BANDEIRA"] == "NACIONAIS":
        nacional.append(get_price(set))
    else:
        outras.append(get_price(set))

    if set["ESTADO"] == "PR":
        parana.append(get_price(set))
    else:
        sp3.append(get_price(set))

interior.sort()
metropolis.sort()
nacional.sort()
outras.sort()
parana.sort()
sp3.sort()

save_graph(interior, metropolis, "darkgreen", "dodgerblue", "Interior", "Metrópolis", "SP3 (cidades de N a V) e Paraná - Interior x Metrópolis", "Interior-Metropolis")

save_graph(nacional, outras, "darkgreen", "orange", "Nacionais", "Outras", "SP3 (cidades de N a V) x Paraná - Bandeiras", "Bandeiras")

save_graph(parana, sp3, "limegreen", "red", "Paraná", "São Paulo", "SP3 (cidades de N a V) x Paraná", "SP3-Parana")


# pyplot.show()
