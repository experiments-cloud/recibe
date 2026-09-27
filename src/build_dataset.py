"""Genera data/ a partir de los problemas de referencia.

Copia los problemas de Blocksworld, Logistics y Depots de pddl-instances,
genera los de ambulance con una semilla fija y escribe las descripciones en
español e inglés en los estilos explicito, implicito (este archivo) e
indirecto (indirect.py).

  python3 src/build_dataset.py --ipc ../tools/pddl-instances
"""
import argparse
import json
import os
import random
import shutil
from collections import defaultdict

from pddl_utils import parse_problem, write_problem
import indirect

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# La primera instancia de cada lista es el ejemplo del prompt P1; las otras 10 son de prueba.
IPC = {
    "blocksworld": ("ipc-2000/domains/blocks-strips-typed",
                    ["instance-2", "instance-6", "instance-3", "instance-9", "instance-1",
                     "instance-10", "instance-7", "instance-12", "instance-17", "instance-16",
                     "instance-13"]),
    "logistics": ("ipc-2000/domains/logistics-strips-typed",
                  ["instance-1", "instance-2", "instance-3", "instance-4", "instance-5",
                   "instance-6", "instance-7", "instance-8", "instance-11", "instance-13",
                   "instance-15"]),
    "depots": ("ipc-2002/domains/depots-strips-automatic",
               ["instance-1", "instance-2", "instance-3", "instance-4", "instance-7",
                "instance-5", "instance-10", "instance-8", "instance-6", "instance-11",
                "instance-13"]),
}


# utilidades de redacción
def join(items, lang):
    items = list(items)
    conj = " y " if lang == "es" else " and "
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + conj + items[-1]


def num(n, lang):
    es = ["cero", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho",
          "nueve", "diez", "once", "doce", "trece", "catorce", "quince"]
    en = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
          "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen"]
    lst = es if lang == "es" else en
    return lst[n] if n < len(lst) else str(n)


def cap(s):
    return s[0].upper() + s[1:]


def bullets(lines):
    return "\n".join("- " + l for l in lines)


def natural_sort(xs):
    import re
    return sorted(xs, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)])


# Sustantivos por tipo: (singular, plural, artículo_sg, artículo_pl)
NOUNS = {
    "es": {
        "block": ("bloque", "bloques", "el", "los"),
        "truck": ("camión", "camiones", "el", "los"),
        "airplane": ("avión", "aviones", "el", "los"),
        "package": ("paquete", "paquetes", "el", "los"),
        "airport": ("aeropuerto", "aeropuertos", "el", "los"),
        "location": ("ubicación", "ubicaciones", "la", "las"),
        "city": ("ciudad", "ciudades", "la", "las"),
        "depot": ("depósito", "depósitos", "el", "los"),
        "distributor": ("distribuidor", "distribuidores", "el", "los"),
        "hoist": ("grúa", "grúas", "la", "las"),
        "pallet": ("tarima", "tarimas", "la", "las"),
        "crate": ("caja", "cajas", "la", "las"),
        "ambulance": ("ambulancia", "ambulancias", "la", "las"),
        "patient": ("paciente", "pacientes", "el", "los"),
    },
    "en": {
        "block": ("block", "blocks", "the", "the"),
        "truck": ("truck", "trucks", "the", "the"),
        "airplane": ("airplane", "airplanes", "the", "the"),
        "package": ("package", "packages", "the", "the"),
        "airport": ("airport", "airports", "the", "the"),
        "location": ("location", "locations", "the", "the"),
        "city": ("city", "cities", "the", "the"),
        "depot": ("depot", "depots", "the", "the"),
        "distributor": ("distributor", "distributors", "the", "the"),
        "hoist": ("hoist", "hoists", "the", "the"),
        "pallet": ("pallet", "pallets", "the", "the"),
        "crate": ("crate", "crates", "the", "the"),
        "ambulance": ("ambulance", "ambulances", "the", "the"),
        "patient": ("patient", "patients", "the", "the"),
    },
}


def np(obj, objs, lang, article=True):
    """'el camión tru1' / 'the truck tru1'."""
    t = objs[obj]
    sg, _, art, _ = NOUNS[lang][t]
    return f"{art} {sg} {obj}" if article else f"{sg} {obj}"


def np_group(names, typ, lang):
    """'los paquetes obj1 y obj2' / 'el paquete obj1'."""
    sg, pl, a1, a2 = NOUNS[lang][typ]
    names = natural_sort(names)
    if len(names) == 1:
        return f"{a1} {sg} {names[0]}"
    return f"{a2} {pl} {join(names, lang)}"


def del_(phrase):
    """Contracciones del español: 'a el' -> 'al', 'de el' -> 'del'."""
    return phrase.replace(" a el ", " al ").replace(" de el ", " del ")


def object_inventory(objs, lang, order):
    parts = []
    for t in order:
        names = natural_sort([o for o, tt in objs.items() if tt == t])
        if not names:
            continue
        sg, pl, _, _ = NOUNS[lang][t]
        if lang == "es":
            parts.append(f"{join(names, lang)} {'es un' if len(names) == 1 else 'son'} "
                         f"{sg if len(names) == 1 else pl}")
        else:
            parts.append(f"{join(names, lang)} {'is a' if len(names) == 1 else 'are'} "
                         f"{sg if len(names) == 1 else pl}")
    parts = [p.replace("es un ubicación", "es una ubicación").replace("es un ciudad", "es una ciudad")
              .replace("es un grúa", "es una grúa").replace("es un tarima", "es una tarima")
              .replace("es un caja", "es una caja").replace("es un ambulancia", "es una ambulancia")
              .replace("is a airplane", "is an airplane").replace("is a airport", "is an airport")
              .replace("is a ambulance", "is an ambulance") for p in parts]
    head = "Objetos: " if lang == "es" else "Objects: "
    return head + "; ".join(parts) + "."


# Blocksworld
def blocks_describe(p, style, lang):
    objs = p["objects"]
    B = lambda x: x.upper()
    blocks = natural_sort(objs)
    es = lang == "es"
    intro = (f"Hay {num(len(blocks), lang)} bloques: {join([B(b) for b in blocks], lang)}. "
             "Un brazo robótico puede tomar y sostener un bloque a la vez."
             if es else
             f"There are {num(len(blocks), lang)} blocks: {join([B(b) for b in blocks], lang)}. "
             "A robot arm can pick up and hold one block at a time.")
    if style == "explicito":
        init = []
        order = {"ontable": 0, "on": 1, "clear": 2, "holding": 3, "handempty": 4}
        for a in sorted(p["init"], key=lambda a: (order[a[0]], a)):
            if a[0] == "ontable":
                init.append(f"El bloque {B(a[1])} está sobre la mesa." if es else f"Block {B(a[1])} is on the table.")
            elif a[0] == "on":
                init.append(f"El bloque {B(a[1])} está sobre el bloque {B(a[2])}." if es else f"Block {B(a[1])} is on block {B(a[2])}.")
            elif a[0] == "clear":
                init.append(f"El bloque {B(a[1])} está despejado (no tiene nada encima)." if es else f"Block {B(a[1])} is clear (nothing is on top of it).")
            elif a[0] == "handempty":
                init.append("La mano del robot está vacía." if es else "The robot's hand is empty.")
            elif a[0] == "holding":
                init.append(f"El robot sostiene el bloque {B(a[1])}." if es else f"The robot is holding block {B(a[1])}.")
        goal = []
        for a in sorted(p["goal"]):
            if a[0] == "on":
                goal.append(f"El bloque {B(a[1])} debe estar sobre el bloque {B(a[2])}." if es else f"Block {B(a[1])} must be on block {B(a[2])}.")
            elif a[0] == "ontable":
                goal.append(f"El bloque {B(a[1])} debe estar sobre la mesa." if es else f"Block {B(a[1])} must be on the table.")
            elif a[0] == "clear":
                goal.append(f"El bloque {B(a[1])} debe quedar despejado." if es else f"Block {B(a[1])} must be clear.")
        h1, h2 = ("Estado inicial:", "Meta:") if es else ("Initial state:", "Goal:")
        return f"{intro}\n\n{h1}\n{bullets(init)}\n\n{h2}\n{bullets(goal)}\n"

    # implícito: pilas de abajo hacia arriba; 'clear' se deduce
    above = {a[2]: a[1] for a in p["init"] if a[0] == "on"}
    piles = []
    for b in natural_sort([a[1] for a in p["init"] if a[0] == "ontable"]):
        pile = [b]
        while pile[-1] in above:
            pile.append(above[pile[-1]])
        piles.append(pile)
    singles = [pl[0] for pl in piles if len(pl) == 1]
    towers = [pl for pl in piles if len(pl) > 1]
    sent = []
    if singles:
        if es:
            sent.append(f"{'El bloque' if len(singles) == 1 else 'Los bloques'} {join([B(s) for s in singles], lang)} "
                        f"{'está solo' if len(singles) == 1 else 'están cada uno solo'} sobre la mesa.")
        else:
            sent.append(f"{'Block' if len(singles) == 1 else 'Blocks'} {join([B(s) for s in singles], lang)} "
                        f"{'is' if len(singles) == 1 else 'are each'} alone on the table.")
    for t in towers:
        sent.append(f"Hay una pila formada, de abajo hacia arriba, por {join([B(x) for x in t], lang)}; {B(t[0])} está sobre la mesa."
                    if es else
                    f"There is a stack made of, from bottom to top, {join([B(x) for x in t], lang)}; {B(t[0])} is on the table.")
    held = [a[1] for a in p["init"] if a[0] == "holding"]
    if held:
        sent.append(f"El robot sostiene el bloque {B(held[0])}." if es else f"The robot is holding block {B(held[0])}.")
    else:
        sent.append("El robot no sostiene ningún bloque." if es else "The robot is not holding any block.")
    # meta: cadenas 'x sobre y'
    pairs = sorted([a for a in p["goal"] if a[0] == "on"], key=lambda a: a[1])
    below = {a[1]: a[2] for a in pairs}
    tops = [a[1] for a in pairs if a[1] not in {q[2] for q in pairs}]
    chunks = []
    for top in natural_sort(tops):
        cur = top
        while cur in below:
            nxt = below[cur]
            chunks.append(f"{B(cur)} sobre {B(nxt)}" if es else f"{B(cur)} on {B(nxt)}")
            cur = nxt
    extra = [a for a in p["goal"] if a[0] != "on"]
    for a in extra:
        if a[0] == "ontable":
            chunks.append(f"{B(a[1])} sobre la mesa" if es else f"{B(a[1])} on the table")
        elif a[0] == "clear":
            chunks.append(f"{B(a[1])} despejado" if es else f"{B(a[1])} clear")
    goal = (f"Al final se debe cumplir lo siguiente: {join(chunks, lang)}." if es else f"In the end the following must hold: {join(chunks, lang)}.")
    return f"{intro} {' '.join(sent)}\n\n{goal}\n"


# Logistics
def logistics_describe(p, style, lang):
    objs = p["objects"]
    es = lang == "es"
    if style == "explicito":
        inv = object_inventory(objs, lang, ["city", "location", "airport", "truck", "airplane", "package"])
        init = []
        order = {"in-city": 0, "at": 1, "in": 2}
        for a in sorted(p["init"], key=lambda a: (order[a[0]], a)):
            if a[0] == "in-city":
                init.append(cap(f"{np(a[1], objs, lang)} pertenece a {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} belongs to {np(a[2], objs, lang)}."))
            elif a[0] == "at":
                init.append(del_(cap(f"{np(a[1], objs, lang)} está en {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is at {np(a[2], objs, lang)}.")))
            elif a[0] == "in":
                init.append(del_(cap(f"{np(a[1], objs, lang)} está dentro de {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is inside {np(a[2], objs, lang)}.")))
        goal = [cap(f"{np(a[1], objs, lang)} debe estar en {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} must be at {np(a[2], objs, lang)}.")
                for a in sorted(p["goal"])]
        h1, h2 = ("Estado inicial:", "Meta:") if es else ("Initial state:", "Goal:")
        return f"{inv}\n\n{h1}\n{bullets(init)}\n\n{h2}\n{bullets(goal)}\n"

    cities = defaultdict(list)
    for a in p["init"]:
        if a[0] == "in-city":
            cities[a[2]].append(a[1])
    sent = []
    sent.append(f"Hay {num(len(cities), lang)} ciudades." if es else f"There are {num(len(cities), lang)} cities.")
    for c in natural_sort(cities):
        places = cities[c]
        locs = [x for x in places if objs[x] == "location"]
        apts = [x for x in places if objs[x] == "airport"]
        parts = []
        if locs:
            parts.append(np_group(locs, "location", lang))
        if apts:
            parts.append(np_group(apts, "airport", lang))
        sent.append(f"La ciudad {c} tiene {join(parts, lang)}." if es else f"City {c} has {join(parts, lang)}.")
    at = defaultdict(list)
    for a in p["init"]:
        if a[0] == "at":
            at[a[2]].append(a[1])
    for place in natural_sort(at):
        groups = []
        for t in ["truck", "airplane", "package"]:
            ns = [o for o in at[place] if objs[o] == t]
            if ns:
                groups.append(np_group(ns, t, lang))
        n_items = len(at[place])
        if es:
            sent.append(del_(f"En {np(place, objs, lang)} {'está' if n_items == 1 else 'están'} {join(groups, lang)}."))
        else:
            sent.append(f"At {np(place, objs, lang, article=False)} {'there is' if n_items == 1 else 'there are'} {join(groups, lang)}.")
    inside = defaultdict(list)
    for a in p["init"]:
        if a[0] == "in":
            inside[a[2]].append(a[1])
    for v in natural_sort(inside):
        sent.append(cap(f"{np(v, objs, lang)} lleva {np_group(inside[v], 'package', lang)}." if es else f"{np(v, objs, lang)} carries {np_group(inside[v], 'package', lang)}."))
    dest = defaultdict(list)
    for a in p["goal"]:
        dest[a[2]].append(a[1])
    chunks = []
    for d in natural_sort(dest):
        chunks.append(del_(f"{np_group(dest[d], 'package', lang)} a {np(d, objs, lang)}" if es else f"{np_group(dest[d], 'package', lang)} to {np(d, objs, lang)}"))
    goal = (f"Hay que llevar {join(chunks, lang)}." if es else f"The task is to bring {join(chunks, lang)}.")
    return " ".join(sent) + "\n\n" + goal + "\n"


# Depots
def depots_describe(p, style, lang):
    objs = p["objects"]
    es = lang == "es"
    if style == "explicito":
        inv = object_inventory(objs, lang, ["depot", "distributor", "truck", "hoist", "pallet", "crate"])
        order = {"at": 0, "on": 1, "in": 2, "lifting": 3, "available": 4, "clear": 5}
        init = []
        for a in sorted(p["init"], key=lambda a: (order[a[0]], a)):
            if a[0] == "at":
                s = f"{np(a[1], objs, lang)} está en {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is at {np(a[2], objs, lang)}."
            elif a[0] == "on":
                s = f"{np(a[1], objs, lang)} está sobre {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is on {np(a[2], objs, lang)}."
            elif a[0] == "in":
                s = f"{np(a[1], objs, lang)} está dentro de {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is inside {np(a[2], objs, lang)}."
            elif a[0] == "lifting":
                s = f"{np(a[1], objs, lang)} está levantando {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} is lifting {np(a[2], objs, lang)}."
            elif a[0] == "available":
                s = f"{np(a[1], objs, lang)} está disponible." if es else f"{np(a[1], objs, lang)} is available."
            elif a[0] == "clear":
                if es:
                    adj = "despejada" if objs[a[1]] in ("crate", "pallet") else "despejado"
                    s = f"{np(a[1], objs, lang)} está {adj} (no tiene nada encima)."
                else:
                    s = f"{np(a[1], objs, lang)} is clear (nothing is on top of it)."
            init.append(del_(cap(s)))
        goal = []
        for a in sorted(p["goal"]):
            if a[0] == "on":
                goal.append(cap(f"{np(a[1], objs, lang)} debe estar sobre {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} must be on {np(a[2], objs, lang)}."))
            elif a[0] == "at":
                goal.append(cap(f"{np(a[1], objs, lang)} debe estar en {np(a[2], objs, lang)}." if es else f"{np(a[1], objs, lang)} must be at {np(a[2], objs, lang)}."))
        h1, h2 = ("Estado inicial:", "Meta:") if es else ("Initial state:", "Goal:")
        return f"{inv}\n\n{h1}\n{bullets(init)}\n\n{h2}\n{bullets(goal)}\n"

    # implícito: por lugar; 'at' de cajas y 'clear' se deducen de las pilas
    above = {a[2]: a[1] for a in p["init"] if a[0] == "on"}
    at = defaultdict(list)
    for a in p["init"]:
        if a[0] == "at" and objs[a[1]] != "crate":
            at[a[2]].append(a[1])
    places = natural_sort([o for o, t in objs.items() if t in ("depot", "distributor")])
    sent = []
    for pl in places:
        items = at.get(pl, [])
        groups = []
        for t in ["hoist", "truck"]:
            ns = [o for o in items if objs[o] == t]
            if ns:
                groups.append(np_group(ns, t, lang))
        pallet_desc = []
        for pal in natural_sort([o for o in items if objs[o] == "pallet"]):
            pile = []
            cur = pal
            while cur in above:
                cur = above[cur]
                pile.append(cur)
            if not pile:
                pallet_desc.append(f"la tarima {pal}, que está vacía" if es else f"pallet {pal}, which is empty")
            elif len(pile) == 1:
                pallet_desc.append(f"la tarima {pal} con la caja {pile[0]} encima" if es else f"pallet {pal} with crate {pile[0]} on it")
            else:
                pallet_desc.append(f"la tarima {pal} con una pila de cajas encima formada, de abajo hacia arriba, por {join(pile, lang)}"
                                   if es else f"pallet {pal} with a stack of crates on it made of, from bottom to top, {join(pile, lang)}")
        allparts = groups + pallet_desc
        if es:
            sent.append(del_(f"En {np(pl, objs, lang)} están {join(allparts, lang)}."))
        else:
            sent.append(f"At {np(pl, objs, lang)} there are {join(allparts, lang)}.")
    for a in sorted(p["init"]):
        if a[0] == "in":
            sent.append(del_(f"El camión {a[2]} lleva la caja {a[1]}." if es else f"Truck {a[2]} carries crate {a[1]}."))
        if a[0] == "lifting":
            sent.append(f"La grúa {a[1]} sostiene la caja {a[2]}." if es else f"Hoist {a[1]} is holding crate {a[2]}.")
    hoists = [o for o, t in objs.items() if t == "hoist"]
    avail = [a[1] for a in p["init"] if a[0] == "available"]
    if len(avail) == len(hoists):
        sent.append("Todas las grúas están libres." if es else "All hoists are free.")
    elif avail:
        sent.append(f"Las grúas libres son {join(natural_sort(avail), lang)}." if es else f"The free hoists are {join(natural_sort(avail), lang)}.")
    chunks = []
    for a in sorted(p["goal"]):
        if a[0] == "on":
            chunks.append(f"{a[1]} sobre {a[2]}" if es else f"{a[1]} on {a[2]}")
        elif a[0] == "at":
            chunks.append(f"{a[1]} en {a[2]}" if es else f"{a[1]} at {a[2]}")
    goal = (f"Al final se debe cumplir lo siguiente: {join(chunks, lang)}." if es else f"In the end the following must hold: {join(chunks, lang)}.")
    return " ".join(sent) + "\n\n" + goal + "\n"


# Ambulancias
def ambulance_generate(seed, idx):
    rnd = random.Random(seed * 1000 + idx)
    n_loc = rnd.randint(4, 7) if idx > 0 else 4
    locs = [f"l{i}" for i in range(1, n_loc + 1)]
    edges = set()
    order = locs[:]
    rnd.shuffle(order)
    for i in range(1, n_loc):                      # árbol de expansión
        a, b = order[i], rnd.choice(order[:i])
        edges.add(tuple(sorted((a, b))))
    for _ in range(rnd.randint(0, n_loc // 2)):   # aristas extra
        a, b = rnd.sample(locs, 2)
        edges.add(tuple(sorted((a, b))))
    hosp = rnd.choice(locs)
    n_amb = 1 if idx < 6 else 2
    n_pat = rnd.randint(2, 4)
    ambs = [f"amb{i}" for i in range(1, n_amb + 1)]
    pats = [f"p{i}" for i in range(1, n_pat + 1)]
    objects = {**{l: "location" for l in locs}, **{a: "ambulance" for a in ambs}, **{p: "patient" for p in pats}}
    init = set()
    for a, b in edges:
        init.add(("connected", a, b))
        init.add(("connected", b, a))
    init.add(("hospital", hosp))
    for a in ambs:
        init.add(("ambulance-at", a, rnd.choice(locs)))
        init.add(("empty", a))
    others = [l for l in locs if l != hosp]
    for p in pats:
        init.add(("patient-at", p, rnd.choice(others)))
    goal = {("patient-at", p, hosp) for p in pats}
    return objects, init, goal


def ambulance_describe(p, style, lang):
    objs = p["objects"]
    es = lang == "es"
    if style == "explicito":
        inv = object_inventory(objs, lang, ["location", "ambulance", "patient"])
        order = {"connected": 0, "hospital": 1, "ambulance-at": 2, "empty": 3, "patient-at": 4, "in": 5}
        init = []
        for a in sorted(p["init"], key=lambda a: (order[a[0]], a)):
            if a[0] == "connected":
                init.append(f"Hay conexión directa de {a[1]} hacia {a[2]}." if es else f"There is a direct connection from {a[1]} to {a[2]}.")
            elif a[0] == "hospital":
                init.append(f"En {a[1]} hay un hospital." if es else f"There is a hospital at {a[1]}.")
            elif a[0] == "ambulance-at":
                init.append(f"La ambulancia {a[1]} está en {a[2]}." if es else f"Ambulance {a[1]} is at {a[2]}.")
            elif a[0] == "empty":
                init.append(f"La ambulancia {a[1]} está vacía." if es else f"Ambulance {a[1]} is empty.")
            elif a[0] == "patient-at":
                init.append(f"El paciente {a[1]} está en {a[2]}." if es else f"Patient {a[1]} is at {a[2]}.")
            elif a[0] == "in":
                init.append(f"El paciente {a[1]} va dentro de la ambulancia {a[2]}." if es else f"Patient {a[1]} is inside ambulance {a[2]}.")
        goal = [f"El paciente {a[1]} debe estar en {a[2]}." if es else f"Patient {a[1]} must be at {a[2]}." for a in sorted(p["goal"])]
        h1, h2 = ("Estado inicial:", "Meta:") if es else ("Initial state:", "Goal:")
        return f"{inv}\n\n{h1}\n{bullets(init)}\n\n{h2}\n{bullets(goal)}\n"

    locs = natural_sort([o for o, t in objs.items() if t == "location"])
    edges = sorted({tuple(sorted(a[1:])) for a in p["init"] if a[0] == "connected"},
                   key=lambda e: (int(e[0][1:]), int(e[1][1:])))
    sent = [f"La red tiene {num(len(locs), lang)} ubicaciones: {join(locs, lang)}." if es else
            f"The network has {num(len(locs), lang)} locations: {join(locs, lang)}."]
    pairs = [f"{a} con {b}" if es else f"{a} with {b}" for a, b in edges]
    sent.append(f"Están conectadas en ambos sentidos: {join(pairs, lang)}." if es else
                f"The following are connected in both directions: {join(pairs, lang)}.")
    hosp = [a[1] for a in p["init"] if a[0] == "hospital"][0]
    sent.append(f"El hospital está en {hosp}." if es else f"The hospital is at {hosp}.")
    ambs = natural_sort([o for o, t in objs.items() if t == "ambulance"])
    amb_at = {a[1]: a[2] for a in p["init"] if a[0] == "ambulance-at"}
    if len(ambs) == 1:
        sent.append(f"Hay una ambulancia, {ambs[0]}, que está vacía en {amb_at[ambs[0]]}." if es else
                    f"There is one ambulance, {ambs[0]}, which is empty at {amb_at[ambs[0]]}.")
    else:
        where = [f"{a} en {amb_at[a]}" if es else f"{a} at {amb_at[a]}" for a in ambs]
        sent.append(f"Hay {num(len(ambs), lang)} ambulancias vacías: {join(where, lang)}." if es else
                    f"There are {num(len(ambs), lang)} empty ambulances: {join(where, lang)}.")
    pat_at = defaultdict(list)
    for a in p["init"]:
        if a[0] == "patient-at":
            pat_at[a[2]].append(a[1])
    chunks = []
    for l in natural_sort(pat_at):
        ps = natural_sort(pat_at[l])
        if es:
            chunks.append(f"{'al paciente' if len(ps) == 1 else 'a los pacientes'} {join(ps, lang)} en {l}")
        else:
            chunks.append(f"{'patient' if len(ps) == 1 else 'patients'} {join(ps, lang)} at {l}")
    sent.append(f"Hay que atender {join(chunks, lang)}." if es else f"Help is needed for {join(chunks, lang)}.")
    goal = ("Todos los pacientes deben ser llevados al hospital." if es else "All patients must be taken to the hospital.")
    return " ".join(sent) + "\n\n" + goal + "\n"


DESCRIBERS = {"blocksworld": blocks_describe, "logistics": logistics_describe,
              "depots": depots_describe, "ambulance": ambulance_describe}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ipc", required=True, help="ruta al repositorio potassco/pddl-instances")
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    manifest = []
    for dom in ["blocksworld", "logistics", "depots", "ambulance"]:
        os.makedirs(os.path.join(DATA, "problems", dom), exist_ok=True)
        if dom in IPC:
            src, insts = IPC[dom]
            for k, inst in enumerate(insts):
                pid = f"{dom}-ex" if k == 0 else f"{dom}-{k:02d}"
                dst = os.path.join(DATA, "problems", dom, pid + ".pddl")
                shutil.copy(os.path.join(args.ipc, src, "instances", inst + ".pddl"), dst)
                manifest.append({"id": pid, "domain": dom, "source": f"{src}/instances/{inst}.pddl",
                                 "role": "example" if k == 0 else "test"})
        else:
            for k in range(11):
                pid = f"{dom}-ex" if k == 0 else f"{dom}-{k:02d}"
                objects, init, goal = ambulance_generate(args.seed, k)
                txt = write_problem(pid, "ambulance", objects, init, goal)
                open(os.path.join(DATA, "problems", dom, pid + ".pddl"), "w").write(txt)
                manifest.append({"id": pid, "domain": dom, "source": f"generado (semilla {args.seed}, índice {k})",
                                 "role": "example" if k == 0 else "test"})

    os.makedirs(os.path.join(DATA, "descriptions"), exist_ok=True)
    for m in manifest:
        p = parse_problem(open(os.path.join(DATA, "problems", m["domain"], m["id"] + ".pddl")).read())
        m["n_objects"], m["n_init"], m["n_goal"] = len(p["objects"]), len(p["init"]), len(p["goal"])
        for style in ["explicito", "implicito", "indirecto"]:
            for lang in ["es", "en"]:
                if style == "indirecto":
                    txt = indirect.DESCRIBERS[m["domain"]](p, lang)
                else:
                    txt = DESCRIBERS[m["domain"]](p, style, lang)
                folder = "examples" if m["role"] == "example" else "descriptions"
                os.makedirs(os.path.join(DATA, folder), exist_ok=True)
                path = os.path.join(DATA, folder, f"{m['id']}__{style}__{lang}.txt")
                open(path, "w", encoding="utf-8").write(txt)
    json.dump(manifest, open(os.path.join(DATA, "manifest.json"), "w"), indent=2, ensure_ascii=False)
    print(f"{len(manifest)} problemas, {sum(1 for m in manifest if m['role'] == 'test')} de prueba")


if __name__ == "__main__":
    main()
