'''
    Script que realiza experimentos com modelos de redes neurais
    usando k-fold stratified cross validation.
'''

from data import load_data, process_data, min_max
from model import NN1, NN2, NN3
from train import train_network

from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
import numpy as np
import torch, time

LEARNING_RATE = 0.001
MODEL_PATH = ['./trained_nn/igG.pt', 
              './trained_nn/igM.pt',
              './trained_nn/PCR.pt']

# modelos disponiveis de redes
NN = [0, 1, 2]

def create_fold(x, y, train, val):
    '''
    Recebe o conjunto inteiro na forma de x e y e os indices dos elementos que
    serão usados como conjunto de treinamento e validação. Retorna o conjunto
    de treinamento e validação de um fold.
    '''
    x_train_f, y_train_f = x[train], y[train]
    x_val_f, y_val_f = x[val], y[val]

    x_train_f = torch.from_numpy(x_train_f).float()
    y_train_f = torch.squeeze(torch.from_numpy(y_train_f).float())
    x_val_f = torch.from_numpy(x_val_f).float()
    y_val_f = torch.squeeze(torch.from_numpy(y_val_f).float())

    return (x_train_f, y_train_f, x_val_f, y_val_f)


def make_kfold():
    '''
    Faz para cada um dos tres exames e para cada um dos tres modelos de rede
    neural o treinalmento usando stratified k-fold cross validation. Retorna 
    uma matriz 3D que contem para cada cambinacao de exame e rede uma lista 
    com quatro valores: acuracia e loss no conjunto de treinamento e no de
    validacao.
    '''
    raw_data = load_data()
    n_folds = 5

    resultado = np.zeros((3, 3, 4)) # [tr_lss,tr_acc, vl_lss,vl_acc]
    for exam_type, name in [(0,'IGG'), (1,'IGM'), (2,'PCR')]:
        print('\n-------------------------------------------')
        print('----------- Rede para ' + name + '------------------')
        print('-------------------------------------------\n')

        x, y = process_data(raw_data, exam_type)
        x = x.to_numpy()
        y = y.to_numpy()

        skf = StratifiedKFold(n_splits=n_folds)
        fold_iter = 1
        for train, val in skf.split(x, y):
            # cada iteracao é um novo fold
            # (x_train_f, y_train_f, x_val_f, y_val_f)
            fold_data = create_fold(x,y,train,val) 
            for model_n in NN:
                # cada iteracao testa um modelo
                if model_n == 0:   network = NN1(fold_data[0].shape[1])
                elif model_n == 1: network = NN2(fold_data[0].shape[1])
                else:              network = NN3(fold_data[0].shape[1])
                
                optimizer = torch.optim.Adam(network.parameters(), lr=LEARNING_RATE)
                criterion = torch.nn.BCELoss()
                valores = train_network(fold_data, network, optimizer, \
                                        criterion, MODEL_PATH[exam_type])
                resultado[exam_type][model_n] = np.sum([resultado[exam_type][model_n], \
                                                np.asarray(valores)], axis=0)

                print("Fold[{0}] model[{1}] accuracy on validation {2:.2f}% and train {3:.2f}%"\
                        .format(fold_iter, model_n+1, valores[3]*100, valores[1]*100))
            fold_iter += 1

    return np.divide(resultado, n_folds)

def plot(data):
    '''
    Cria uma tabela mostrando a acuracia media de cada modelo de rede em cada 
    exame. A imagem é salva em `trained_nn/accuracy_table.png`. 
    '''
    fig, ax = plt.subplots(figsize=(13, 2))

    plot_data = [[], [], []]
    for model in [0, 1, 2]:
        m_lst = ['Modelo NN' + str(model + 1)]
        for exam in [0, 1, 2]:
            aux = data[exam][model]
            msg = "Validation {0:.2f}% Train {1:.2f}%".format(aux[3]*100, aux[1]*100)
            m_lst.append(msg)
        plot_data[model] = m_lst
    
    table = plt.table(cellText=plot_data, colLabels=['-', 'igG', 'igM', 'PCR'],\
                                                loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    plt.title("Acuracia média entre rede para cada exame e um modelo")
    plt.axis('off')
    plt.savefig('trained_nn/accuracy_table.png')
    plt.close()

if __name__ == '__main__':

    start = time.time()
    print('\n--- INICIANDO TESTES K-FOLD CROSS VALIDATION\n')
    results = make_kfold()
    
    print('\n--- CRIANDO TABELA\n')
    plot(results)
    
    end = time.time()
    print('\nTempo gasto: %.2fs'%(end-start))
    print('\n--- FIM\n\n')