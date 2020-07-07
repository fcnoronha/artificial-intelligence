# <center> Previsão de estágio da infecção por COVID-19

## <center> MAC0425 Introdução a inteligencia artificial - EP04

<center> 
Carolina Senra Marques - 10737101
<br>
Felipe Castro de Noronha - 10737032
</center>

## Resumo

Introdução, que deve conter os seguintes elementos: motivação para o trabalho,
contendo um ou dois parágrafos; objetivos do trabalho, contendo um parágrafo;
estrutura do relatório a seguir, contém um parágrafo.

## Introdução

### Motivação
~max 2 paragrafos 

### Objetivos
~max 1 paragrafo 

### Estrutura deste relatório
~max 1 paragrafo


## Metodologia

que descreve os seguintes itens: pré-processamento dos dados; arquite-
tura da rede neural; descrição dos experimentos.

### Pré-processamento
~max 2 paginas 

- Arrumamos os arquivos, corrigimos os caracteres que estavam errados por causa da conversão de formatação, usando o script `_fix_utf.py`.
- Usamos os dados do HSL e Fleury (pegar o link la no paca depois)
- Com o script `_get_unique.py` pegamos todas as entradas únicas das colunas 'DE_ANALITO' da tabela de exames do fleury e hsl
- Decidimos que usaríamos todos os exames que estivessem presentes na interseção entre as duas tabelas, a lista completa destes exames utilizados pode ser vista em `used_analitos.csv`
    - Tivemos que refinar esta lista de exames usados, retirando da lista exames que tivesses resultados de difícil mapeamento numérico
- O arquivo `data.csv` contem os dados finais usados pela rede neural, é gerado pelo script `_generate.py`
    - O aquivo generate.py gera um dicionario para cada paciente, onde cada linha é uma lista com o numero de elementos igual ao numero de exames escolhidos
    - As linhas que contem informações sobre cada exame são ordenadas em relação a data
    - Criamos _batchs_ de exames realizados no mesmo dia, atualizando as entradas nas listas de exames dos respectivos pacientes
    - Ao final do processamento de um _batch_ todos os pacientes que tiveram seu prontuario de exames alterado viram novas linhas no arquivo `data.csv`
    - Assim, cada linha em `data.csv` representa todos os resultados de exames mais recentes que um determinado paciente tinha em um momento de tempo
    - Valores não inicializados foram deixados como 0
    - Para o treinamento da rede neural de cada exame, linhas onde ele não foi feito foram apagadas

### Arquitetura da rede neural
~max 3 paragros

Como arquitetura para a rede neural optamos por uma primeira camada de 512 nos, uma segunda camada de 256 e uma terceira de 128. 

### Descrição dos experimentos

## Resultados

## Discussão

## Bibliografia
