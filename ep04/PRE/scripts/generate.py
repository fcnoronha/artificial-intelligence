'''
script responsavel por gerar dataset final
'''
import re

# palavras que devem ser mapeadas para valores negativos, positivos ou zero
subst_z = ['inferior a','ausentes ','ausentes','INDETECTÁVEL',
           'NÃO DETECTADO','Indeterminado','Inconclusivo','Inconclusivo ',
           'Indetectável','normal','INCONCLUSIVO','INCONCLUSIVO ',
           'INDETERMINADO','Influenza B - POSITIVO','FRACAMENTE REAGENTE ',
           '-','---','*','vide contagem de plaquetas especial.']
subst_n = ['NEGATIVO','N E G A T I V A','negativo','negativa','NÃO REAGENTE',
           'não reagente','Não reagente','Mutação ausente',
           'NÃO DETECTADO (NEGATIVO)']
subst_p = ['POSITIVO','P O S I T I V O','POSITIVA','Influenza A - POSITIVO',
           'superior a','maior que 250','positivo','DETECTADO','REAGENTE',
           'DETECTÁVEL','cerca d','DETECTADO (POSITIVO)']

FILE_PATH = '../'
FILE_NAME = 'data'

def remove_space_nl(s):
    '''
    Remove espaços e quebras de linha de uma determinada string s.
    '''
    s = s.replace(' ', '')
    s = s.replace('\n', '')
    return s

def substitute(x):
    '''
    Transforma um dado valor x no seu devido valor. Realiza as seguintes
    checagens:
    - se é uma string que estabelece um limite e retira o dado limite
    - se é uma string e deveria ter um valor em {-1,0,1} 
    - se é um numero em string, retornando o valor convertido
    '''
    if 'inferior' in x or 'superior' in x or 'maior' in x or 'cerca' in x:             
        match = re.findall('\d+', x)  
        return float(match[0])
    if x in subst_z or 'REAGENTE' in x:
        return 0.0
    if x in subst_n:
        return -1.0
    if x in subst_p:
        return 1.0
    return float(x)

def remove_space_nl(s):
    '''
    Remove espaços e quebras de linha de uma determinada string s.
    '''
    s = s.replace(' ', '')
    s = s.replace('\n', '')
    return s

def extract_exams():
    '''
    Lê todos os exames do arquivo all_both_unique.csv, criando um dicianario
    que mapeia exames para uma determinada coluna da tabela e cria a lista
    com as labels do dataset gerado.
    
    Retorna o dicionario e o numero de diferentes features levadas em conta.
    '''
    ex2col = {}
    feature_cnt = 2
    labels = ['SEXO', 'IDADE']
    for row in open(FILE_PATH + 'all_both_unique.csv'):
        row = row.split(',')
        labels.append(row[0].replace('\n', ''))
        for ex in row:
            ex2col[remove_space_nl(ex)] = feature_cnt
        feature_cnt += 1

    # escrevendo cabeçalho do dataset
    f = open(FILE_PATH + FILE_NAME + '.csv', 'w+')
    f.write(str(labels)[1:-1] + '\n')
    f.close()

    return ex2col, feature_cnt

def generate_dataset(ex2col, fcnt):
    '''
    Função que gera o dataset.
    '''
    data = {}
    # nome do dataset atual, se tem aspas nos campos, indice da coluna de data
    for name, has_qm, date_idx in [('fleury', False, 1), ('hsl', True, 2)]:
        is_first = True
        # criando uma entrada no dicionario para cada paciente
        for row in open(FILE_PATH + './' + name + '_p.csv'):
            if is_first:
                is_first = False
                continue
            if has_qm: row = row.replace('\"', '') 
            row = row.split(',')
            id_pacient = str(row[0])
            data[id_pacient] = [0 for i in range(fcnt)]
            data[id_pacient][0] = 1 if 'F' in row[1] else 2 # 1==F | 2==M
            if row[2] != 'AAAA': 
                data[id_pacient][1] = 2020 - int(row[2])

        # arquivo de exames do hospital atual
        all_ex = open(FILE_PATH + name + '_e.csv', 'r').read()
        if has_qm: all_ex = all_ex.replace('\"', '')
        all_ex = all_ex.split('\n')
        all_ex = all_ex[1:]

        # fazendo com que o arquivo lido vire uma tabela
        sz = len(all_ex)
        for i in range(sz):
            all_ex[i] = all_ex[i].split(',')
            date = all_ex[i][date_idx]
            # fazendo com que a data vire um inteiro da forma YYYYMMDD
            if name == 'fleury':
                all_ex[i][date_idx] = int(date[6:] + date[3:5] + date[:2])
            if name == 'hsl':
                all_ex[i][date_idx] = int(date[:4] + date[5:7] + date[8:])

        # sorteado a lista de exames de acordo com a data
        all_ex = sorted(all_ex, key=lambda x: x[date_idx])

        r = l = 0
        # criando batchs de dias a serem processados
        while r < sz:
            while r < sz and all_ex[r][date_idx] == all_ex[l][date_idx]: r += 1
            is_modified = set()
            # processando todos os exames realizado em um determinado dia
            for i in range(l, r):
                id_pacient = all_ex[i][0]
                exam = remove_space_nl(all_ex[i][date_idx + 3])
                result = all_ex[i][date_idx + 4]
                if exam not in ex2col: continue
                result = substitute(result)
                id_col = ex2col[exam]
                data[id_pacient][id_col] = result
                is_modified.add(id_pacient)

            # colocando novas linhas no dataset para pacientes modificados
            f = open(FILE_PATH + FILE_NAME + '.csv', 'a+')
            for id_pacient in is_modified:
                f.write(str(data[id_pacient])[1:-1] + '\n')
            f.close()
            l = r

if __name__ == "__main__":
    ex2col, feature_cnt = extract_exams()
    generate_dataset(ex2col, feature_cnt)