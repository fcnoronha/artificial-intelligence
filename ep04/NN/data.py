'''
    Modulo que implementa o pre-processamento basico para que os dados sejam
    ingeridos e aproveitados pela rede. O pre-processamento bruto é realizado
    pelos scripts em /PRE/scripts/.
'''

from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from collections import Counter
import pandas as pd

def load_data(data_path='../PRE/data_r.csv'):
    '''
    Funcao que importa dados de um arquivo csv. Retorna um dataFrame.
    '''
    data = pd.read_csv(data_path)
    return data

def process_data(data, exam_type):
    '''
    Faz o processamento fino dos dados para um determinado exame, isolando a
    coluna de resultados do mesmo para ser usado como y. Além disso, aqui, 
    todos os valores das colunas são normalizadas para o intervalo [0, 1] e 
    linhas com y == 0 (nulo) são excluidas. Finalmente é feito over-sampling
    visando balancear as classes.
    '''
    labels = list(data.columns)
    target_exam = labels[-3+exam_type]
    df = data.copy()

    # removendo linhas com y == 0
    df.drop(df.loc[df[target_exam]==0].index, inplace=True)
    # normalizando valores para [0,1]
    min_max_scaler = MinMaxScaler()
    scaled = min_max_scaler.fit_transform(df.values)
    df = pd.DataFrame(scaled, columns=df.columns)

    # separando dados de entrada em x e resultado-alvo em y
    x = df[labels[:-3]]            
    y = df[target_exam]            

    # over-sampling para equilibrar as classes 
    ros = RandomOverSampler(random_state=0)
    x_resampled, y_resampled = ros.fit_resample(x, y)
    print(sorted(Counter(y_resampled).items()))
    x, y = shuffle(x_resampled, y_resampled, random_state=42)

    return (x, y)

def min_max(df):
    '''
    Captura os valores minimos e maximos de cada coluna do dataset. Esses
    valores serão depois usados para normalizar o input de usuario disponivel
    no modulo use.py.
    '''
    min_max = [[min, max] for min, max in zip(df.min(), df.max())]
    f = open('trained_nn/min_max.csv', 'w+')
    for val in min_max:
        f.write(str(val[0]) + ',' + str(val[1]) + '\n')
    f.close()