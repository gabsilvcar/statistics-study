import json 
import math
from tabulate import tabulate

ROUNDING = 3
ROUNDING_FORMAT = '.3f'

def determine_class_amount(data_set):
    return math.trunc(1+  math.log(len(data_set), 2)) 

def determine_class_size(data_set, number_classes, min, max):
    range = max - min
    return round(range/number_classes, ROUNDING)

def get_median(data_set):
    lenght = len(data_set)

    middle = int(math.trunc(lenght/2))

    if lenght % 2 == 0:
        return round((data_set[middle] + data_set[middle - 1]) / 2, ROUNDING)
    else:
        return round(data_set[middle], ROUNDING)

def create(data_set):
    print()
    data_set.sort()
    max_value = float(max(data_set))
    min_value = float(min(data_set))
    number_classes = determine_class_amount(data_set)
    class_size = determine_class_size(data_set, number_classes, min_value, max_value)

    entries = []
    headers = ['Classes', 'Frequência', 'F-Relativa', 'Mediana', '%', '% Acumulada']


    freq = []
    accumulated_percentage = 0
    for i in range(number_classes):
    # print(tabulate([['Alice', 24], ['Bob', 19]], headers=['Name', 'Age']))
        freq.append([])
        inferior = round(min_value + i*class_size, ROUNDING)
        superior = round(inferior + class_size, ROUNDING)
        class_range = (str(format(inferior, ROUNDING_FORMAT)) + "-|" + str(format(superior, ROUNDING_FORMAT)))
        for entry in data_set:
            if inferior <= float(entry) < superior:
                freq[i].append(float(entry))

        percentage = len(freq[i])/len(data_set)
        accumulated_percentage += percentage
        entries.append([class_range, len(freq[i]), round(len(freq[i])/len(data_set), ROUNDING), get_median(freq[i]), round(percentage, ROUNDING), round(accumulated_percentage, ROUNDING)])

    print(tabulate(entries, headers=headers, numalign="center", stralign="center"))
    print()
    print(str(class_size) + " tamanho das classes")
    print(str(number_classes) + " numero de classes")    
    print(str(len(data_set)) + " tamanho da amostra\n")

# 258 tamanho da amostra

def get_price(set): 
    return set['PRE_VENDA'].replace(",", ".")

file = open("anp-data.json")
data = json.load(file)

parana = []
sp3 = []

for set in data:
    if set["ESTADO"] == "PR":
        parana.append(get_price(set))
    else:
        sp3.append(get_price(set))

create(parana)


