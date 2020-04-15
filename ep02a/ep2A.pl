% EP02a MAC0425 - INTELIGENCIA ARTIFICIAL

% FELIPE CASTRO DE NORONHA
% NUSP: 10737032

%%% PREDICADOS AUXILIARES %%%

% Checa se duas listam tem o mesmo tamanho
mesmo_tamanho([], []).
mesmo_tamanho([_|T1], [_|T2]) :-
    mesmo_tamanho(T1, T2).

% checa_subconjunto(X, Y) sucede se X for subconjunto de Y
checa_subconjunto([], _).
checa_subconjunto([H|T], L):- 
    member(H, L), 
    checa_subconjunto(T, L).

%%% EXERCICIO 1 %%% 

gera_conjunto(LO, [], ANS, C) :-
    checa_subconjunto(C, LO),
    ANS = C.
gera_conjunto(LO, [H|T], ANS, C) :-
    \+ member(H, C),
    append(C, [H], NC),
    gera_conjunto(LO, T, ANS, NC).
gera_conjunto(LO, [_|T], ANS, C) :-
    gera_conjunto(LO, T, ANS, C).
       
lista_para_conjunto(L, C) :-
    gera_conjunto(L, L, CN, []),
    !,
    C = CN.

% Testes:
% lista_para_conjunto([], []).
% lista_para_conjunto([], X).
% lista_para_conjunto([a,b,c], X).
% lista_para_conjunto([a,b,c], [c,a,b]).
% lista_para_conjunto([a,a,a,a,b,b,a,a,a,b,c], X).
% lista_para_conjunto([a,a,a,a,b,b,a,a,a,b,c], [b,a,c]).
% lista_para_conjunto([], [a,c]).
% lista_para_conjunto([x,x,x,x], [x]).


%%% EXERCICIO 2 %%% 

mesmo_conjunto(L1, L2) :- 
    mesmo_tamanho(L1, L2),
    checa_subconjunto(L1, L2), 
    checa_subconjunto(L2, L1).

% Testes:
% mesmo_conjunto([], [])
% mesmo_conjunto([a,b,c], [a,b,c])
% mesmo_conjunto([c,a,b], [b,a])
% mesmo_conjunto([a,b,c], [c,b,a])
% mesmo_conjunto([], [a])


%%% EXERCICIO 3 %%% 

uniao_conjunto(A, B, U) :-
    append(A, B, UR),
    lista_para_conjunto(UR, U).

% Testes:
% uniao_conjunto([], [], X). 
% uniao_conjunto([a,b], [], X).
% uniao_conjunto([a,b,c], [a,b,c], X).
% uniao_conjunto([a,c], [b,d], X).
% uniao_conjunto([], [a, b], X).
% uniao_conjunto([], [a,b], [a,b,c]). 


%%% EXERCICIO 4 %%% 

gera_inter([], _, ANS, ANS).
gera_inter([H|A], B, ANS, I) :-
    member(H, B),
    gera_inter(A, B, ANS, [H|I]).
gera_inter([_|A], B, ANS, I) :-
    gera_inter(A, B, ANS, I).

inter_conjunto(A, B, I) :-
    gera_inter(A, B, IO, []),
    mesmo_conjunto(IO, I),
    !.

% Testes:
% inter_conjunto([], [], []).
% inter_conjunto([a], [a], [a]).
% inter_conjunto([a], [a], X).
% inter_conjunto([a,b,c], [a,d,e], X).
% inter_conjunto([a,b,c], [a,b,c], X).
% inter_conjunto([], [b], X).


%%% EXERCICIO 5 %%% 

calcula_diferenca([], _, D, D).
calcula_diferenca([X|A], B, ANS, D) :- 
    member(X, B),
    calcula_diferenca(A, B, ANS, D).
calcula_diferenca([X|A], B, ANS, D) :-
    \+ member(X, B),
    calcula_diferenca(A, B, ANS, [X|D]).

diferenca_conjunto(A, B, D) :- 
    calcula_diferenca(A, B, D, []),
    !.

% Testes:
% diferenca_conjunto([], [], []).
% diferenca_conjunto([a,b], [], X).
% diferenca_conjunto([a,b,c], [c, h], []).
% diferenca_conjunto([a,b,c], [c, h], X).
% diferenca_conjunto([], [a,b], X).
% diferenca_conjunto([a], [a], []).



%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes come�am aqui.
%%%%%%%% Para executar os testes, use a consulta:   ?- run_tests.

%%%%%%%% Mais informacoes sobre testes podem ser encontradas em:
%%%%%%%%    https://www.swi-prolog.org/pldoc/package/plunit.html

:- begin_tests(conjuntos).
test(lista_para_conjunto, all(Xs=[[1,a,3,4]]) ) :-
    lista_para_conjunto([1,a,3,3,a,1,4], Xs).
test(lista_para_conjunto2,fail) :-
    lista_para_conjunto([1,a,3,3,a,1,4], [a,1,3,4]).

test(mesmo_conjunto, set(Xs=[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    mesmo_conjunto([1,a,3], Xs).
test(uniao_conjunto2,fail) :-
    mesmo_conjunto([1,a,3,4], [1,3,4]).

test(uniao_conjunto, set(Ys==[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    uniao_conjunto([1,a], [a,3], Xs),
    mesmo_conjunto(Xs,Ys).
test(uniao_conjunto2,fail) :-
    uniao_conjunto([1,a,3,4], [1,2,3,4], [1,1,a,2,3,3,4,4]).

test(inter_conjunto, all(Xs==[[1,3,4]])) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], Xs).
test(inter_conjunto2,fail) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], [1,1,3,3,4,4]).

test(diferenca_conjunto, all(Xs==[[2]])) :-
    diferenca_conjunto([1,2,3], [3,a,1], Xs).
test(diferenca_conjunto2,fail) :-
    diferenca_conjunto([1,3,4], [1,2,3,4], [_|_]).

:- end_tests(conjuntos).
