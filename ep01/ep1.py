"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Felipe Castro de Noronha
  NUSP : 10737032

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  - http://www.dominiopublico.gov.br/
    Usado para obter as obras que compoem a parte bonus

"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        if len(state) == 0: return True
        if state[0] == ' ' or state[-1] == ' ': return False
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        return self.query

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        lst = []
        for i in range(len(state)):
            lst.append(state[:i+1])
        return lst

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        new_state = state[len(action):]
        return new_state

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return len(state) == 0

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        cst = self.unigramCost(action)
        if (len(action) == 0): cst = 0
        return cst


def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
     
    # BEGIN_YOUR_CODE 

    '''
    Implementação da função que faz a seguimentação de palavras.

    Nessa implementação, o campo node.action vai conter a ultima palavra 
    originada, e o campo node.state representa o restante da string, parte 
    que ainda não foi dividida. Logo, temos que initial_node.action == "" 
    e que initial_node.state == query, além disso, temos que 
    goal_node.state == "" e que 
    goal_node.action == <utlima palavra da frase gerada>.

    Ademais, nossa transição de estado é feita colocando um espaço em todas 
    as posições possiveis dentro da string que representa a estado, e a 
    partir disso, criamos a divisão:
        
        <state> => <action> + <new_state>

    onde, para calcularmos o custo, basta pegarmos unigramCost(action).
    '''

    segmentation_problem = SegmentationProblem(query, unigramCost)	
    goal_node = util.uniformCostSearch(segmentation_problem)
    if (goal_node != None):
        is_valid, solution = util.getSolution(goal_node, segmentation_problem) 
        if (is_valid): 
            return solution
        else: 
            print("Could not recover solution for the segmentation problem")
            return None
    else:
        print("Could not complete search for the segmentation problem")
        return None
    
    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        initial = [util.SENTENCE_BEGIN] + self.queryWords
        return tuple(initial)

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        word = state[1]
        possibles = self.possibleFills(word)
        if (len(possibles) == 0): possibles = [word]
        return possibles

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        new_state = (action,) + state[2:] 
        return new_state

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        size = len(state)
        return size == 1

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        cst = self.bigramCost(state[0], action)
        return cst

def insertVowels(queryWords, bigramCost, possibleFills):
    
    # BEGIN_YOUR_CODE 
    
    '''
    Implementação da função que faz a inserção de vogais.

    Nessa implementação, o node.state é uma lista de strings que não possuem 
    vogais, a não ser pelo primeiro elemento da lista, este, representa a 
    ultima palavra que foi escolhida, já com as vogais. Além disso, o 
    node.action representa a palavra que foi escolhida naquele passo.

    Logo, temos que initial_node.state == (<BEGIN> + query words) e 
    initial_node.action = "", além disso, temos que 
    goal_node.state == goal_node.action == <ultima palavra gerada>.
    Assim, temos:

        state => action and new_state
    
    e para calcular o custo, basta pegarmos bigramCost(state[0], action).
    '''

    insert_problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    goal_node = util.uniformCostSearch(insert_problem)
    if (goal_node != None):
        is_valid, solution = util.getSolution(goal_node, insert_problem) 
        if (is_valid): 
            return solution
        else: 
            print("Could not recover solution for the insert vowels problem")
            return None
    else:
        print("Could not complete search for the insert vowels problem")
        return None
    
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()

    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)

    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

    # Meus testes
    result_segment = segmentWords('iamgoingtotakemyhorsetotheoldtownroad', unigramCost)
    print(result_segment)

    result_segment = segmentWords('thisprogramisverygoodandiamproundofmyself', unigramCost)
    print(result_segment)

    result_segment = segmentWords('notsoogood', unigramCost)
    print(result_segment)

    result_segment = segmentWords('ironic', unigramCost)
    print(result_segment)

    result_insert = insertVowels(['', 'hs', 'n', 'nw'], bigramCost, possibleFills)
    print(result_insert)

    result_insert = insertVowels(['', 'hv', 'n', 'ppl', 'pn'], bigramCost, possibleFills)
    print(result_insert)

    result_insert = insertVowels(['ths', 's', 'wrkng'], bigramCost, possibleFills)
    print(result_insert)

    result_insert = insertVowels(['th', 'lrd', 'f', 'th', 'rngs', 's', 'th', 'bst'], bigramCost, possibleFills)
    print(result_insert)


if __name__ == '__main__':
    main()
