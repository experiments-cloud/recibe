"""Envía las descripciones a los modelos y guarda cada respuesta en results/respuestas.jsonl.

Las corridas ya completadas se omiten, así que el programa se puede interrumpir
y volver a ejecutar.

  python3 src/run_experiment.py
  python3 src/run_experiment.py --modelos gemini-3.8-flash --estilos indirecto
"""
import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm import Client, LLMError  # noqa: E402
from pddl_utils import parse_problem, write_problem  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def domain_name(domain_text):
    m = re.search(r"\(\s*domain\s+([^\s\)]+)", domain_text, re.I)
    return m.group(1) if m else "domain"


def build_prompt(template_dir, prompt_id, lang, domain_text, description, example=None):
    base = open(os.path.join(template_dir, f"p0_{lang}.txt"), encoding="utf-8").read()
    ej = ""
    if prompt_id == "P1":
        ej = open(os.path.join(template_dir, f"ejemplo_{lang}.txt"), encoding="utf-8").read()
        ej = ej.replace("{EJ_DESCRIPCION}", example[0].strip()).replace("{EJ_PROBLEMA}", example[1])
    # el dominio se envía sin comentarios
    domain_text = "\n".join(l for l in re.sub(r";[^\n]*", "", domain_text).splitlines() if l.strip())
    return (base.replace("{EJEMPLO}", ej)
                .replace("{DOMINIO}", domain_text.strip())
                .replace("{DESCRIPCION}", description.strip()))


def worked_example(domain, style, lang):
    desc = open(os.path.join(DATA, "examples", f"{domain}-ex__{style}__{lang}.txt"), encoding="utf-8").read()
    ref = parse_problem(open(os.path.join(DATA, "problems", domain, f"{domain}-ex.pddl")).read())
    dname = domain_name(open(os.path.join(DATA, "domains", f"{domain}.pddl")).read()).lower()
    return desc, write_problem(f"{domain}-ejemplo", dname, ref["objects"], ref["init"], ref["goal"])


def is_truncated(rec):
    fr = str(rec.get("finish_reason") or "").lower()
    return fr in ("length", "max_tokens", "finishreason.max_tokens")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(ROOT, "config.yaml"))
    ap.add_argument("--modelos", nargs="*", help="etiquetas de los modelos (por defecto, todos)")
    ap.add_argument("--estilos", nargs="*", help="estilos de descripción (por defecto, los de config.yaml)")
    ap.add_argument("--rehacer-truncadas", action="store_true",
                    help="volver a pedir las respuestas cortadas por el límite max_tokens")
    ap.add_argument("--hilos", type=int, default=2, help="llamadas simultáneas")
    ap.add_argument("--salida", default=os.path.join(ROOT, "results", "respuestas.jsonl"))
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    manifest = [m for m in json.load(open(os.path.join(DATA, "manifest.json")))
                if m["role"] == "test" and m["domain"] in cfg["dominios"]]
    models = cfg["modelos"]
    if args.modelos:
        models = [m for m in models if m["etiqueta"] in args.modelos]

    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    done = set()
    if os.path.exists(args.salida):
        for line in open(args.salida, encoding="utf-8"):
            r = json.loads(line)
            if r.get("status") != "ok":
                continue
            # Solo se repiten las respuestas cortadas por max_tokens. Una respuesta vacía
            # que el modelo terminó por sí mismo se conserva como error del modelo.
            if args.rehacer_truncadas and is_truncated(r):
                continue
            done.add(r["run_id"])

    tdir = os.path.join(ROOT, "prompts")
    jobs = []
    for spec in models:
        for pr in cfg["prompts"]:
            for lang in cfg["idiomas"]:
                for style in (args.estilos or cfg["estilos"]):
                    for m in manifest:
                        for rep in range(1, cfg["repeticiones"] + 1):
                            rid = f"{spec['etiqueta']}|{pr}|{lang}|{style}|{m['id']}|r{rep}"
                            if rid not in done:
                                jobs.append((spec, pr, lang, style, m, rep, rid))
    print(f"{len(jobs)} llamadas pendientes, {len(done)} ya completadas")
    if not jobs:
        return

    lock = threading.Lock()
    clients = {}

    def get_client(spec):
        with lock:
            if spec["etiqueta"] not in clients:
                s = dict(spec)
                s.setdefault("temperature", cfg.get("temperatura"))
                s.setdefault("max_tokens", cfg.get("max_tokens", 4096))
                clients[spec["etiqueta"]] = Client(s)
            return clients[spec["etiqueta"]]

    def work(job):
        spec, pr, lang, style, m, rep, rid = job
        dom = m["domain"]
        dtext = open(os.path.join(DATA, "domains", f"{dom}.pddl"), encoding="utf-8").read()
        desc = open(os.path.join(DATA, "descriptions", f"{m['id']}__{style}__{lang}.txt"), encoding="utf-8").read()
        example = worked_example(dom, style, lang) if pr == "P1" else None
        prompt = build_prompt(tdir, pr, lang, dtext, desc, example)
        rec = {"run_id": rid, "model": spec["etiqueta"], "prompt": pr, "lang": lang, "style": style,
               "domain": dom, "problem": m["id"], "rep": rep,
               "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "prompt_chars": len(prompt)}
        try:
            rec.update(get_client(spec).generate(prompt))
            rec["status"] = "ok"
        except Exception as e:  # noqa: BLE001
            rec.update({"status": "error", "error": f"{type(e).__name__}: {e}"[:500]})
        return rec

    for spec in {s["etiqueta"]: s for s, *_ in jobs}.values():
        try:
            get_client(spec)
        except LLMError as e:
            sys.exit(f"{spec['etiqueta']}: {e}")

    t0 = time.time()
    n = errors = 0
    with ThreadPoolExecutor(max_workers=max(1, args.hilos)) as ex, open(args.salida, "a", encoding="utf-8") as f:
        for fut in as_completed([ex.submit(work, j) for j in jobs]):
            rec = fut.result()
            with lock:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
            n += 1
            if rec["status"] != "ok":
                errors += 1
                if errors <= 3:
                    print(f"  error en {rec['run_id']}: {rec['error'][:200]}")
            if n % 25 == 0 or n == len(jobs):
                print(f"  {n}/{len(jobs)}  {time.time() - t0:.0f} s  errores: {errors}")
    if errors:
        print(f"{errors} llamadas fallaron; al ejecutar de nuevo el programa se vuelven a pedir.")


if __name__ == "__main__":
    main()
