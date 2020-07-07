'''
    Script usado para concertar a formatação UTF de arquivos defeituosos.
'''

import glob
from ftfy import fix_encoding

PATH = '../*.csv'

for filename in glob.glob(PATH):
    if 'fleury' in filename: continue
    text = open(filename, 'r').read()
    f = open(filename.replace('.csv', '_fixed.csv'), 'a+')
    f.write(fix_encoding(text))
    f.close()