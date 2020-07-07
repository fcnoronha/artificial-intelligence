'''
    Arquivo que define o modelo neural a ser utilizado, incluindo
    a funcao de processamento dos dados atraves do modelo.
'''

from torch import nn
from torch import sigmoid

n_hl1 = 512
n_hl2 = 256
n_hl3 = 128

class Base_NN(nn.Module):
    '''
    Classe que define modelo de rede Feed-Foward simples, com duas camadas
    ocultas, totalmente conectadas.
    '''

    def __init__(self, n_features):
        super(Base_NN, self).__init__()

        self.hidden_layer_1 = nn.Linear(n_features, n_hl1)
        self.hidden_layer_2 = nn.Linear(n_hl1, n_hl2)
        self.hidden_layer_3 = nn.Linear(n_hl2, n_hl3)
        self.output_layer = nn.Linear(n_hl3, 1)

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
