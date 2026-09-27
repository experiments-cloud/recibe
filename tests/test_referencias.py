"""Evalúa cada problema de referencia como si fuera la respuesta de un modelo.

Todos deben tener sintaxis válida, ser resolubles, tener un plan válido en la
referencia y coincidir con ella.

  python3 tests/test_referencias.py
"""
import argparse, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import yaml
from evaluate import evaluate_one

ap = argparse.ArgumentParser()
ap.add_argument("--config", default=os.path.join(ROOT, "config.yaml"))
a = ap.parse_args()
cfg = yaml.safe_load(open(a.config))
cdir = os.path.dirname(os.path.abspath(a.config))
for k in ("fast_downward", "val"):
    cfg[k] = os.path.normpath(os.path.join(cdir, cfg[k]))
fails = 0
man = [m for m in json.load(open(os.path.join(ROOT, "data", "manifest.json"))) if m["role"] == "test"]
for m in man:
    ref = open(os.path.join(ROOT, "data", "problems", m["domain"], m["id"] + ".pddl")).read()
    for lang, tags in (("es", ("[INICIO_PROBLEMA]", "[FIN_PROBLEMA]")), ("en", ("[BEGIN_PROBLEM]", "[END_PROBLEM]"))):
        rec = {"run_id": f"ref|{m['id']}|{lang}", "status": "ok", "lang": lang, "domain": m["domain"],
               "problem": m["id"], "text": f"Claro.\n{tags[0]}\n```pddl\n{ref}\n```\n{tags[1]}"}
        row, _ = evaluate_one((rec, cfg))
        ok = all(row[k] for k in ("sintaxis_ok", "resoluble", "plan_valido_ref", "exacto"))
        if not ok:
            fails += 1
            print("FALLA", m["id"], lang, {k: row[k] for k in ("fd_rc", "sintaxis_ok", "resoluble", "plan_valido_ref", "exacto")})
    print(f"{m['id']}: plan de {row['long_plan']} pasos")
print("todas las referencias pasan" if fails == 0 else f"{fails} fallas")
sys.exit(1 if fails else 0)
