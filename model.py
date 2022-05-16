from matplotlib import pyplot
import json 
import math
import numpy as np
import seaborn as sns
import warnings
from tabulate import tabulate
from contextlib import redirect_stdout

warnings.filterwarnings("ignore")

ROUNDING = 2
ROUNDING_FORMAT = '.3f'
RESOURCES = 'resources/'
GRAPH_PATH = RESOURCES + 'graphs/'
DATA_PATH = RESOURCES + 'data/'
TABLES_PATH = RESOURCES + 'tables/'

def determine_class_amount(data_set):
    return math.trunc(1+  math.log(len(data_set), 2)) 

def determine_class_size(data_set, number_classes, min, max):
    range = max - min
    return round(range/number_classes, ROUNDING)

def get_median(data_set):
    lenght = len(data_set)

    middle = int(math.trunc(lenght/2))

    if lenght == 0:
        return lenght
    if lenght % 2 == 0:
        return (data_set[middle] + data_set[middle - 1]) / 2
    else:
        return data_set[middle]

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

def create_tables(data_set, name, file_name):
    with open(TABLES_PATH + file_name, 'w') as f:
        with redirect_stdout(f):
            print(name + '\n')
            data_set.sort()
            max_value = float(max(data_set))
            min_value = float(min(data_set))
            number_classes = determine_class_amount(data_set)
            class_size = determine_class_size(data_set, number_classes, min_value, max_value)

            entries = []
            headers = [
                'Classes',
                'Frequência',
                'F-Relativa',
                'Media',
                'Mediana',
                'Moda',
                "Variância",
                "Desvio Padrão",
                "Erro Padrão",
                "Coeficiente de Variação",
                '%',
                '% Acumulada']

            freq = []
            accumulated_percentage = 0
            for i in range(number_classes):
                freq.append([])
                inferior = round(min_value + i*class_size, ROUNDING)
                superior = round(inferior + class_size, ROUNDING)
                class_range = (str(format(inferior, ROUNDING_FORMAT)) + "-|" + str(format(superior, ROUNDING_FORMAT)))
                for entry in data_set:
                    if inferior <= float(entry) < superior:
                        freq[i].append(float(entry))
                
                avg = get_average(freq[i])
                variance = variance_sample(freq[i])
                std_deviation = math.sqrt(variance)
                error_estimative = error_estimate(freq[i], std_deviation)

                percentage = len(freq[i])/len(data_set)
                accumulated_percentage += percentage
                entries.append([
                    class_range, # Classes
                    len(freq[i]), # Frequencia
                    round(len(freq[i])/len(data_set), ROUNDING), # Frequência Relativa
                    round(avg, ROUNDING), # Media
                    round(get_median(freq[i]), ROUNDING), # Mediana
                    most_frequent(freq[i]), # Moda
                    round(variance, ROUNDING*2), # Variancia
                    round(std_deviation, ROUNDING*2), # Desvio Padrão
                    round(error_estimative, ROUNDING*2), # Erro Padrão
                    round(coeff_variation(std_deviation, avg), ROUNDING), # Coeficiente de Variação
                    round(percentage, ROUNDING), # Porcentagem
                    round(accumulated_percentage, ROUNDING) # Porcentagem acumulada
                    ])

            print(tabulate(entries, headers=headers, numalign="center", stralign="center"))
            print()
            print(str(class_size) + " tamanho das classes")
            print(str(number_classes) + " numero de classes")    
            print(str(len(data_set)) + " tamanho da amostra\n")

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
    path = GRAPH_PATH + file_name
    pyplot.savefig(path, )

    pyplot.figure().clear()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()

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

save_graph(interior, metropolis, "darkgreen", "dodgerblue", "Interior", "Metrópolis", "SP3 (cidades de N a V) e Paraná - Interior x Metrópolis", "Interior-Metropolis")

save_graph(nacional, outras, "darkgreen", "orange", "Nacionais", "Outras", "SP3 (cidades de N a V) x Paraná - Bandeiras", "Bandeiras")

save_graph(parana, sp3, "limegreen", "red", "Paraná", "São Paulo", "SP3 (cidades de N a V) x Paraná", "SP3-Parana")

create_tables(parana, "Paraná - Preço da GA", "parana.txt")
create_tables(sp3, "SP3 (cidades de N a V) - Preço da GA", "sp3.txt")

create_tables(nacional, "SP3 (cidades de N a V) e Paraná - Bandeiras Nacionais", "bandeiras.txt")
create_tables(outras, "SP3 (cidades de N a V) e Paraná - Outras Bandeiras", "bandeiras.txt")

create_tables(interior, "SP3 (cidades de N a V) e Paraná - Interior", "interior.txt")
create_tables(metropolis, "SP3 (cidades de N a V) e Paraná - Metrópolis", "metropolis.txt")
# pyplot.show()
