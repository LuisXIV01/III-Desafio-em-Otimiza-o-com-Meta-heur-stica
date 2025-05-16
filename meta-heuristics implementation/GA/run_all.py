#!/usr/bin/env python3
import json
import subprocess
import os
import time

# Configurações
JSON_PATH    = "responses.json"
SOLVER_CMD   = ["python", "src/main.py"]
CHECKER_CMD  = ["python", "checker.py"]
INPUT_DIR    = "data"
OUTPUT_DIR   = "output"

def main():
    # Garante que a pasta de saída existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Carrega instâncias e ótimos/bounds
    with open(JSON_PATH, encoding="utf-8") as f:
        instances = json.load(f)

    # Cabeçalho
    print(f"{'Instância':<12} {'Ótimo Esperado':<15} {'Tempo (s)':<10} Resultado")
    print("-" * 70)

    for inst in instances:
        name    = inst["name"]
        # monta string de “ótimo esperado” ou “[lower…upper]”
        if "optimum" in inst and inst["optimum"] is not None:
            expected = str(inst["optimum"])
        else:
            b    = inst.get("bounds", {})
            lower = b.get("lower", "?")
            upper = b.get("upper", "?")
            expected = f"[{lower}…{upper}]"

        input_file  = os.path.join(INPUT_DIR,  f"{name}")
        output_file = os.path.join(OUTPUT_DIR, f"{name}.out.txt")

        # 1) Roda o solver (que já gera output_file)
        t0 = time.perf_counter()
        solver = subprocess.run(
            SOLVER_CMD + [input_file],
            capture_output=True, text=True
        )
        t1 = time.perf_counter()
        elapsed = t1 - t0
        if solver.returncode != 0:
            result = f"ERRO solver: {solver.stderr.strip()}"
        else:
            # 2) Roda o checker
            checker = subprocess.run(
                CHECKER_CMD + [input_file, output_file],
                capture_output=True, text=True
            )
            if checker.returncode != 0:
                result = f"ERRO checker: {checker.stderr.strip()}"
            else:
                # Pega última linha da saída do checker
                result = checker.stdout.strip().splitlines()[-1]

        print(f"{name:<12} {expected:<15} {elapsed:<10.2f} {result}")

if __name__ == "__main__":
    main()
