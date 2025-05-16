# III Desafio em Otimização com Meta-heurística

# Sumário

- [Equipe](#equipe)
- [1. Como é formado o vetor‑solução](#1-como-é-formado-o-vetor‑solução)
- [2. Função de avaliação (`_fitness`)](#2-função-de-avaliação-_fitness)
- [3. Método principal (`solve`)](#3-método-principal-solve)
- [4. Algoritmo Genético](#4-algoritmo-genético)
    - [Funcionamento do Algoritmo Genético (`_ga`)](#funcionamento-do-algoritmo-genético-_ga)
    - [Operadores Genéticos Usados](#operadores-genéticos-usados)
    - [Critério de Parada](#critério-de-parada)
    - [Testes](#testes)
- [5. Tabu Search](#5-tabu-search)
    - [Funacionamento do Tabu Search (`_ts`)](#funcionamento-do-tabu-search-_ts)
        - [Passos principais do TS implementado](#passos-principais-do-ts-implementado)
    - [Testes](#testes-1)

---
## Equipe

[![LuisXIV01](https://github.com/LuisXIV01.png?size=100)](https://github.com/LuisXIV01)
[![ManelHRO](https://github.com/ManelHRO.png?size=100)](https://github.com/ManelHRO)

---

## 1. Como é formado o vetor‑solução

```text
Exemplo de entrada (3 jobs × 3 máquinas)
Job 0 → [(M0, 3), (M1, 2), (M2, 2)]  # 3 operações
Job 1 → [(M0, 2), (M2, 1), (M1, 4)]  # 3 operações
Job 2 → [(M1, 4), (M2, 3)]           # 2 operações
```

1. **Construção do vetor base**
   Repetimos o índice de cada job tantas vezes quanto o número de operações dele:

```python
seq = [0, 0, 0, 1, 1, 1, 2, 2]  # 3 + 3 + 2 = 8 posições
```

2. **Permutação = indivíduo**
   O algoritmo usa esse vetor para formar a solução.
   A posição no vetor indica **qual operação (0, 1, 2,…) daquele job** será executada quando chegar a vez dele:

```text
Indivíduo = [1, 2, 0, 1, 0, 2, 0, 1]

Leitura:
 index 0 → Job 1, operação 0
 index 1 → Job 2, operação 0
 index 2 → Job 0, operação 0
 index 3 → Job 1, operação 1
 … e assim por diante
```

> ✅ **Por que isso funciona?**
> Toda vez que um job aparece, avançamos um contador interno (`op_counter[job]`) para saber qual operação dele escalonar. Assim, cada job respeita sua ordem interna sem precisar codificar máquinas explicitamente no cromossomo.

---

## 2. Função de avaliação (`_fitness`)

```python
def _fitness(self, seq):
    end_time_job = [0] * self.num_jobs      # último término de cada job
    end_time_mac = [0] * self.num_machines  # último término de cada máquina
    op_counter = [0] * self.num_jobs        # qual operação de cada job já foi agendada
    makespan = 0

    for job in seq:                  # percorre o vetor na ordem
        op_idx = op_counter[job]     # operação corrente do job
        machine, duration = self.jobs[job][op_idx]
        start = max(end_time_job[job], end_time_mac[machine])
        end = start + duration

        # atualiza cronogramas parciais
        end_time_job[job] = end
        end_time_mac[machine] = end
        makespan = max(makespan, end)
        op_counter[job] += 1

    return makespan  # menor é melhor
```

**O que ela faz?**

* **Simula** a execução das operações na sequência proposta.
* Mantém o horário de término **por job** e **por máquina** para garantir precedência e indisponibilidade.
* O retorno é o *makespan* final, usado como pontuação no algoritmo (menor = melhor).

---

## 3. Método principal (`solve`)

```python
def solve(self):
    # 1. Cria vetor base
    seq = []
    for j, ops in enumerate(self.jobs):
        seq.extend([j] * len(ops))

    # 2. Executa GA → melhor sequência
    best_fit, best_seq = self._ga(seq)

    # 3. Converte sequência em cronograma detalhado
    #    (job, op_idx, machine, start, duration)
    ...
    return self.schedule
```

1. **Geração do vetor base** — como descrito na seção 1.
2. **Otimização** — chama o algoritmo meta-heurístico, no exemplo `self._ga`, que executa forma uma solução.
3. **Decodificação** — apos escolher o melhor vetor, reconstrói um cronograma completo, salvando em `self.schedule`.

---

## 4. Algoritmo Genético

| Parâmetro       | Significado                         |
| --------------- | ----------------------------------- |
| `TAM_POP`       | Tamanho da população                |
| `IT_MAX`        | Nº de gerações                      |
| `MUTATION_RATE` | Probabilidade de mutar um indivíduo |

> Esses valores são ajustados conforme o tamanho/complexidade da instância.

---

### Funcionamento do Algoritmo Genético (`_ga`)

O Algoritmo Genético (GA) é uma meta-heurística inspirada no processo natural da evolução, buscando soluções melhores ao longo das gerações.

**Passos principais do GA implementado:**
1. **População inicial:**
Gera uma população de soluções aleatórias, embaralhando o vetor base para criar diversidade.

2. **Avaliação da população:**
Cada indivíduo (sequência) é avaliado pela função `_fitness`, que retorna o *makespan* (menor é melhor).

3. **Seleção por torneio:**
Seleciona pares de indivíduos para cruzamento, escolhendo os melhores dentre competidores aleatórios.

4. **Crossover (recombinação):**
Combina dois pais para gerar dois filhos, trocando segmentos do vetor para misturar características.

5. **Mutação:**
Aplica pequenas alterações aleatórias (troca de posições) nos filhos para aumentar a diversidade.

6. **Elitismo:**
Mantém os melhores indivíduos da geração atual para a próxima, garantindo que a qualidade não diminua.

7. **Repetição:**
Repete o processo por um número fixo de gerações (`IT_MAX`), buscando melhora contínua.

### Operadores Genéticos Usados
#### Crossover
- Seleciona dois pontos aleatórios no vetor.

- Copia o segmento entre esses pontos do pai 1 para o filho 1, e do pai 2 para o filho 2.

- Preenche as posições restantes do filho com os genes do outro pai, respeitando a quantidade de operações de cada job.

#### Mutação
- Com baixa probabilidade (`MUTATION_RATE`), troca duas posições aleatórias no vetor para explorar novas soluções.

### Critério de Parada
O algoritmo termina ao alcançar o número máximo de gerações (`IT_MAX`) e retorna o melhor indivíduo encontrado.

### Testes

| Parâmetro       | Significado                         | Valor Padrão |
| --------------- | ----------------------------------- | ------------ |
| `TAM_POP`       | Tamanho da população                | `50`         |
| `IT_MAX`        | Nº de gerações                      | `500`        |
| `MUTATION_RATE` | Probabilidade de mutar um indivíduo | `0.01`       |

![Convergência do Best Makespan](meta-heuristics%20implementation/GA/image/abz9-50-500.png)
*Imagem 1: Convergência do Best Makespan do caso `abz9` - (melhor global: 1020)*

![Convergência do Best Makespan](meta-heuristics%20implementation/GA/image/la17-50-500.png)
*Imagem 2: Convergência do Best Makespan do caso `la17` - (melhor global: 862)*

![Convergência do Best Makespan](meta-heuristics%20implementation/GA/image/ta38-50-500.png)
*Imagem 3: Convergência do Best Makespan do caso `ta38` - (melhor global: 2694)*

---

#### Testes rodados com todos os casos

| Instância | Ótimo Esperado | Tempo (s) | Resultado           |
|-----------|----------------|-----------|---------------------|
| abz5      | 1234           | 9.82      | ⏱️ Makespan: 1366    |
| abz6      | 943            | 9.73      | ⏱️ Makespan: 1028    |
| abz7      | 656            | 26.18     | ⏱️ Makespan: 948     |
| abz8      | [645…665]      | 24.50     | ⏱️ Makespan: 1002    |
| abz9      | [661…679]      | 26.68     | ⏱️ Makespan: 994     |
| ft06      | 55             | 5.15      | ⏱️ Makespan: 55      |
| ft10      | 930            | 9.63      | ⏱️ Makespan: 1062    |
| ft20      | 1165           | 9.74      | ⏱️ Makespan: 1318    |
| la01      | 666            | 6.14      | ⏱️ Makespan: 682     |
| la02      | 655            | 6.46      | ⏱️ Makespan: 732     |
| la03      | 597            | 6.53      | ⏱️ Makespan: 664     |
| la04      | 590            | 6.67      | ⏱️ Makespan: 634     |
| la05      | 593            | 6.22      | ⏱️ Makespan: 593     |
| la06      | 926            | 8.39      | ⏱️ Makespan: 935     |
| la07      | 890            | 7.97      | ⏱️ Makespan: 930     |
| la08      | 863            | 8.01      | ⏱️ Makespan: 884     |
| la09      | 951            | 7.70      | ⏱️ Makespan: 993     |
| la10      | 958            | 7.96      | ⏱️ Makespan: 958     |
| la11      | 1222           | 9.93      | ⏱️ Makespan: 1264    |
| la12      | 1039           | 9.50      | ⏱️ Makespan: 1060    |
| la13      | 1150           | 10.15     | ⏱️ Makespan: 1180    |
| la14      | 1292           | 9.50      | ⏱️ Makespan: 1292    |
| la15      | 1207           | 9.62      | ⏱️ Makespan: 1388    |
| la16      | 945            | 9.68      | ⏱️ Makespan: 1062    |
| la17      | 784            | 10.10     | ⏱️ Makespan: 876     |
| la18      | 848            | 11.24     | ⏱️ Makespan: 904     |
| la19      | 842            | 11.85     | ⏱️ Makespan: 966     |
| la20      | 902            | 10.19     | ⏱️ Makespan: 1074    |
| la21      | 1046           | 13.55     | ⏱️ Makespan: 1331    |
| la22      | 927            | 12.85     | ⏱️ Makespan: 1155    |
| la23      | 1032           | 13.77     | ⏱️ Makespan: 1181    |
| la24      | 935            | 14.44     | ⏱️ Makespan: 1173    |
| la25      | 977            | 15.09     | ⏱️ Makespan: 1182    |
| la26      | 1218           | 18.49     | ⏱️ Makespan: 1518    |
| la27      | 1235           | 18.36     | ⏱️ Makespan: 1652    |
| la28      | 1216           | 17.90     | ⏱️ Makespan: 1740    |
| la29      | 1152           | 16.72     | ⏱️ Makespan: 1627    |
| la30      | 1355           | 18.12     | ⏱️ Makespan: 1740    |
| la31      | 1784           | 25.61     | ⏱️ Makespan: 2234    |
| la32      | 1850           | 26.62     | ⏱️ Makespan: 2271    |
| la33      | 1719           | 25.02     | ⏱️ Makespan: 2074    |
| la34      | 1721           | 24.51     | ⏱️ Makespan: 2233    |
| la35      | 1888           | 25.30     | ⏱️ Makespan: 2405    |
| la36      | 1268           | 20.69     | ⏱️ Makespan: 1600    |
| la37      | 1397           | 19.47     | ⏱️ Makespan: 1794    |
| la38      | 1196           | 19.28     | ⏱️ Makespan: 1569    |
| la39      | 1233           | 20.05     | ⏱️ Makespan: 1706    |
| la40      | 1222           | 19.82     | ⏱️ Makespan: 1615    |
| orb01     | 1059           | 10.57     | ⏱️ Makespan: 1239    |
| orb02     | 888            | 10.79     | ⏱️ Makespan: 983     |
| orb03     | 1005           | 11.07     | ⏱️ Makespan: 1308    |
| orb04     | 1005           | 10.94     | ⏱️ Makespan: 1191    |
| orb05     | 887            | 11.13     | ⏱️ Makespan: 1013    |
| orb06     | 1010           | 10.60     | ⏱️ Makespan: 1266    |
| orb07     | 397            | 10.72     | ⏱️ Makespan: 449     |
| orb08     | 899            | 11.70     | ⏱️ Makespan: 1102    |
| orb09     | 934            | 10.87     | ⏱️ Makespan: 1073    |
| orb10     | 944            | 11.66     | ⏱️ Makespan: 1108    |
| swv01     | 1407           | 17.92     | ⏱️ Makespan: 2178    |
| swv02     | 1475           | 19.09     | ⏱️ Makespan: 2232    |
| swv03     | [1369…1398]    | 19.35     | ⏱️ Makespan: 2086    |
| swv04     | [1450…1474]    | 18.48     | ⏱️ Makespan: 2129    |
| swv05     | 1424           | 18.25     | ⏱️ Makespan: 2259    |
| swv06     | [1591…1678]    | 25.10     | ⏱️ Makespan: 2654    |
| swv07     | [1446…1600]    | 26.54     | ⏱️ Makespan: 2512    |
| swv08     | [1640…1763]    | 28.60     | ⏱️ Makespan: 2856    |
| swv09     | [1604…1661]    | 28.77     | ⏱️ Makespan: 2697    |
| swv10     | [1631…1767]    | 28.12     | ⏱️ Makespan: 2662    |
| swv11     | [2983…2991]    | 42.93     | ⏱️ Makespan: 4940    |
| swv12     | [2972…3003]    | 43.38     | ⏱️ Makespan: 4758    |
| swv13     | 3104           | 43.41     | ⏱️ Makespan: 5390    |
| swv14     | 2968           | 47.49     | ⏱️ Makespan: 5090    |
| swv15     | [2885…2904]    | 46.66     | ⏱️ Makespan: 4846    |
| swv16     | 2924           | 47.82     | ⏱️ Makespan: 3641    |
| swv17     | 2794           | 45.12     | ⏱️ Makespan: 3464    |
| swv18     | 2852           | 45.31     | ⏱️ Makespan: 3554    |
| swv19     | 2843           | 46.74     | ⏱️ Makespan: 3804    |
| swv20     | 2823           | 46.26     | ⏱️ Makespan: 3410    |
| yn1       | [826…885]      | 37.28     | ⏱️ Makespan: 1303    |
| yn2       | [861…909]      | 38.53     | ⏱️ Makespan: 1311    |
| yn3       | [827…892]      | 38.08     | ⏱️ Makespan: 1323    |
| yn4       | [918…968]      | 38.04     | ⏱️ Makespan: 1404    |
| ta01      | 1231           | 20.68     | ⏱️ Makespan: 1743    |
| ta02      | 1244           | 20.50     | ⏱️ Makespan: 1653    |
| ta03      | 1218           | 20.69     | ⏱️ Makespan: 1669    |
| ta04      | 1175           | 22.92     | ⏱️ Makespan: 1609    |
| ta05      | 1224           | 23.80     | ⏱️ Makespan: 1587    |
| ta06      | 1238           | 24.57     | ⏱️ Makespan: 1741    |
| ta07      | 1227           | 15.76     | ⏱️ Makespan: 1670    |
| ta08      | 1217           | 11.91     | ⏱️ Makespan: 1591    |
| ta09      | 1274           | 14.50     | ⏱️ Makespan: 1704    |
| ta10      | 1241           | 14.76     | ⏱️ Makespan: 1728    |
| ta11      | [1323…1361]    | 19.21     | ⏱️ Makespan: 2122    |
| ta12      | [1351…1367]    | 12.02     | ⏱️ Makespan: 2006    |
| ta13      | [1282…1342]    | 11.91     | ⏱️ Makespan: 1864    |
| ta14      | 1345           | 16.19     | ⏱️ Makespan: 1841    |
| ta15      | [1304…1340]    | 15.59     | ⏱️ Makespan: 2122    |
| ta16      | [1302…1360]    | 15.67     | ⏱️ Makespan: 1990    |
| ta17      | 1462           | 14.11     | ⏱️ Makespan: 2076    |
| ta18      | [1369…1396]    | 12.92     | ⏱️ Makespan: 1846    |
| ta19      | [1297…1335]    | 11.67     | ⏱️ Makespan: 2140    |
| ta20      | [1318…1351]    | 12.64     | ⏱️ Makespan: 1968    |
| ta21      | [1539…1644]    | 18.95     | ⏱️ Makespan: 2453    |
| ta22      | [1511…1600]    | 15.48     | ⏱️ Makespan: 2551    |
| ta23      | [1472…1557]    | 20.56     | ⏱️ Makespan: 2218    |
| ta24      | [1602…1647]    | 17.74     | ⏱️ Makespan: 2426    |
| ta25      | [1504…1595]    | 16.53     | ⏱️ Makespan: 2435    |
| ta26      | [1539…1645]    | 14.84     | ⏱️ Makespan: 2459    |
| ta27      | [1616…1680]    | 19.29     | ⏱️ Makespan: 2592    |
| ta28      | [1591…1614]    | 19.52     | ⏱️ Makespan: 2532    |
| ta29      | [1514…1635]    | 19.10     | ⏱️ Makespan: 2477    |
| ta30      | [1473…1584]    | 18.76     | ⏱️ Makespan: 2544    |
| ta31      | 1764           | 20.77     | ⏱️ Makespan: 2647    |
| ta32      | [1774…1796]    | 19.03     | ⏱️ Makespan: 2869    |
| ta33      | [1778…1793]    | 23.23     | ⏱️ Makespan: 2721    |
| ta34      | [1828…1829]    | 23.91     | ⏱️ Makespan: 2893    |
| ta35      | 2007           | 20.85     | ⏱️ Makespan: 2830    |
| ta36      | 1819           | 23.69     | ⏱️ Makespan: 2854    |
| ta37      | [1771…1778]    | 25.74     | ⏱️ Makespan: 2844    |
| ta38      | 1673           | 23.62     | ⏱️ Makespan: 2817    |
| ta39      | 1795           | 22.28     | ⏱️ Makespan: 2681    |
| ta40      | [1631…1674]    | 19.52     | ⏱️ Makespan: 2747    |
| ta41      | [1859…2018]    | 30.02     | ⏱️ Makespan: 3370    |
| ta42      | [1867…1956]    | 32.46     | ⏱️ Makespan: 3226    |
| ta43      | [1809…1859]    | 32.43     | ⏱️ Makespan: 3013    |
| ta44      | [1927…1984]    | 27.88     | ⏱️ Makespan: 3357    |
| ta45      | [1997…2000]    | 29.12     | ⏱️ Makespan: 3278    |
| ta46      | [1940…2021]    | 30.13     | ⏱️ Makespan: 3363    |
| ta47      | [1789…1903]    | 26.82     | ⏱️ Makespan: 3010    |
| ta48      | [1912…1952]    | 34.17     | ⏱️ Makespan: 3021    |
| ta49      | [1915…1968]    | 26.70     | ⏱️ Makespan: 3227    |
| ta50      | [1807…1926]    | 29.89     | ⏱️ Makespan: 3137    |
| ta51      | 2760           | 37.06     | ⏱️ Makespan: 4372    |
| ta52      | 2756           | 34.59     | ⏱️ Makespan: 4361    |
| ta53      | 2717           | 35.00     | ⏱️ Makespan: 4058    |
| ta54      | 2839           | 41.60     | ⏱️ Makespan: 4018    |
| ta55      | 2679           | 38.05     | ⏱️ Makespan: 4299    |
| ta56      | 2781           | 44.74     | ⏱️ Makespan: 4103    |
| ta57      | 2943           | 31.45     | ⏱️ Makespan: 4294    |
| ta58      | 2885           | 34.21     | ⏱️ Makespan: 4633    |
| ta59      | 2655           | 38.15     | ⏱️ Makespan: 4171    |
| ta60      | 2723           | 38.91     | ⏱️ Makespan: 4112    |
| ta61      | 2868           | 43.66     | ⏱️ Makespan: 5027    |
| ta62      | 2869           | 45.54     | ⏱️ Makespan: 5056    |
| ta63      | 2755           | 46.88     | ⏱️ Makespan: 4849    |
| ta64      | 2702           | 50.73     | ⏱️ Makespan: 4432    |
| ta65      | 2725           | 51.04     | ⏱️ Makespan: 4719    |
| ta66      | 2845           | 50.89     | ⏱️ Makespan: 4829    |
| ta67      | 2825           | 37.39     | ⏱️ Makespan: 4990    |
| ta68      | 2784           | 39.11     | ⏱️ Makespan: 4770    |
| ta69      | 3071           | 37.80     | ⏱️ Makespan: 4790    |
| ta70      | 2995           | 45.11     | ⏱️ Makespan: 4888    |
| ta71      | [None…None]    | 74.42     | ⏱️ Makespan: 8487    |
| ta72      | [None…None]    | 74.45     | ⏱️ Makespan: 8229    |
| ta73      | [None…None]    | 92.83     | ⏱️ Makespan: 8417    |
| ta74      | [None…None]    | 112.53    | ⏱️ Makespan: 8539    |
| ta75      | [None…None]    | 110.54    | ⏱️ Makespan: 8598    |
| ta76      | [None…None]    | 90.41     | ⏱️ Makespan: 8611    |
| ta77      | [None…None]    | 101.34    | ⏱️ Makespan: 8655    |
| ta78      | [None…None]    | 90.15     | ⏱️ Makespan: 8097    |
| ta79      | [None…None]    | 85.87     | ⏱️ Makespan: 8534    |
| ta80      | [None…None]    | 123.03    | ⏱️ Makespan: 8398    |

---

## 5. Tabu Search
| Parâmetro       | Significado                         |
| --------------- | ----------------------------------- |
| `BAN`           | Valor de bloqueio (tabu)            |
| `MAX_ITER`      | Nº máximo de iterações              |
> Esses valores são ajustados conforme o tamanho/complexidade da instância.

### Funcionamento do Tabu Search (`_TS`)
Funcionamento do Tabu Search (tabu_search)
O Tabu Search (TS) é uma meta-heurística baseada em exploração local, que utiliza memória de curto prazo para evitar ciclos e diversificar a busca por boas soluções.

#### Passos principais do TS implementado:

1. **Geração da solução inicial:**

    Cria uma permutação aleatória do vetor base usando `first_solution()`.
    
    Essa solução serve tanto como a “corrente” quanto como “melhor até agora” (`current_solution` e `best_solution`).

2. **Avaliação e inicialização:**

    Calcula o fitness (*makespan*) da solução corrente via `fitness()`.

    Define `fitness_current` e `fitness_best` com esse valor.

    Inicializa a grade tabu (`tabu_grid`) marcando todos os movimentos como permitidos.

    Cria uma fila (`list_grid`) para armazenar movimentos e seus tempos de banimento.

3. **Geração de vizinhança:**

    Em cada iteração, chama `get_neighbors()` para obter todos os vizinhos por swap adjacente e as posições trocadas correspondentes.

4. **Seleção de movimento:**

    Para cada vizinho, avalia seu fitness:

    Movimento não–tabu e melhora sobre fitness_current: aceita imediatamente, marca o swap como tabu e adiciona (x, y, ban) em `list_grid`.

    Movimento tabu, mas que melhora `fitness_current` (critérios de aspiração): aceita mesmo assim e repete o processo de marcação.

    Caso não seja aceito, armazena em `aux_neighbors` para possível aceitação de solução pior.

5. **Aceitação de solução pior (diversificação):**

    Se nenhum movimento foi aceito e um número aleatório em `[0,1)` excede 0.70, escolhe o melhor candidato de aux_neighbors (o “menos ruim”) e o aceita, marcando-o tabu.

6. **Atualização do tabu:**

    Executa `decrease_ban()`, que decrementa o contador de cada entrada em `list_grid` e libera movimentos cujo banimento chegou a zero, removendo sua marcação em `tabu_grid.`

7. **Atualização do melhor global (intensificação):**

    Se o fitness da solução corrente ficar abaixo de `fitness_best`, atualiza `best_solution` e `fitness_best`.

8. **Critério de parada:**

    Repete os passos de 3 a 7 até alcançar max_iter iterações.

### Testes
