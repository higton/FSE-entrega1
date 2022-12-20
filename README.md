# FSE - Trabalho 2

| Aluno | Matricula |
| --|-- |
| Paulo Batista | 180054554 |

## Sobre

Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. 

### Observações:

* A aplicação central foi configurada para rodar na placa 2, caso queria modificar, é necessário alterar o json e os parametros que são passados para o script.
* É importante rodar a aplicação **Central** com a janela do terminal em um tamanho grande.

## Como executar

#### Central

```
cd central
python3 main.py 10422 '164.41.98.26'
```

#### Distribuido 1

```
cd distribuido
python3 main.py ../configuracao_sala_0.json
```

#### Distribuido 2

```
cd distribuido
python3 main.py ../configuracao_sala_02.json
```
