'''
    Script que gera um histograma da frequencia dos analitos em data.csv. Os 
    campos com valores iguais a 0 são considerados como vazios.
'''

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data.csv')

labels = list(df.columns)
count = [0 for i in range(len(labels))]
for i in range(len(labels)):
    for x in df[labels[i]]:
        count[i] += 1 if x != 0 else 0

print('Total de exames: ' + str(len(labels)))
for i in range(len(labels)):
    print(str(labels[i]) + "= " + str(count[i]))
