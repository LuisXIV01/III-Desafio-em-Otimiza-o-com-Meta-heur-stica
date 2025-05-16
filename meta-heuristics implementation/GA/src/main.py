import sys
import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from common import read_jobshop_instance, write_output
from solver import Solver

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
    start = time.time()
    solution = solver.solve()
    elapsed = time.time() - start
    write_output(solution, instance_path)
    print(f"Tempo de execução: {elapsed:.3f} segundos")

    history = solver.history

    """fig = go.Figure(
        data=go.Scatter(
            x=list(range(len(history))),
            y=history,
            mode='lines+markers',
            hovertemplate='Geração %{x}<br>Makespan %{y}<extra></extra>'
        )
    )
    fig.update_layout(
        title='Convergência do Best Makespan',
        xaxis_title='Geração',
        yaxis_title='Makespan',
        template='plotly_white'
    )

    out_html = "makespan_history.html"
    fig.write_html(out_html, auto_open=True)
    print(f"Gráfico interativo salvo em: {out_html}")"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <instance_path>")
        sys.exit(1)

    main(sys.argv[1])
