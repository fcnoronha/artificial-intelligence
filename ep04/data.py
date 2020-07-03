'''
Programa que implementa as funcoes necessarias para o pre-processmento dos
dados brutos, necessario para leva-los a um estado adequado para
o treinamento pelo modelo definido em model.py.
'''


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(data_path='data/weatherAUS.csv'):
    """Funcao que importa dados de um aqruivo csv, usando pandas"""
    raw_data = pd.read_csv(data_path)
    return raw_data


def pre_processing(raw_data):
    """Funcao que filtra e limpa os dados meteorologicos para o treinamento"""

    # Seleciona as variaveis que serao usadas como features:
    cols = ['Rainfall', 'Humidity3pm', 'Pressure9am',
            'RainToday', 'RainTomorrow']
    processed_data = raw_data[cols]

    # Adequa o formato das variaveis RainToday e RainTomorrow:
    processed_data['RainToday'].replace({'No': 0, 'Yes': 1}, inplace=True)
    processed_data['RainTomorrow'].replace({'No': 0, 'Yes': 1}, inplace=True)

    # Remove todas as entradas dos dados que nao possuem
    # todas as features  instanciadas:
    processed_data = processed_data.dropna(how='any')
    return processed_data



if __name__ == "__main__":
    raw_data = load_data()
    processed_data = pre_processing(raw_data)
    visualize_data(processed_data)
