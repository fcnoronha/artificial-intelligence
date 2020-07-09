Neste diretório temos os programas necessários para a rede neural. Para
executar o treinamento da rede basta executar `$ python3 main.py`. A rede 
gerada fica armazena em `/trained_nn/`.

Além, caso queira fazer uso da rede treinada para novas predições, execute 
`$ python3 use.py`. Um arquivo pode ser usado como entrada deste modo 
interativo, como, por exemplo, o arquivo txt aqui disponível, logo temos,
`$ python3 use.py < test_input.txt`.

Finalmente, o testes com k-fold stratified cross validation são realizados 
pelo script `experiment.py`, execute-o novamente caso queira checar a avaliação
dos diferentes modelos.