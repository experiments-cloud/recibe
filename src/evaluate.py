"""Evalúa las respuestas de results/respuestas.jsonl y escribe results/evaluacion.csv.

Columnas principales:
  extraido         la respuesta contiene un bloque (define ...)
  sintaxis_ok      el traductor de Fast Downward acepta el dominio y el problema
  resoluble        Fast Downward encuentra un plan dentro del límite de tiempo
  plan_valido_ref  VAL acepta ese plan en el problema de referencia
  exacto           objetos con sus tipos, :init y :goal iguales a la referencia
  init_f1, goal_f1 F1 por hecho
  error_principal  primera falla encontrada en el orden anterior

Los problemas extraídos se guardan en results/problemas_generados/.

  python3 src/evaluate.py [--procesos 1]
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pddl_utils import PDDLParseError, extract_problem_text, parse_problem  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FD_TRANSLATE_ERRORS = {30, 31, 36}   # códigos de salida de Fast Downward por errores de entrada


def prf(gen, ref):
    tp = len(gen & ref)
    p = tp / len(gen) if gen else (1.0 if not ref else 0.0)
    r = tp / len(ref) if ref else 1.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return round(p, 4), round(r, 4), round(f, 4)


def run_fd(fd, alias, tlimit, domain, problem, workdir):
    plan = os.path.join(workdir, "plan.txt")
    cmd = [sys.executable, fd, "--alias", alias, "--plan-file", plan,
           "--overall-time-limit", f"{tlimit}s", domain, problem]
    try:
        p = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=tlimit + 30)
        rc, log = p.returncode, p.stdout[-3000:] + p.stderr[-2000:]
    except subprocess.TimeoutExpired:
        rc, log = 23, "tiempo agotado"
    plan_text = open(plan).read() if os.path.exists(plan) else None
    return rc, plan_text, log


def run_val(val, domain, problem, plan_path):
    try:
        p = subprocess.run([val, domain, problem, plan_path], capture_output=True, text=True, timeout=60)
        out = p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return False, "timeout"
    return ("Plan valid" in out), out[-1500:]


def evaluate_one(args):
    rec, cfg = args
    dom, pid = rec["domain"], rec["problem"]
    dom_path = os.path.join(DATA, "domains", f"{dom}.pddl")
    ref_path = os.path.join(DATA, "problems", dom, f"{pid}.pddl")
    ref = parse_problem(open(ref_path).read())
    row = {k: rec.get(k) for k in ("run_id", "model", "prompt", "lang", "style", "domain", "problem", "rep",
                                    "model_version", "tokens_in", "tokens_out", "latency_s")}
    row.update({"llamada_ok": rec.get("status") == "ok", "extraido": False, "modo_extraccion": None,
                "parse_propio_ok": False, "sintaxis_ok": False, "fd_rc": None, "resoluble": False,
                "long_plan": None, "plan_valido_ref": False, "objetos_ok": False, "init_ok": False,
                "goal_ok": False, "exacto": False, "init_p": 0.0, "init_r": 0.0, "init_f1": 0.0,
                "goal_p": 0.0, "goal_r": 0.0, "goal_f1": 0.0, "n_init_omitidos": None,
                "n_init_extra": None, "n_goal_omitidos": None, "n_goal_extra": None,
                "n_obj_tipo_erroneo": None, "n_obj_faltantes": None, "n_obj_extra": None,
                "error_principal": None})
    if not row["llamada_ok"]:
        row["error_principal"] = "fallo_api"
        return row, None
    text, how = extract_problem_text(rec.get("text"), rec["lang"])
    row["modo_extraccion"] = how
    if not text:
        row["error_principal"] = "sin_pddl"
        return row, None
    row["extraido"] = True

    # comparación de hechos
    gen = None
    try:
        gen = parse_problem(text)
        row["parse_propio_ok"] = True
    except PDDLParseError:
        pass
    if gen:
        ro, go = ref["objects"], gen["objects"]
        row["n_obj_faltantes"] = len(set(ro) - set(go))
        row["n_obj_extra"] = len(set(go) - set(ro))
        row["n_obj_tipo_erroneo"] = sum(1 for o in set(ro) & set(go) if ro[o] != go[o])
        row["objetos_ok"] = ro == go
        row["n_init_omitidos"] = len(ref["init"] - gen["init"])
        row["n_init_extra"] = len(gen["init"] - ref["init"])
        row["n_goal_omitidos"] = len(ref["goal"] - gen["goal"])
        row["n_goal_extra"] = len(gen["goal"] - ref["goal"])
        row["init_ok"] = gen["init"] == ref["init"] and gen["init_simple"]
        row["goal_ok"] = gen["goal"] == ref["goal"] and gen["goal_simple"]
        row["init_p"], row["init_r"], row["init_f1"] = prf(gen["init"], ref["init"])
        row["goal_p"], row["goal_r"], row["goal_f1"] = prf(gen["goal"], ref["goal"])
        row["exacto"] = row["objetos_ok"] and row["init_ok"] and row["goal_ok"]

    # planificador y validador
    wd = tempfile.mkdtemp(prefix="ev_")
    try:
        prob_path = os.path.join(wd, "problem.pddl")
        open(prob_path, "w").write(text + "\n")
        rc, plan, log = run_fd(cfg["fast_downward"], cfg["fd_alias"], cfg["fd_tiempo_limite_s"],
                               dom_path, prob_path, wd)
        row["fd_rc"] = rc
        row["sintaxis_ok"] = rc not in FD_TRANSLATE_ERRORS
        row["resoluble"] = rc == 0 and plan is not None
        if row["resoluble"]:
            row["long_plan"] = len([l for l in plan.splitlines() if l.startswith("(")])
            ok, _ = run_val(cfg["val"], dom_path, ref_path, os.path.join(wd, "plan.txt"))
            row["plan_valido_ref"] = ok
        saved = text
    finally:
        shutil.rmtree(wd, ignore_errors=True)

    # error principal: la primera falla en el orden de la evaluación
    if row["exacto"]:
        row["error_principal"] = None
    elif not row["sintaxis_ok"]:
        row["error_principal"] = "sintaxis"
    elif gen and (row["n_obj_faltantes"] or row["n_obj_extra"] or row["n_obj_tipo_erroneo"]):
        row["error_principal"] = "objetos_o_tipos"
    elif gen and row["n_init_omitidos"] and not row["n_init_extra"]:
        row["error_principal"] = "init_hechos_omitidos"
    elif gen and row["n_init_extra"] and not row["n_init_omitidos"]:
        row["error_principal"] = "init_hechos_extra"
    elif gen and row["n_init_extra"] and row["n_init_omitidos"]:
        row["error_principal"] = "init_hechos_cambiados"
    elif gen and not row["goal_ok"]:
        row["error_principal"] = "meta"
    else:
        row["error_principal"] = "otro"
    return row, saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(ROOT, "config.yaml"))
    ap.add_argument("--entrada", default=os.path.join(ROOT, "results", "respuestas.jsonl"))
    ap.add_argument("--salida", default=os.path.join(ROOT, "results", "evaluacion.csv"))
    ap.add_argument("--procesos", type=int, default=2)
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    cdir = os.path.dirname(os.path.abspath(args.config))
    for k in ("fast_downward", "val"):
        cfg[k] = os.path.normpath(os.path.join(cdir, cfg[k]))
        if not os.path.exists(cfg[k]):
            sys.exit(f"no se encontró {k}: {cfg[k]}")

    # si una corrida aparece varias veces, se usa la última respuesta exitosa
    recs = {}
    for line in open(args.entrada, encoding="utf-8"):
        r = json.loads(line)
        if r["run_id"] not in recs or r.get("status") == "ok":
            recs[r["run_id"]] = r
    recs = list(recs.values())
    print(f"{len(recs)} respuestas")

    outdir = os.path.join(os.path.dirname(args.salida), "problemas_generados")
    os.makedirs(outdir, exist_ok=True)

    # las salidas idénticas para el mismo problema se evalúan una sola vez
    groups = {}
    for r in recs:
        text = extract_problem_text(r.get("text"), r["lang"])[0] if r.get("status") == "ok" else None
        key = (r["problem"], r.get("status"), hashlib.sha1((text or "").encode()).hexdigest())
        groups.setdefault(key, []).append(r)
    reps_ = [g[0] for g in groups.values()]
    print(f"{len(reps_)} salidas distintas")
    per_fields = ("run_id", "model", "prompt", "lang", "style", "rep", "model_version",
                  "tokens_in", "tokens_out", "latency_s")
    rows = []
    with ProcessPoolExecutor(max_workers=args.procesos) as ex:
        for i, (g, (row, text)) in enumerate(zip(groups.values(),
                                                 ex.map(evaluate_one, [(r, cfg) for r in reps_], chunksize=4))):
            for r in g:
                rr = dict(row)
                for k in per_fields:
                    rr[k] = r.get(k)
                ext = extract_problem_text(r.get("text"), r["lang"])[1] if r.get("status") == "ok" else None
                rr["modo_extraccion"] = ext
                rows.append(rr)
                if text:
                    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", r["run_id"])
                    open(os.path.join(outdir, safe + ".pddl"), "w").write(text + "\n")
            if (i + 1) % 100 == 0:
                print(f"  {i + 1}/{len(reps_)}")
    rows.sort(key=lambda r: r["run_id"])
    with open(args.salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Resultados en {args.salida}")


if __name__ == "__main__":
    main()
