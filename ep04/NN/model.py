'''
    Arquivo que define o modelo neural a ser utilizado, incluindo
    a funcao de processamento dos dados atraves do modelo.
'''

from torch import nn
from torch import sigmoid

class NN1(nn.Module):
    '''
    Modelo 1 da rede Feed-Foward simples, com três camadas ocultas de tamanho
    512, 256 e 128
    '''

    def __init__(self, n_features):
        super(NN1, self).__init__()

        self.n_hl1 = 512
        self.n_hl2 = 256
        self.n_hl3 = 128
        self.hidden_layer_1 = nn.Linear(n_features, self.n_hl1)
        self.hidden_layer_2 = nn.Linear(self.n_hl1, self.n_hl2)
        self.hidden_layer_3 = nn.Linear(self.n_hl2, self.n_hl3)
        self.output_layer = nn.Linear(self.n_hl3, 1)

    def forward(self, x):
        '''
        Define uma passagem pelas camadas da rede. A partir disso, o pytorch
        gera o backpropagation.
        '''
        h1 = nn.functional.relu(self.hidden_layer_1(x))
        h2 = nn.functional.relu(self.hidden_layer_2(h1))
        h3 = nn.functional.relu(self.hidden_layer_3(h2))
        y = sigmoid(self.output_layer(h3))
        return y

class NN2(nn.Module):
    '''
    Modelo 2 da rede Feed-Foward simples, com três camadas ocultas de tamanho
    1024, 512 e 256 
    '''

    def __init__(self, n_features):
        super(NN2, self).__init__()

        self.n_hl1 = 1024
        self.n_hl2 = 512
        self.n_hl3 = 256
        self.hidden_layer_1 = nn.Linear(n_features, self.n_hl1)
        self.hidden_layer_2 = nn.Linear(self.n_hl1, self.n_hl2)
        self.hidden_layer_3 = nn.Linear(self.n_hl2, self.n_hl3)
        self.output_layer = nn.Linear(self.n_hl3, 1)

    def forward(self, x):
        '''
        Define uma passagem pelas camadas da rede. A partir disso, o pytorch
        gera o backpropagation.
        '''
        h1 = nn.functional.relu(self.hidden_layer_1(x))
        h2 = nn.functional.relu(self.hidden_layer_2(h1))
        h3 = nn.functional.relu(self.hidden_layer_3(h2))
        y = sigmoid(self.output_layer(h3))
        return y


class NN3(nn.Module):
    '''
    Modelo 3 da rede Feed-Foward simples, com três camadas ocultas de tamanho
    256, 128 e 64
    '''

    def __init__(self, n_features):
        super(NN3, self).__init__()

        self.n_hl1 = 256
        self.n_hl2 = 128
        self.n_hl3 = 64
        self.hidden_layer_1 = nn.Linear(n_features, self.n_hl1)
        self.hidden_layer_2 = nn.Linear(self.n_hl1, self.n_hl2)
        self.hidden_layer_3 = nn.Linear(self.n_hl2, self.n_hl3)
        self.output_layer = nn.Linear(self.n_hl3, 1)

    def forward(self, x):
        '''
        Define uma passagem pelas camadas da rede. A partir disso, o pytorch
        gera o backpropagation.
        '''
        h1 = nn.functional.relu(self.hidden_layer_1(x))
        h2 = nn.functional.relu(self.hidden_layer_2(h1))
        h3 = nn.functional.relu(self.hidden_layer_3(h2))
        y = sigmoid(self.output_layer(h3))
        return y
