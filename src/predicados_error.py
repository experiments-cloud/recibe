"""Cuenta qué predicados se omiten o se agregan de más en el :init de las salidas
incorrectas, y qué tipos de objeto se declaran mal.

Lee results/evaluacion.csv y los archivos de results/problemas_generados/.
Escribe en results/analisis/:
  predicados_error.csv   una fila por modelo, dominio, estilo y predicado
  tipos_error.csv        una fila por modelo, dominio, tipo correcto y tipo declarado
  predicados_error.md    resumen

Uso:  python3 src/predicados_error.py [--resultados results]
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pddl_utils import PDDLParseError, parse_problem  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resultados", default=os.path.join(ROOT, "results"))
    ap.add_argument("--modelos", nargs="*", help="limitar a estos modelos")
    args = ap.parse_args()
    res = args.resultados
    gen_dir = os.path.join(res, "problemas_generados")
    out = os.path.join(res, "analisis")
    os.makedirs(out, exist_ok=True)

    d = pd.read_csv(os.path.join(res, "evaluacion.csv"))
    d["ex"] = d["exacto"].astype(bool) & d["sintaxis_ok"].astype(bool)
    d = d[~d["ex"] & d["parse_propio_ok"].astype(bool)]
    if args.modelos:
        d = d[d["model"].isin(args.modelos)]

    refs = {}
    omit = defaultdict(Counter)       # (modelo, dominio, estilo) -> predicado -> hechos omitidos
    extra = defaultdict(Counter)
    n_out = Counter()
    types = Counter()                 # (modelo, dominio, tipo de referencia, tipo declarado) -> objetos
    missing_files = 0
    for _, r in d.iterrows():
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", r["run_id"])
        path = os.path.join(gen_dir, safe + ".pddl")
        if not os.path.exists(path):
            missing_files += 1
            continue
        key = (r["model"], r["domain"], r["style"])
        if r["problem"] not in refs:
            refs[r["problem"]] = parse_problem(open(os.path.join(ROOT, "data", "problems", r["domain"],
                                                                  r["problem"] + ".pddl")).read())
        ref = refs[r["problem"]]
        try:
            gen = parse_problem(open(path).read())
        except PDDLParseError:
            continue
        n_out[key] += 1
        for a in ref["init"] - gen["init"]:
            omit[key][a[0]] += 1
        for a in gen["init"] - ref["init"]:
            extra[key][a[0]] += 1
        for o, t in ref["objects"].items():
            g = gen["objects"].get(o)
            if g is not None and g != t:
                types[(r["model"], r["domain"], t, g)] += 1

    rows = []
    for key in sorted(n_out):
        preds = set(omit[key]) | set(extra[key])
        for p in sorted(preds):
            rows.append({"modelo": key[0], "dominio": key[1], "estilo": key[2], "predicado": p,
                         "salidas incorrectas": n_out[key],
                         "hechos omitidos": omit[key][p], "hechos extra": extra[key][p],
                         "omitidos por salida": round(omit[key][p] / n_out[key], 2),
                         "extra por salida": round(extra[key][p] / n_out[key], 2)})
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(out, "predicados_error.csv"), index=False)
    tt = pd.DataFrame([{"modelo": k[0], "dominio": k[1], "tipo correcto": k[2], "tipo declarado": k[3],
                        "objetos": v} for k, v in sorted(types.items())])
    tt.to_csv(os.path.join(out, "tipos_error.csv"), index=False)

    md = ["# Predicados y tipos en las salidas incorrectas", "",
          f"Salidas incorrectas analizadas: {sum(n_out.values())}. Archivos no encontrados: {missing_files}.", ""]
    if not t.empty:
        agg = (t.groupby(["modelo", "dominio", "predicado"])[["hechos omitidos", "hechos extra"]].sum()
               .reset_index())
        tot = t.drop_duplicates(["modelo", "dominio", "estilo"]).groupby(["modelo", "dominio"])[
            "salidas incorrectas"].sum().rename("salidas incorrectas").reset_index()
        agg = agg.merge(tot, on=["modelo", "dominio"])
        agg["% de los omitidos"] = (100 * agg["hechos omitidos"] /
                                    agg.groupby(["modelo", "dominio"])["hechos omitidos"].transform("sum")
                                    ).round(1)
        agg["% de los extra"] = (100 * agg["hechos extra"] /
                                 agg.groupby(["modelo", "dominio"])["hechos extra"].transform("sum")).round(1)
        agg = agg.fillna(0)
        md += ["## Hechos de :init omitidos y extra, por modelo, dominio y predicado (todos los estilos)", "",
               agg.to_markdown(index=False), ""]
    if not tt.empty:
        md += ["## Objetos declarados con un tipo distinto al de la referencia", "", tt.to_markdown(index=False), ""]
    open(os.path.join(out, "predicados_error.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"Resultados en {out}")


if __name__ == "__main__":
    main()
