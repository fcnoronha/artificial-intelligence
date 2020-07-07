'''
    Script usado para gerar uma instancia reduzida do arquivo 'data.csv'.
'''

FILE = '../data.csv'
N_LINES = 10000

cnt = 0
total = 0

for row in open('../data.csv', 'r').readlines():
    total += 1

f = open('../data_r.csv', 'w+')
for row in open('../data.csv', 'r').readlines():
    if cnt > total - N_LINES or cnt == 0:
        f.write(str(row))   
    cnt += 1
f.close()