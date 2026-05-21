# BIBLIOTECAS/LIBRARIES

import networkx as nx
import numpy as np
import gurobipy as gp
# from gurobipy import GRB
from time import perf_counter
from datetime import timedelta


def ler_elementos_por_id(nome_arquivo):
    elementos_por_id = {}

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Remove espaços em branco e quebras de linha
            linha = linha.strip()
            # Divide a linha em duas partes: a primeira parte (antes da vírgula) é o índice, a segunda é a lista de elementos
            indice, elementos_str = linha.split(',', 1)
            # Avalia a string para transformá-la em uma lista de elementos
            elementos = eval(elementos_str)
            # Armazena os elementos na estrutura com o índice como chave
            elementos_por_id[int(indice)] = elementos

    return elementos_por_id


def ler_arestas_por_id_(nome_arquivo):
    arestas_por_id = {}

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Remove espaços em branco e quebra de linha
            linha = linha.strip()
            # Divide a linha em duas partes: a primeira parte (antes da vírgula) é o índice, a segunda são as arestas
            indice, arestas_str = linha.split(',', 1)
            # Avalia a string para transformá-la em uma lista de tuplas
            arestas = eval(arestas_str)
            # Armazena as arestas na estrutura com o índice como chave
            arestas_por_id[int(indice)] = arestas

    return arestas_por_id


def ler_arestas_por_id(caminho_arquivo):
    dicionario = {}

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Separar a linha pela primeira vírgula
            chave, resto = linha.split(',', 1)

            # Extrair a lista e ignorar o valor final
            lista, _ = resto.rsplit(',', 1)

            # Converter a lista de string para uma lista de tuplas
            lista_tuplas = eval(lista)

            # Armazenar no dicionário
            dicionario[int(chave)] = lista_tuplas

    return dicionario


def carregar_segundos_elementos(nome_arquivo):
    segundos_elementos_por_id = {}

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Remove espaços em branco e quebras de linha
            linha = linha.strip()
            # Divide a linha em partes usando a vírgula como separador
            elementos = linha.split(',')
            # Converte o primeiro elemento (ID) para inteiro
            id_atual = int(elementos[0])
            # Armazena o segundo elemento no dicionário
            segundos_elementos_por_id[id_atual] = elementos[1]

    return segundos_elementos_por_id


def gerar_lista(frente, atras, x):
    # Inicializa a lista com zeros
    lista = [0] * x

    # Preenche com 1 nas posições indicadas pela lista 'frente'
    for indice in frente:
        lista[indice] = 1

    # Preenche com -1 nas posições indicadas pela lista 'atras'
    for indice in atras:
        lista[indice] = -1

    return lista


# Total de execucoes
exe = 135


def main():

    # read the data
    nome_arquivo = 'data2/grafo.txt'
    nome_arquivo2 = 'data2/grafo_vet.txt'
    nome_arquivo3 = 'data2/grafo_frente.txt'
    nome_arquivo4 = 'data2/grafo_tras.txt'
    nome_arquivo5 = 'data2/grafo_info.txt'

    dicionario_arestas = ler_arestas_por_id(nome_arquivo)
    # print('dicionario_arestas=', dicionario_arestas)
    # stop

    dicionario_elementos = ler_elementos_por_id(nome_arquivo2)
    dicionario_frente = ler_elementos_por_id(nome_arquivo3)
    dicionario_atras = ler_elementos_por_id(nome_arquivo4)
    dicionario_nodes = carregar_segundos_elementos(nome_arquivo5)

    '''
    print(' dicionario_arestas=',dicionario_arestas )
    print(' ')

    print('dicionario_elementos =',dicionario_elementos )
    print(' ')

    print(' dicionario_frente=', dicionario_frente)
    print(' ')

    print('dicionario_atras =', dicionario_atras)
    print(' ')

    print('dicionario_nodes =', dicionario_nodes)
    print(' ')
    '''

    # stop

    for i0 in np.arange(exe):

        arq_model = open('res_model2/model_'+f"{i0 + 1}"+'.txt', 'a')
        arq_model_list = open('res_model2/model_list_'+f"{i0 + 1}"+'.txt', 'a')

        # Acessando a lista de arestas
        # print(dicionario_arestas[i+1])

        # Acessando a lista de elementos
        # print(dicionario_elementos[i+1])

        # Acessando a lista de elementos frente
        # print(dicionario_frente[i+1])

        # Acessando a lista de elementos atras
        # print(dicionario_atras[i+1])

        # Acessando a lista de toral de nodes
        # print(dicionario_nodes[i+1])

        # Criar um grafo não direcionado --------------------------------------
        g = nx.Graph()

        # total de estudantes
        s = int(dicionario_nodes[i0+1])

        # Adicionar vértices/nodes
        g.add_nodes_from(range(s))

        # Adicionar arestas
        arestas = dicionario_arestas[i0+1]

        #print(arestas[0])
        #stop

        # Adicionar arestas ao grafo garantindo que o primeiro elemento seja menor que o segundo
        g.add_edges_from([tuple(sorted(aresta)) for aresta in arestas])

        # Contabilizar o total de arestas
        ta = g.number_of_edges()

        # carteiras por fileira
        n = dicionario_elementos[i0+1]

        # total de layers
        c = len(n)

        # requisitos 1: frente / -1:f  fundo / 0: sem requisitos
        r = gerar_lista(dicionario_frente[i0+1], dicionario_atras[i0+1], s)

        start_time = perf_counter()

        #  ------------------------------------------------

        # Create a new model
        cm = gp.Model(name="CM")

        # binaries decision variables / Use list comprehension
        a = {(i, j): cm.addVar(lb=0, ub=1, obj=1, vtype=gp.GRB.BINARY, name=f'a_{i}_{j}', column=None)
             for i in np.arange(s) for j in np.arange(s) if i != j}

        # binaries decision variables / Use list comprehension
        x = {(i, ca, k): cm.addVar(lb=0, ub=1, obj=0, vtype=gp.GRB.BINARY, name=f'x_{i}_{ca}_{k}', column=None)
             for i in np.arange(s) for ca in np.arange(c) for k in np.arange(n[ca])}

        # conflict vector
        co = {(i, j): 1 if i != j and (g.has_edge(i, j) or g.has_edge(j, i)) else 0 for i in np.arange(s)
              for j in np.arange(s)}

        # ------------------------------------------
        # auxiliar binaries decision variables para linearizar funcão yi*yj (0,0)=(1,0)=(0,1) = 0 e (1,1)=abs(z-w)
        w = {(i, j, ca, k, z): cm.addVar(lb=0, ub=1, obj=1, vtype=gp.GRB.BINARY, name=f'w_{i}_{j}_{ca}_{k}_{z}',
                                         column=None) for ca in np.arange(c - 1) for k in range(n[ca])
             for z in range(n[ca + 1]) for (i, j) in co if co[i, j] != 0}

        # -------------------------------------------

        objective = gp.quicksum(abs(z - k) * w[i, j, ca, k, z] - ta * a[i, j] for ca in np.arange(c - 1)
                                for k in np.arange(n[ca]) for z in np.arange(n[ca + 1]) for (i, j) in co if
                                co[i, j] == 1)

        # (2)
        for i in np.arange(s):
            cm.addConstr(gp.quicksum(x[i, ca, k] for ca in range(c) for k in range(n[ca])) == 1, f'restr_2_{i}')

        # (3)
        for ca in np.arange(c):
            for k in range(n[ca]):
                cm.addConstr(gp.quicksum(x[i, ca, k] for i in range(s)) <= 1, f'restr_3_{ca}_{k}')

        # -------------------------------------------------------------------------- temp

        # (4)
        for i in range(s):
            for j in range(s):
                if (i, j) in co and co[i, j] != 0:  # Verifica se há um conflito entre os alunos i e j
                    for ca in range(c - 1):  # Itera sobre as camadas
                        for k in range(n[ca]):  # Itera sobre as posições dos alunos na camada ca
                            for z in range(n[ca + 1]):
                                cm.addConstr(a[i, j] >= x[i, ca, k] + x[j, ca + 1, z] - 1,
                                             f'restr_4_{i}_{j}_{ca}_{k}_{z}')

        # (4) ''
        for (i, j) in co:
            if co[i, j] == 1:  # Verifica se há um conflito entre os alunos i e j
                for ca in range(c - 1):  # Itera sobre as camadas
                    for k in range(n[ca]):  # Itera sobre as posições dos alunos na camada ca
                        for z in range(n[ca + 1]):
                            cm.addConstr(w[i, j, ca, k, z] >= x[i, ca, k] + x[j, ca + 1, z] - 1,
                                         f'restr_e2_{ca}_{i}_{j}_{k}_{z}')
                            cm.addConstr(w[i, j, ca, k, z] <= x[i, ca, k], f'restr_e3_{ca}_{i}_{j}_{k}_{z}')
                            cm.addConstr(w[i, j, ca, k, z] <= x[j, ca + 1, z], f'restr_e4_{ca}_{i}_{j}_{k}_{z}')

                            cm.addConstr(abs(z - k) * w[i, j, ca, k, z] >= 2 * w[i, j, ca, k, z],
                                         f'restr_e1_{ca}_{i}_{j}_{k}_{z}')
                            cm.addConstr(abs(z - k) * w[i, j, ca, k, z] <= max(n[ca] - 1, n[ca + 1] - 1),
                                         f'restr_e5_{ca}_{i}_{j}_{k}_{z}')

        # ---------------------------------------------------------------------

        # (7)
        for i in np.arange(s):
            for j in np.arange(s):
                if i != j:
                    cm.addConstr(a[i, j] <= co[i, j], f'restr_7_{i}_{j}')

        # --------------------------------------------------------------------------------------------------

        d_min = 2  # 3
        # (8)
        for i in range(s):
            for j in range(s):
                if (i, j) in co and co[i, j] == 1:  # Verifica se há um conflito entre os alunos i e j
                    for ca in range(c):  # Itera sobre as camadas
                        for k in range(n[ca] - 1):  # Itera sobre as posições dos alunos na camada ca
                            for z in range(k + 1, n[ca]):
                                # Garante que a diferença entre as posições dos alunos na mesma camada seja >= 2
                                # cm.addConstr(z - k >= x[i, ca, k] + x[j, ca, z], f'restr_8_{i}_{j}_{ca}_{k}_{z}')
                                cm.addConstr(z - k >= (x[i, ca, k] + x[j, ca, z] - 1) * d_min,
                                             f'restr_8_{i}_{j}_{ca}_{k}_{z}')
        '''

        # Teste d_min
        d_min = 2  # ou qualquer valor mínimo desejado

        for i in range(s):
            for j in range(s):
                if (i, j) in co and co[i, j] == 1:  # Verifica se há um conflito entre os alunos i e j
                    for ca in range(c):  # Itera sobre as camadas
                        for k in range(n[ca] - d_min):  # Itera sobre as posições dos alunos na camada ca
                            for z in range(k + d_min, n[ca]):
                                # Garante que a diferença entre as posições dos alunos na mesma camada seja >= d_min
                                cm.addConstr(z - k >= x[i, ca, k] + x[j, ca, z], f'restr_8_{i}_{j}_{ca}_{k}_{z}')
        '''

        # --------------------------------------------------------------------------------------------------------
        # (9)
        # guarantees the first two rows (one or the other) for students who need to sit in the front
        for i in range(s):
            if r[i] == 1:
                cm.addConstr(gp.quicksum(x[i, ca, 0] for ca in np.arange(c))
                             + gp.quicksum(x[i, ca, 1] for ca in np.arange(c)) == 1, f'restr_9_{i}')

        # (10)
        # guarantees the last two rows (one or the other) for students who need to sit at the back
        for i in range(s):
            if r[i] == -1:
                cm.addConstr(gp.quicksum(x[i, ca, n[ca] - 1] for ca in np.arange(c))
                             + gp.quicksum(x[i, ca, n[ca] - 2] for ca in np.arange(c)) == 1, f'restr_10_{i}')

        # for maximization / minimization
        cm.ModelSense = gp.GRB.MAXIMIZE  # MINIMIZE
        cm.setObjective(objective)

        cm.write("cm.lp")

        # Optimize model
        cm.optimize()

        # ------------------------------------------------

        end_time = perf_counter()

        # ----------------------------------------------------------------

        # Define uma função para formatar números
        def format_number(t):
            if t == 0:
                return abs(t)  # Retorna o valor absoluto de 0, que é 0
            else:
                return t  # Retorna o número original se não for 0

        # -----------------------------------------------------Armazena Results
        # Define dicionários para armazenar os resultados
        aij_results = {}
        x_results = {}
        dij_results = {}

        # Use a função format_number para imprimir os resultados e armazená-los
        for v in cm.getVars():
            if v.VarName.startswith('a_') and v.x == 1:
                # Armazena os resultados para aij=1
                aij_results[v.VarName] = v.x
            if v.VarName.startswith('d_') and v.x != 0:
                # Armazena os resultados para dij=1
                dij_results[v.VarName] = v.x
            elif v.VarName.startswith('x_') and v.x == 1:
                # Armazena os resultados para x=1
                x_results[v.VarName] = v.x

        # Lista de listas par imprimir resultados -----------------------------------------

        # Inicializa a estrutura de listas de listas
        fileiras = [[] for _ in range(c)]  # 7 fileiras (0 a 6)

        # Processa as variáveis e organiza os alunos nas fileiras e posições
        for var_name, value in x_results.items():
            # Extrai os índices do nome da variável
            parts = var_name.split('_')
            aluno, fileira, posicao = map(int, parts[1:])
            # Garante que a sublista tenha o tamanho adequado
            while len(fileiras[fileira]) <= posicao:
                fileiras[fileira].append(None)
            # Coloca o aluno na posição correta
            fileiras[fileira][posicao] = aluno

        # Remove os None das sublistas para maior clareza (opcional)
        fileiras = [list(filter(lambda elem: elem is not None, fileira)) for fileira in fileiras]

        # Exibe a estrutura resultante
        # print(fileiras)

        # ----------------------------------------------------------------
        '''
        # Verificando se a solução é ótima  - # GRB.OPTIMAL
        if cm.status == gp.GRB.OPTIMAL:
            # id graph, f(x) Objective function, Problem Status, time, time
            arq_model.write(
                str(i0+1) + str(',') + str(int(cm.ObjVal)) + str(',') +
                str(cm.status) + str(',') + str(timedelta(seconds=end_time - start_time)) +
                str(',') + str(end_time - start_time) + '\n')
            # permutation vector p - graph index and vector p
            arq_model_list.write(str(i0+1) + str(',') + str(fileiras) + '\n')

        else:
            # id graph, f(x) Objective function, Problem Status, time, time
            arq_model.write(
                str(i0+1) + str(',') + str(int(cm.ObjVal)) + str(',') +
                str(cm.status) + str(',') + str(timedelta(seconds=end_time - start_time)) +
                str(',') + str(end_time - start_time) + str('ERROR') + '\n')
            # permutation vector p - graph index and vector p
            arq_model_list.write(str(i0+1) + str(',') + str(fileiras) + '\n')
        '''

        if cm.status == gp.GRB.OPTIMAL:
            # Solução ótima encontrada
            arq_model.write(
                f"{i0 + 1},{int(cm.ObjVal)},{cm.status},{timedelta(seconds=end_time - start_time)},{end_time - start_time}\n")
            arq_model_list.write(f"{i0 + 1},{fileiras}\n")

        elif cm.status == gp.GRB.INFEASIBLE:
            # Problema inviável
            arq_model.write(
                f"{i0 + 1},INFEASIBLE,{cm.status},{timedelta(seconds=end_time - start_time)},{end_time - start_time}\n")
            arq_model_list.write(f"{i0 + 1},INFEASIBLE\n")

        elif cm.status == gp.GRB.UNBOUNDED:
            # Problema ilimitado
            arq_model.write(
                f"{i0 + 1},UNBOUNDED,{cm.status},{timedelta(seconds=end_time - start_time)},{end_time - start_time}\n")
            arq_model_list.write(f"{i0 + 1},UNBOUNDED\n")

        else:
            # Outro status (inclui casos como interrupção por tempo, etc.)
            arq_model.write(
                f"{i0 + 1},UNKNOWN_STATUS,{cm.status},{timedelta(seconds=end_time - start_time)},{end_time - start_time}\n")
            arq_model_list.write(f"{i0 + 1},UNKNOWN_STATUS\n")

        # Close the archive
        arq_model.close()
        arq_model_list.close()


# Run program
if __name__ == "__main__":
    main()
