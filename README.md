# NEAT aplicado no Jogo Flappy Bird utilizando Python

## Introdução

É utilizado a Rede Neural NEAT, Neural Evolution Augmenting Topology, e a Biblioteca Pygame do Python
para desenvolver esse Projeto. A rede neural utilizando o Python vai permitir com que o usuário defina os
inputs(Entradas) e Outputs(Saidas), ou seja, vai definir as informações de entrada(configurações) e de
acordo com essa entrada um resultado especifico. O trabalho das redes neurais é jogar o jogo com diferentes
entradas até que consiga aprender a saida "perfeita".



## NEAT

A configuração do NEAT é feita em um arquivo TXT e linkada no código, para que seja possivelmente a IA identificar suas regras. É passado vários Input para NEAT, no caso 100:

![Input and Output1](https://user-images.githubusercontent.com/42840902/114314540-8f6c1680-9ad1-11eb-8577-5ebb5f180c1f.png)

É feito um conceito de **_gerações_**, onde dentre esses 100 Inputs irá gerar 1 output, ao aplicar os 100 Inputs no Jogo, irá analisar e verificar qual dos Inputs teve um melhor output, sendo assim, fazendo uma geração nova através deste input.

Para saber mais sobre a AI NEAT, Acesse [NEAT Python](https://neat-python.readthedocs.io/en/latest/).

## Execução

Para rodar o projeto é necessário a instalação de uma Biblioteca dentro de um Ambiente Virtual para não instalar pacotes a mais no seu Python Global do Computador, ou seja:



Para criar uma Ambiente Virtual:

```python
Python -m venv {nome_do_Ambiente_Virtual}
```

Entrar na venv:

```python
Windows = {nome_do_Ambiente_Virtual}/Scripts/activate

Linux = source {nome_do_Ambiente_Virtual}\bin\activate
```

Bibliotecas:

```python
pip install pygame
```

```python
pip install neat-python
```

**Pronto!**

## Demonstração

![flappybridvideo1 2](https://user-images.githubusercontent.com/42840902/114314070-972abb80-9acf-11eb-943d-865d3340420e.gif)

Se quiser jogar o jogo, é possivel fazer essa alteração no código, na Variavel **ai_jogando**, deve colocar valor **False** para que o jogo se torne manual.

## Ferramentas
- Python(Pygame)
- NEAT(Neural Evolution Augmenting Topology)

