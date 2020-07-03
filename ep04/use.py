'''
Programa implementa funcoes para o uso do modelo definido em model.py,
quando ja treinado, para a realizacao de previsoes de chuva,
dadas as features meteorologicas selecionadas em data.py
'''
import torch


def predictor(network, device, features):
    """Funcao que faz um uso unico da rede treinada"""
    entry = torch.as_tensor(features) \
        .float() \
        .to(device)
    output = network(entry)
    return output.ge(0.5)  # Binariza o output da rede       


def use_network(model_path='FFN_2HLayers.pt', device='cpu'):
    """Funcao que faz um uso unico da rede neural treinada, de maneira amigavel"""
    network = torch.load(model_path)
    message1 = '==> Entre com os dados  necessarios para a previsao...\n'
    message2 = '==> [Formato: rainfall/humidity/rain_today/pressure]\n==> '
    awnser = input(message1+message2).split('/')
    if awnser[0] == 'e':
        return False
    forecast = predictor(network, device, anwser)
    # a previsao tera formato [PCR, igG, igM]
    print('Resultado do exame PCR:' + str(forecast[0]))
    print('Resultado do exame igG:' + str(forecast[1]))
    print('Resultado do exame igM:' + str(forecast[2]))
    return True


def use_iteratively(model_path='FFN_2HLayers.pt', device='cpu'):
    """Funcao que proporciona um menu de uso iterativo da rede neural treinada"""
    print('==> Modelo neural carregado de '+model_path)
    print("==> (Use 'e' para sair)\n")
    keep_going = True
    while keep_going:
        keep_going = use_network(model_path, device)


if __name__ == "__main__":
    model_path = 'FFN_2HLayers.pt'
    use_iteratively(model_path, 'cpu')
