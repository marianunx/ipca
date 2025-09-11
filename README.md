Calculadora IPCA com Histórico em SQLite

Este projeto é uma calculadora de correção monetária utilizando o índice IPCA (disponível via API do Banco Central).
O programa permite que o usuário realize 10 cálculos obrigatórios, que são salvos automaticamente em um banco de dados SQLite.

Como funciona

Após realizar os 10 cálculos:

O usuário visualiza uma lista com os valores originais de cada cálculo;

Pode selecionar qualquer valor para consultar os detalhes, incluindo:
-Valor original
-Período
-Fator acumulado
-Valor corrigido
-Data da consulta 

Como usar

Clone o repositório

Instale as dependências:
pip install bcb pandas
Execute o programa:
python calculadora_exata.py