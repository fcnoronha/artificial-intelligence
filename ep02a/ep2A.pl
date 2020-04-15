%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necess�rio

%%% PREDICADOS AUXILIARES

% Checa se duas listam tem o mesmo tamanho
mesmo_tamanho([], []).
mesmo_tamanho([_|T1], [_|T2]) :-
    mesmo_tamanho(T1, T2).

% checa_subconjunto(X, Y) sucede se X for subconjunto de Y
checa_subconjunto([], _).
checa_subconjunto([H|T], L):- 
    member(H, L), 
    checa_subconjunto(T, L).

% checa_subconjunto_ord(X, Y) sucede se X for subconjunto de Y, onde os
% elementos em X tem que aparecer na mesma ordem que aparecem em Y
checa_subconjunto_ord([], _).
checa_subconjunto_ord(_, []) :-
    false.
checa_subconjunto_ord([H|T], [H|L]):- 
    checa_subconjunto_ord(T, L).
checa_subconjunto_ord([H|T], L):- 
    member(H1, L), 
    checa_subconjunto_ord(T1, L).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1 - NÂO OK

gera_conjunto([], C, LO) :- 
    checa_subconjunto(C, LO).
gera_conjunto( [H | T], C, LO) :- 
    member(H, C),
    gera_conjunto(T, C, LO).
gera_conjunto( [H | T], C, LO) :- 
    \+ member(H, C),
    append(C, [H], C),
    gera_conjunto(T, C, LO).

%lista_para_conjunto(L, C) :- 
%    gera_conjunto(L, C, L),
%    !.

lista_para_conjunto(List, Unique) :-
    list_unique_1(List, [], Unique).
list_unique_1([], _, []).
list_unique_1([X|Xs], So_far, Us) :-
    list_unique_2(X, Xs, So_far, Us).
list_unique_2(X, Xs, So_far, [X|Us]) :-
    maplist(dif(X), So_far),
    list_unique_1(Xs, [X|So_far], Us).
list_unique_2(X, Xs, So_far, Us) :-
    memberchk(X, So_far),
    list_unique_1(Xs, So_far, Us).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2 - OK

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3 - OK

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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4 - OK

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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 5 - FALTA TESTAR

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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



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
