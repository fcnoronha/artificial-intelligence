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
"""

import math
import random
from collections import defaultdict
import util


# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        return ['Pegar', 'Espiar', 'Sair']

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (newState, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        # BEGIN_YOUR_CODE
        
        # corner cases
        if state[2] == None: return []
        if action == 'Espiar' and state[1] != None: return []

        # total amount of cards available in state
        total_amt = 0
        for x in state[2]: total_amt += x

        reachable_states = []
        if action == 'Pegar':
            # if i will iterate though all cards or if i know the next card
            list_iter = range(len(self.valores_cartas)) if state[1] == None else [state[1]]
            for i in list_iter:
                # card not available on current deck
                if state[2][i] == 0: continue
                new_hand = state[0] + self.valores_cartas[i]
                # if the game is over deck should be None
                if new_hand > self.limiar or total_amt == 1: 
                    new_deck = None
                else:  
                    new_deck = state[2][:i] + (state[2][i]-1,) + state[2][i+1:]
                # probability of the new state
                if state[1] == None:
                    new_prob = state[2][i]/total_amt
                else:
                    new_prob = 1
                # reward of the new state
                if total_amt == 1 and new_hand <= self.limiar:
                    new_reward = new_hand
                else:
                    new_reward = 0
                new_state = (new_hand, None, new_deck)
                new_tuple = (new_state, new_prob, new_reward)
                reachable_states.append(new_tuple)

        elif action == 'Espiar':
            for i in range(len(self.valores_cartas)):
                # card not available on current deck
                if state[2][i] == 0: continue
                new_state = (state[0], i, state[2])
                new_tuple = (new_state, state[2][i]/total_amt, -self.custo_espiada)
                reachable_states.append(new_tuple)

        elif action == 'Sair':
            if state[0] > self.limiar:
                new_tuple = ((state[0], None, None), 1, 0)
            # return total amount in hands if not bankrupt
            else:
                new_tuple = ((state[0], None, None), 1, state[0])
            reachable_states.append(new_tuple)

        return reachable_states
        # END_YOUR_CODE

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.pi = {}
        self.V = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.V to the dictionary mapping states to optimal values
        - self.pi to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi
        
        V = defaultdict(float)  # state -> value of state
        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE

        gamma = mdp.discount()
        continue_iter = True
        while continue_iter:
            # new value function
            vp = defaultdict(float)
            for state in mdp.states:
                vp[state] = -float('inf')
                for action in mdp.actions(state):
                    q = 0
                    for ss, p, r in mdp.succAndProbReward(state, action):
                        q += p * (gamma*V[ss] + r)
                    if q > vp[state]: 
                        vp[state] = q 
            continue_iter = False
            for state in mdp.states:
                if abs(vp[state]-V[state]) >= epsilon:
                    continue_iter = True
            if continue_iter: V = vp
                
        # END_YOUR_CODE

        # Extract the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        # print("ValueIteration: %d iterations" % numIters)
        self.pi = pi
        self.V = V

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)

# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)

def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE

    XERETA = BlackjackMDP(valores_cartas=[4, 8, 25], multiplicidade=2, limiar=20, custo_espiada=1)
    return XERETA

    # END_YOUR_CODE


# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE

        # learning rate 
        alpha = self.getStepSize()
        # gamma
        gamma = self.discount
        # Q for current state and action
        cur_q = self.getQ(state, action)
        
        # best value from s' taking action a'
        next_state_val = 0
        if newState != None:
            for al in self.actions(newState):
                if self.getQ(newState, al) > next_state_val:
                    next_state_val = self.getQ(newState, al)
            
        # update weights from features
        for f, v in self.featureExtractor(state, action):
            self.weights[f] += alpha*(reward + (gamma*next_state_val) - cur_q)*v

        # END_YOUR_CODE

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE

    # pairs (feature_key, feature_value)
    extracted = []
    feature_value = 1

    # first kind of feature: taken action and total in hands
    feature_key = action + "_" + str(state[0])
    extracted.append((feature_key, feature_value))

    if state[2] != None:
        # second kind of features: action and presence/absence of cards of each type 
        feature_key = action + "_has_cards_"
        feature_value = 1
        for i in range(len(state[2])):
            feature_key += str(1 if state[2][i] > 0 else 0)
        extracted.append((feature_key, feature_value))

        # third kind of features: action and amount of cards of each type
        for i in range(len(state[2])):
            feature_key = action + "_amt_card_" + str(i) + "_" + str(state[2][i])
            extracted.append((feature_key, feature_value))

    return extracted
    # END_YOUR_CODE