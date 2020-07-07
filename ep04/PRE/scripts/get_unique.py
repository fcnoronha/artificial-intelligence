'''
    Script que pega a interseção dos itens distintos da coluna 'DE_ANALITO'
    da base de dados do Fleury e o HSL. O resultado é armazenado no arquivo
    'used_analitos.csv'.
'''

import glob

sets = []
for filename, col in [('../fleury_e.csv', 4), ('../hsl_e.csv', 5)]:
    unique_set = set()

    for row in open(filename, 'r'):
        item = str(row.split(',')[col])
        if col == 5: item = item[1:-1]
        unique_set.add(item)

    f.close()
    sets.append(unique_set)

set_intersection = sets[0].intersection(sets[1])
f = open('../used_analitos.csv', "w+")
for item in set_intersection:
    f.write(item+'\n')
f.close()