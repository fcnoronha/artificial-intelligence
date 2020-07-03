import glob

sets = []
for filename, col in [('./fleury_e.csv', 4), ('./hsl_e.csv', 5)]:
    unique_set = set()

    for row in open(filename, 'r'):
        item = str(row.split(',')[col])
        if col == 5: item = item[1:-1]
        unique_set.add(item)
        
    f = open(filename.replace('_e.csv','_unique_set.csv'), 'w+')
    for x in unique_set:
        f.write(x+'\n')

    f.close()
    sets.append(unique_set)

set_intersection = sets[0].intersection(sets[1])

f = open('all_both_unique.csv', "w+")
for item in set_intersection:
    f.write(item+'\n')
f.close()