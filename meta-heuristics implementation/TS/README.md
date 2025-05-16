# Smart Job X

Este projeto contém um template inicial para resolver o problema de **Job Shop Scheduling**. Ele implementa a estrutura básica que organiza as operações de um conjunto de jobs em uma sequência que pode ser validada.

## Como Funciona

### Estrutura do Projeto

O projeto é dividido em alguns módulos principais:

1. **`main.py`**: O script principal que leitura da instância de entrada, chama o solver e escreve a solução em um arquivo de saída.
2. **`solver.py`**: Contém a lógica para resolver o problema de escalonamento de operações para cada job, além de funções para verificar a validade do agendamento.
3. **`checker.py`**: Utiliza a solução gerada pelo `solver.py` e a valida contra possíveis erros, como:
   - **Operações repetidas**: Verifica se a mesma operação foi agendada mais de uma vez para o mesmo job.
   - **Faltam ou sobram operações**: Checa se todas as operações para os jobs estão agendadas e se não há operações extras.
   - **Conflitos de máquina**: Verifica se duas operações que precisam ser executadas na mesma máquina não se sobrepõem.
4. **`common.py`**: Contém funções auxiliares para ler e escrever as instâncias de entrada e as soluções geradas.
5. **`write_output.py`**: Função para salvar a solução gerada em um arquivo de saída.
6. **`read_input.py`**: Função para ler a instância de entrada do arquivo de entrada.
7. **`optimum.py`**: Mostra a solução otima para o problema se não existir uma solução otima conhecida mostra o lower bound e o upper bound.

### Fluxo de Execução

1. **Leitura da Instância de Entrada**: A instância do problema é lida a partir de um arquivo de entrada. Este arquivo contém a lista de jobs e suas respectivas operações (máquina e duração).
2. **Solução do Problema**: O solver gera um agendamento de operações baseado na instância fornecida. Ele tenta escalonar todas as operações de maneira que respeite a ordem entre elas e os tempos de execução nas máquinas.

3. **Validação da Solução**: A solução gerada é validada no módulo `checker.py`. A validação inclui:

   - **Verificação de Duplicatas**: Verifica se não existem operações repetidas.
   - **Verificação de Operações Faltantes ou Extras**: Garante que todas as operações necessárias estão presentes e que não há operações desnecessárias.
   - **Verificação de Conflitos de Máquina**: Verifica se duas operações na mesma máquina não se sobrepõem no tempo.

4. **Saída**: A solução válida (se não houver erros) é salva em um arquivo de saída.

### Como Rodar o Projeto

Para rodar o projeto, siga os seguintes passos:

1. **Instale as dependências**:

   Este projeto não requer dependências externas específicas, mas certifique-se de ter Python 3.x instalado.

2. **Arquivo de entrada**:

   - A primeira linha contém dois números inteiros: o número de jobs e o número de máquinas.
   - As linhas subsequentes descrevem as operações de cada job. Para cada job, as operações são listadas em pares de inteiros (máquina, duração).

   Exemplo de entrada:

   ```
    4 4 # 4 jobs, 4 machines
    4 88 8 68 6 94 # job 0 -> (job 0 | machine:4 duration:88, ...)
    5 72 3 50 6 69 # job 1 -> (job 1 | machine:5 duration:72, ...)
    9 83 8 61 0 83 # job 2 -> (job 2 | machine:9 duration:83, ...)
    7 94 2 68 1 61 # job 3 -> (job 3 | machine:7 duration:94, ...)
   ```

3. **Arquivo de saída**:

   - O arquivo de saída contém a solução gerada pelo solver. Cada linha representa uma operação e contém uma quintupla de inteiros: job, operação, máquina, tempo de inicio e duração.

   Exemplo de saída:

   ```
    0 0 0 0 5  # Job 0, Op 0 -> Machine 0 | Start: 0, Duration: 5
    1 0 1 0 3  # Job 1, Op 0 -> Machine 1 | Start: 0, Duration: 3
    2 0 0 5 4  # Job 2, Op 0 -> Machine 0 | Start: 5, Duration: 4
    0 1 1 3 6  # Job 0, Op 1 -> Machine 1 | Start: 3, Duration: 6
    1 1 0 3 7  # Job 1, Op 1 -> Machine 0 | Start: 3, Duration: 7
    2 1 1 9 2  # Job 2, Op 1 -> Machine 1 | Start: 9, Duration: 2
   ```

4. **Rodar o Solver**:

   Para gerar a solução, execute o script `main.py`:

   ```bash
   python src/main.py data/instancia.txt
   ```

   Onde `instancia.txt` é o arquivo de entrada.

5. **Validar a Solução**:

   Para validar a solução gerada, execute o script `checker.py`:

   ```bash
   python checker.py data/instancia.txt output/solucao.txt
   ```

   Onde `solucao.txt` é o arquivo de saída gerado pelo solver.

   Se não houver conflitos, a validação irá retornar "✅ Solução válida", caso contrário, indicará os problemas encontrados.

## References

- J. Adams, E. Balas, D. Zawack. "The shifting bottleneck procedure for job shop scheduling.", Management Science, Vol. 34, Issue 3, pp. 391-401, 1988.
- J.F. Muth, G.L. Thompson. "Industrial scheduling.", Englewood Cliffs, NJ, Prentice-Hall, 1963.
- S. Lawrence. "Resource constrained project scheduling: an experimental investigation of heuristic scheduling techniques (Supplement).", Graduate School of Industrial Administration. Pittsburgh, Pennsylvania, Carnegie-Mellon University, 1984.
- D. Applegate, W. Cook. "A computational study of job-shop scheduling.", ORSA Journal on Computer, Vol. 3, Isuue 2, pp. 149-156, 1991.
- R.H. Storer, S.D. Wu, R. Vaccari. "New search spaces for sequencing problems with applications to job-shop scheduling.", Management Science Vol. 38, Issue 10, pp. 1495-1509, 1992.
- T. Yamada, R. Nakano. "A genetic algorithm applicable to large-scale job-shop problems.", Proceedings of the Second international workshop on parallel problem solving from Nature (PPSN'2). Brussels (Belgium), pp. 281-290, 1992.
- E. Taillard. "Benchmarks for basic scheduling problems", European Journal of Operational Research, Vol. 64, Issue 2, pp. 278-285, 1993.
- tamy0612. JSPLIB. https://github.com/tamy0612/JSPLIB.git
