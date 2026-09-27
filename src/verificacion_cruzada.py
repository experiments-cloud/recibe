"""Verificación cruzada entre modelos (análisis posterior).

Para cada salida de un modelo "objetivo", la compara con la salida de un modelo
"verificador" para el mismo caso (prompt, idioma, estilo, problema y repetición).
La salida se acepta solo si ambas declaran los mismos objetos y tipos, y los
mismos hechos en :init y :goal. Si no coinciden, o si alguna de las dos no
tiene archivo, la salida queda marcada para revisión.

No hace llamadas a ningún modelo: usa results/evaluacion.csv y los archivos de
results/problemas_generados/.

Para cada par (objetivo, verificador) reporta:
  aceptadas          % de salidas del objetivo que se aceptan
  error residual     % de las aceptadas que no son una coincidencia exacta
  errores detectados % de las salidas incorrectas del objetivo que quedan marcadas
  falsas alarmas     % de las salidas correctas del objetivo que quedan marcadas

Uso:  python3 src/verificacion_cruzada.py [--resultados results]
"""
import argparse
import os
import re
import sys
from itertools import permutations

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pddl_utils import PDDLParseError, parse_problem  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = ["prompt", "lang", "style", "problem", "rep"]


def load_facts(gen_dir, run_id, cache):
    if run_id in cache:
        return cache[run_id]
    path = os.path.join(gen_dir, re.sub(r"[^A-Za-z0-9_.-]+", "_", run_id) + ".pddl")
    val = None
    if os.path.exists(path):
        try:
            p = parse_problem(open(path).read())
            val = (tuple(sorted(p["objects"].items())), frozenset(p["init"]), frozenset(p["goal"]))
        except PDDLParseError:
            val = None
    cache[run_id] = val
    return val


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultados", default=os.path.join(ROOT, "results"))
    args = ap.parse_args()
    res = args.resultados
    gen_dir = os.path.join(res, "problemas_generados")
    out = os.path.join(res, "analisis")
    os.makedirs(out, exist_ok=True)

    d = pd.read_csv(os.path.join(res, "evaluacion.csv"))
    d["ex"] = d["exacto"].astype(bool) & d["sintaxis_ok"].astype(bool)
    d["valida"] = d["sintaxis_ok"].astype(bool) & d["resoluble"].astype(bool)
    models = list(dict.fromkeys(d["model"]))
    cache = {}
    d["hechos"] = [load_facts(gen_dir, r, cache) for r in d["run_id"]]
    by_model = {m: d[d.model == m].set_index(KEYS) for m in models}

    rows = []
    for target, checker in permutations(models, 2):
        t = by_model[target]
        c = by_model[checker].reindex(t.index)
        agree = [(a is not None) and (a == b) for a, b in zip(t["hechos"], c["hechos"])]
        agree = pd.Series(agree, index=t.index)
        for regla, acepta in [("solo planificador", t["valida"]),
                              ("coincidencia con verificador", agree),
                              ("planificador + coincidencia", t["valida"] & agree)]:
            n = len(t)
            acc = acepta.astype(bool)
            correct = t["ex"]
            rows.append({
                "objetivo": target, "verificador": checker if regla != "solo planificador" else "(ninguno)",
                "regla": regla, "salidas": n,
                "aceptadas (%)": pct(acc.sum(), n),
                "error residual en aceptadas (%)": pct((acc & ~correct).sum(), acc.sum()),
                "errores detectados (%)": pct((~acc & ~correct).sum(), (~correct).sum()),
                "falsas alarmas (%)": pct((~acc & correct).sum(), correct.sum()),
                "errores del objetivo": int((~correct).sum()),
            })
    t = pd.DataFrame(rows).drop_duplicates(subset=["objetivo", "verificador", "regla"])
    t.to_csv(os.path.join(out, "verificacion_cruzada.csv"), index=False)
    md = ["# Verificación cruzada entre modelos", "",
          "Una salida se acepta si su archivo coincide hecho por hecho con el del verificador "
          "para el mismo caso. La regla 'solo planificador' acepta toda salida con sintaxis válida y resoluble.", "",
          t.to_markdown(index=False), ""]
    open(os.path.join(out, "verificacion_cruzada.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"Resultados en {out}")


if __name__ == "__main__":
    main()
