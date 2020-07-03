import glob
from ftfy import fix_encoding
source_path='./*.csv'
filenames = glob.glob(source_path)
for filename in filenames:
    if filename[2] == 'f': continue
    print(filename)
    text = open(filename,'r').read()
    f = open(filename.replace('.csv','_fixed.csv'),"a+")
    f.write(fix_encoding(text))
    f.close()