import random
from tqdm import tqdm
from common import read_jobshop_instance, write_output

# Genetic algorithm parameters
TAM_POP = 50
IT_MAX = 500
MUTATION_RATE = 0.01

class Solver:
    def __init__(self, jobs, num_jobs, num_machines):
        """
        Initializes a Solver instance for a job shop scheduling problem.

        Args:
            jobs (list[list[tuple[int, int]]]): A list of jobs, where each job is a list of
                (machine, duration) pairs.
            num_jobs (int): The number of jobs.
            num_machines (int): The number of machines.
        """
        self.jobs = jobs
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.schedule = []
        self.history = []

    def solve(self):
        # Build initial sequence of job indices (each job repeated for its operations)
        seq = []
        for j, ops in enumerate(self.jobs):
            seq.extend([j] * len(ops))

        # Run genetic algorithm to get best sequence
        best_fitness, best_seq = self._ga(seq)

        # Convert best sequence to concrete schedule: (job, op_idx, machine, start, duration)
        end_time_job = [0] * self.num_jobs
        end_time_mac = [0] * self.num_machines
        op_counter = [0] * self.num_jobs
        schedule = []
        for job in best_seq:
            op_idx = op_counter[job]
            machine, duration = self.jobs[job][op_idx]
            start = max(end_time_job[job], end_time_mac[machine])
            end = start + duration
            end_time_job[job] = end_time_mac[machine] = end
            schedule.append((job, op_idx, machine, start, duration))
            op_counter[job] += 1

        self.schedule = schedule
        return schedule

    def _fitness(self, seq):
        # Computes makespan for a given sequence
        end_time_job = [0] * self.num_jobs
        end_time_mac = [0] * self.num_machines
        op_counter = [0] * self.num_jobs
        makespan = 0
        for job in seq:
            op_idx = op_counter[job]
            machine, duration = self.jobs[job][op_idx]
            start = max(end_time_job[job], end_time_mac[machine])
            end = start + duration
            end_time_job[job] = end_time_mac[machine] = end
            makespan = max(makespan, end)
            op_counter[job] += 1
        return makespan

    def _crossover(self, p1, p2):
        n = len(p1)
        c1, c2 = sorted(random.sample(range(n), 2))
        child1 = [-1] * n
        child2 = [-1] * n
        count1 = [0] * self.num_jobs
        count2 = [0] * self.num_jobs

        # Copy segments
        for i in range(c1, c2 + 1):
            child1[i] = p1[i]
            child2[i] = p2[i]
            count1[p1[i]] += 1
            count2[p2[i]] += 1

        # Fill remainder by order
        idx = 0
        for gene in p2:
            while idx < n and child1[idx] != -1:
                idx += 1
            if idx < n and count1[gene] < self.jobs[gene].__len__():
                child1[idx] = gene
                count1[gene] += 1
        idx = 0
        for gene in p1:
            while idx < n and child2[idx] != -1:
                idx += 1
            if idx < n and count2[gene] < self.jobs[gene].__len__():
                child2[idx] = gene
                count2[gene] += 1

        return child1, child2

    def _mutate(self, seq):
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(seq)), 2)
            seq[i], seq[j] = seq[j], seq[i]
        return seq

    def _initial_population(self, seq):
        # Generate initial population of random permutations
        population = []
        for _ in range(TAM_POP):
            indiv = seq.copy()
            random.shuffle(indiv)
            population.append((self._fitness(indiv), indiv))
        return population

    def _tournament(self, pop):
        participants = random.sample(pop, 2)
        return min(participants, key=lambda x: x[0])[1]

    def _ga(self, seq):
        pop = self._initial_population(seq)
        pop.sort(key=lambda x: x[0])
        best = pop[0]
        bar = tqdm(range(IT_MAX), desc='GA', unit='gen')
        for _ in bar:
            # Elitismo
            parents = [pop[0][1], pop[1][1]]
            candidates = pop[2:]
            # Torneio
            for _ in range(TAM_POP - 2):
                parents.append(self._tournament(pop))

            new_pop = []
            # Crossover e mutate
            for i in range(0, TAM_POP, 2):
                p1 = parents[i]
                p2 = parents[(i + 1) % len(parents)]
                c1, c2 = self._crossover(p1, p2)
                c1 = self._mutate(c1)
                c2 = self._mutate(c2)
                new_pop.append((self._fitness(c1), c1))
                new_pop.append((self._fitness(c2), c2))

            pop = sorted(new_pop, key=lambda x: x[0])
            self.history.append(pop[0][0])
            if pop[0][0] < best[0]:
                best = pop[0]

        return best  
