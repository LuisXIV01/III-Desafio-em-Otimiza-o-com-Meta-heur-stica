import sys
import random
import time
from collections import deque
import matplotlib.pyplot as plt
from typing import List, Tuple

class Solver:
    def __init__(self, jobs: List[List[Tuple[int, int]]], num_jobs: int, num_machines: int, ban: int = 3, max_iter: int = 500):
        self.jobs = jobs
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.ban = ban
        self.max_iter = max_iter
        self.fitness_history: List[int] = []
        self.schedule: List[Tuple[int, int, int, int, int]] = []

    def _fitness(self, order: List[int]) -> int:
        end_job = [0] * self.num_jobs
        end_mac = [0] * self.num_machines
        op_idx = [0] * self.num_jobs

        for job in order:
            op = op_idx[job]
            machine, dur = self.jobs[job][op]
            start = max(end_job[job], end_mac[machine])
            finish = start + dur
            end_job[job] = finish
            end_mac[machine] = finish
            op_idx[job] += 1

        return max(end_mac)

    def _neighbors(self, order: List[int]) -> Tuple[List[List[int]], List[Tuple[int, int]]]:
        neighs, swaps = [], []
        for i in range(1, len(order)):
            aux = order.copy()
            aux[i], aux[i - 1] = aux[i - 1], aux[i]
            neighs.append(aux)
            swaps.append((i - 1, i))
        return neighs, swaps

    def _order_to_schedule(self, order: List[int]) -> List[Tuple[int, int, int, int, int]]:
        end_job = [0] * self.num_jobs
        end_mac = [0] * self.num_machines
        op_idx = [0] * self.num_jobs
        schedule = []

        for job in order:
            op = op_idx[job]
            machine, dur = self.jobs[job][op]
            start = max(end_job[job], end_mac[machine])
            finish = start + dur
            end_job[job] = finish
            end_mac[machine] = finish
            op_idx[job] += 1
            schedule.append((job, op, machine, start, dur))

        return schedule

    def solve(self) -> List[Tuple[int, int, int, int, int]]:
        order = [j for j in range(self.num_jobs) for _ in range(self.num_machines)]
        random.shuffle(order)

        best = current = order[:]
        fit_best = fit_curr = self._fitness(current)
        self.fitness_history.append(fit_best)

        tabu = [[False] * len(order) for _ in range(len(order))]
        queue = deque()

        for _ in range(self.max_iter):
            neighbors, swaps = self._neighbors(current)
            improved = False

            for neigh, (a, b) in zip(neighbors, swaps):
                fit_neigh = self._fitness(neigh)
                if not tabu[a][b] and fit_neigh < fit_curr:
                    current, fit_curr = neigh, fit_neigh
                    tabu[a][b] = True
                    queue.append((a, b, self.ban))
                    improved = True
                    break
                elif tabu[a][b] and fit_neigh < fit_best:
                    current, fit_curr = neigh, fit_neigh
                    improved = True
                    break

            if not improved:
                fit_vals = [self._fitness(n) for n in neighbors]
                idx = fit_vals.index(min(fit_vals))
                current = neighbors[idx]
                fit_curr = fit_vals[idx]

            for _ in range(len(queue)):
                i, j, t = queue.popleft()
                if t > 1:
                    queue.append((i, j, t - 1))
                else:
                    tabu[i][j] = False

            if fit_curr < fit_best:
                best, fit_best = current[:], fit_curr

            self.fitness_history.append(fit_best)

        self.schedule = self._order_to_schedule(best)
        return self.schedule

    def print_schedule(self):
        for job, op, mac, start, dur in self.schedule:
            print(f"job {job}, Op{op} -> Machine {mac} | Start: {start}, Duration: {dur}")
        makespan = max(start + dur for *_, start, dur in self.schedule)
        print(f"\nFitness (makespan): {makespan}")


# Exemplo de uso
if __name__ == "__main__":
    num_jobs = 5
    num_machines = 3
    random.seed(42)

    jobs = [
        [(random.randrange(num_machines), random.randint(1, 10)) for _ in range(num_machines)]
        for _ in range(num_jobs)
    ]

    solver = Solver(jobs, num_jobs, num_machines, ban=3, max_iter=100)
    solver.solve()
    solver.print_schedule()
    solver.plot_fitness()
