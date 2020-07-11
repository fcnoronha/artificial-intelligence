'''
    Função que implementa o uso pratico da rede neural já treinada.
    Este modulo pode ser usado separadamente dos outros. Para isso, 
    basta digitar no terminal '$ python3 use.py' e, em seguida, os
    resultados dos exames do paciente (incluindo PCR, igG e igM) na
    ordem descrita em PRE/used_analitos.csv. 
    Pode-se tambem passar o imput por um arquivo .txt que seja uma 
    linha contendo todos os resultados dos exames separados por '/'.
    Para usa-lo desta maneira basta digitar '$ python3 use.py < a.txt'
    onde a.txt contem o input.
'''

import torch

MODEL_PATH = ['./trained_nn/igG.pt', 
              './trained_nn/igM.pt',
              './trained_nn/PCR.pt']
name = ['igG', 'igM', 'PCR']

def predictor(network, device, features):
    '''
    Faz a predição de um resultado utilizando um input do usuario.
    '''
    entry = torch.as_tensor(features).float().to(device)
    output = network(entry)
    return output.ge(0.5) # Binariza o output da rede       

def normalize(person):
    '''
    Funcao que recebe os dados de exame de uma pessoa e retorna eles 
    normalizados de acordo com o valor minimo e maximo de cada exam
    '''
    norm = []
    i = 0
    for row in open('trained_nn/min_max.csv','r').readlines():
        if i >= len(person): break
        row = [float(x) for x in row.split(',')]
        new_result = 0.0
        if row[1] - row[0] != 0:
            new_result = (float(person[i]) - row[0]) / (row[1] - row[0])
        norm.append(new_result)
        i += 1

    return norm    

def use_network(device='cpu'):
    '''
    Funcao que recebe os exames de um paciente e usa cada uma das redes neurais 
    treinadas para retornar os resultados
    '''

    message = '==> Entre com os exames necessarios para a previsao\n'
    message += '==> [Formato: Creatinina/Potássio/RDW/...]\n'
    message += '==> [A lista de exames pode ser vists em PRE/used_analitos.csv]\n'
    answer = input(message).split(',')

    # rodando a rede de cada exame
    for exam in range(3):
        network = torch.load(MODEL_PATH[exam], map_location='cpu')
        answer = normalize(answer)
        prediction = predictor(network, device, answer)
        prediction = 'POSITIVO' if prediction else 'NEGATIVO'
        print('Resultado do exame ' + name[exam] + ': ' + prediction)

if __name__ == "__main__":
    use_network()
