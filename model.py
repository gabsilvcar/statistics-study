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

def latex_converter(entries):
    tex = ""
    i = 0
    for entry in entries:
        i += 1
        tex += str(entry)
        if not (i == len(entries)):
            tex += ' & '
        else:
            tex += '\\' + '\\' + '\n'
    return tex 

def save_latex_table(tex_table, file_name, subfolder):
    text_file = open(LATEX_PATH + subfolder + file_name, "w")
    n = text_file.write(tex_table)
    text_file.close()

def create_tables(data_set, name, file_name, descriptive):
    empirical = latex_converter(["Classe", "Frequência", "F-Relativa", "%", "% Acumulada"])
    with open(TABLES_PATH + file_name, 'w') as f:
        with redirect_stdout(f):
            print(name + '\n')
            data_set.sort()
            max_value = float(max(data_set))
            min_value = float(min(data_set))
            number_classes = determine_class_amount(data_set)
            class_size = determine_class_size(data_set, number_classes, min_value, max_value)

            entries_empirical = []
            headers_empirical = [
                'Classes',
                'Frequência',
                'F-Relativa',
                '%',
                '% Acumulada']
            entries_descriptive = []
            headers_descriptive = [
                'Media',
                'Q1',
                'Mediana',
                'Q3',
                'L Inferior',
                'L Superior',
                'Moda',
                "Variância",
                "Desvio Padrão",
                "Erro Padrão",
                "Coeficiente de Variação",
            ]

            freq = []
            accumulated_percentage = 0
            for i in range(number_classes):
                freq.append([])
                inferior = min_value + i*class_size
                if i == number_classes -1:
                    superior = max_value + 0.001
                else:
                    superior = inferior + class_size
                class_range = (str(format(inferior, ROUNDING_FORMAT)) + "|-" + str(format(superior, ROUNDING_FORMAT)))

                for entry in data_set:
                    if inferior <= float(entry) < superior:
                        freq[i].append(float(entry))

                percentage = len(freq[i])/len(data_set)
                accumulated_percentage += percentage
                entries_empirical.append([
                    class_range, # Classes
                    len(freq[i]), # Frequencia
                    round(len(freq[i])/len(data_set), ROUNDING), # Frequência Relativa
                    round(percentage, ROUNDING), # Porcentagem
                    round(accumulated_percentage, ROUNDING) # Porcentagem acumulada
                    ])
                empirical += latex_converter([class_range, len(freq[i]), round(len(freq[i])/len(data_set), ROUNDING), round(percentage, ROUNDING), round(accumulated_percentage, ROUNDING)])
                

            avg = get_average(data_set)
            variance = variance_sample(data_set)
            std_deviation = math.sqrt(variance)
            error_estimative = error_estimate(data_set, std_deviation)
            q1 = get_Qx(data_set,1)
            q3 = get_Qx(data_set,3)
            alc_q1_q3 = (q3 - q1)
            built_descriptive_entries = [
                    round(avg, ROUNDING), # Media
                    round(get_Qx(data_set,1), ROUNDING), #Q1
                    round(q1, ROUNDING), # Mediana
                    round(q3, ROUNDING), #Q3
                    round(q1 - 1.5*alc_q1_q3, ROUNDING), #LimiteInferior
                    round(q3 + 1.5*alc_q1_q3, ROUNDING), #LimiteSuperior
                    most_frequent(data_set), # Moda
                    round(variance, ROUNDING), # Variancia
                    round(std_deviation, ROUNDING), # Desvio Padrão
                    round(error_estimative, ROUNDING), # Erro Padrão
                    round(coeff_variation(std_deviation, avg), ROUNDING), # Coeficiente de Variação
            ]

            built_descriptive = [
                    file_name.replace(".txt", ""),
                    round(avg, ROUNDING), # Media
                    round(get_median(data_set), ROUNDING), # Mediana
                    most_frequent(data_set), # Moda
                    round(variance, ROUNDING), # Variancia
                    round(std_deviation, ROUNDING), # Desvio Padrão
                    round(error_estimative, ROUNDING), # Erro Padrão
                    round(coeff_variation(std_deviation, avg), ROUNDING), # Coeficiente de Variação
            ]

            entries_descriptive.append(built_descriptive_entries)
            descriptive += latex_converter(built_descriptive)

            print(tabulate(entries_empirical, headers=headers_empirical, numalign="center", stralign="center"))
            print()
            print(str(round(class_size, ROUNDING)) + " tamanho das classes")
            print(str(number_classes) + " numero de classes")    
            print(str(len(data_set)) + " tamanho da amostra\n")
            print(tabulate(entries_descriptive, headers=headers_descriptive, numalign="center", stralign="center"))

            save_latex_table(empirical, file_name, "empirical/")

            return descriptive



def create_hist(data_set, color, label):
    kwargs = dict(bins=determine_class_amount(data_set), color=color, label=label)

    sns.distplot(data_set, **kwargs)

def create_graph(label):
    pyplot.grid(axis='y', alpha=0.75)
    pyplot.xlabel('Valor (em R$)')
    pyplot.ylabel('Frequencia')
    pyplot.title(label)
    pyplot.ylim(0,2)
    pyplot.xlim(5,10)
    pyplot.legend();
    pyplot.xticks(np.arange(5, 10, 0.5))
    manager = pyplot.get_current_fig_manager()
    manager.window.showMaximized()
    # fig = pyplot.gcf()
    # fig.set_size_inches(18.5, 10.5)

def get_price(set): 
    return float(set['PRE_VENDA'].replace(",", "."))

def save_histogram(dataset1, dataset2, color1, color2, label1, label2, title, file_name):
    create_hist(dataset1, color1, label1) 
    create_hist(dataset2, color2, label2) 

    create_graph(title)
    path = GRAPH_PATH + file_name
    pyplot.savefig(path, )

    pyplot.figure().clear()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()

def save_boxplot(dataset1, dataset2, color1, color2, label1, label2, title, file_name):

        data = {
        label1: dataset1,
        label2: dataset2
        }
        df = pds.concat([pds.DataFrame(v, columns=[k]) for k, v in data.items()], axis=1)


        
    

        sns.set_theme(style="whitegrid")

        box_plot = sns.boxplot(data=df

        )
        add_median_labels(box_plot, ROUNDING_FORMAT)
        path = GRAPH_PATH + "box/" +file_name

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
def create_boxplot(data_set, color, label):

    sns.boxplot(data_set)

# Dados obtidos em 
# https://preco.anp.gov.br/
# Referentes aos dados de 01-05-22 a 07-05-22
file = open(DATA_PATH + "anp-data.json")
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

save_histogram(interior, metropolis, "darkgreen", "dodgerblue", "Interior", "Metrópolis", "SP3 (cidades de N a V) e Paraná - Interior x Metrópolis", "Interior-Metropolis")

save_histogram(nacional, outras, "darkgreen", "orange", "Nacionais", "Outras", "SP3 (cidades de N a V) x Paraná - Bandeiras", "Bandeiras")

save_histogram(parana, sp3, "limegreen", "red", "Paraná", "São Paulo", "SP3 (cidades de N a V) x Paraná", "SP3-Parana")

descriptive = latex_converter(["Dados", "Média", "Mediana", "Moda", "Variância", "Desvio Padrão", "Erro Padrão", "Coef. Variação"])


descriptive = create_tables(parana, "Paraná - Preço da GA", "parana.txt", descriptive)
descriptive = create_tables(sp3, "SP3 (cidades de N a V) - Preço da GA", "sp3.txt", descriptive)

descriptive = create_tables(nacional, "SP3 (cidades de N a V) e Paraná - Bandeiras Nacionais", "bandeiras-nacionais.txt", descriptive)
descriptive = create_tables(outras, "SP3 (cidades de N a V) e Paraná - Outras Bandeiras", "outras-bandeiras.txt",descriptive)

descriptive = create_tables(interior, "SP3 (cidades de N a V) e Paraná - Interior", "interior.txt", descriptive)
descriptive = create_tables(metropolis, "SP3 (cidades de N a V) e Paraná - Metrópolis", "metropolis.txt", descriptive)
# pyplot.show()
descriptive = save_latex_table(descriptive, "descriptive", "descriptive/")

save_boxplot(interior, metropolis, "darkgreen", "dodgerblue", "Interior", "Metrópolis", "SP3 (cidades de N a V) e Paraná - Interior x Metrópolis", "Interior-Metropolis")

save_boxplot(nacional, outras, "darkgreen", "orange", "Nacionais", "Outras", "SP3 (cidades de N a V) x Paraná - Bandeiras", "Bandeiras")

save_boxplot(parana, sp3, "limegreen", "red", "Paraná", "São Paulo", "SP3 (cidades de N a V) x Paraná", "SP3-Parana")

