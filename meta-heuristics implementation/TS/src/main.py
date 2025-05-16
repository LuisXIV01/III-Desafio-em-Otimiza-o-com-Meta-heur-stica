import sys
import time
import matplotlib.pyplot as plt
from common import read_jobshop_instance, write_output
from solver import Solver
import numpy as np

def main(instance_path):
    """
    Main entry point of the program. Reads a job shop instance from the file at
    `instance_path`, solves it using the `Solver` class, and writes the solution to
    a file.

    Args:
        instance_path (str): Path to the file containing the job shop instance.
    """
    jobs, num_jobs, num_machines = read_jobshop_instance(instance_path)

    solver = Solver(jobs, num_jobs, num_machines)
    history = solver.fitness_history
    start = time.time()
    solution = solver.solve()
    elapsed = time.time() - start

    write_output(solution, instance_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <instance_path>")
        sys.exit(1)

    main(sys.argv[1])
