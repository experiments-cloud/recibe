"""Descripciones en estilo indirecto.

Todos los hechos de la referencia se pueden obtener del texto, pero casi
ninguno aparece de forma literal. Se usan referencias relativas (el aeropuerto
de cit2, la tarima de distributor1), complementos (todos los demás bloques),
rangos (p1 a p5), pilas descritas de arriba hacia abajo y rutas que hay que
convertir en conexiones de ida y vuelta. Los hechos que se deducen de otros,
como clear o available, no se mencionan.
"""
from collections import defaultdict


def _join(items, lang):
    items = list(items)
    conj = " y " if lang == "es" else " and "
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + conj + items[-1]


def _nsort(xs):
    import re
    return sorted(xs, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)])


def _range(names, lang):
    """['p1','p2','p3','p4'] -> 'p1 a p4' si son consecutivos; si no, lista."""
    import re
    names = _nsort(names)
    m = [re.fullmatch(r"([a-z]+)(\d+)", n) for n in names]
    if len(names) >= 3 and all(m) and len({x.group(1) for x in m}) == 1:
        nums = [int(x.group(2)) for x in m]
        if nums == list(range(nums[0], nums[0] + len(nums))):
            return f"{names[0]} a {names[-1]}" if lang == "es" else f"{names[0]} to {names[-1]}"
    return _join(names, lang)


# Blocksworld
def blocks(p, lang):
    es = lang == "es"
    B = str.upper
    blocks_ = _nsort(p["objects"])
    above = {a[2]: a[1] for a in p["init"] if a[0] == "on"}
    piles = []
    for b in _nsort([a[1] for a in p["init"] if a[0] == "ontable"]):
        pile = [b]
        while pile[-1] in above:
            pile.append(above[pile[-1]])
        piles.append(pile)
    towers = [pl for pl in piles if len(pl) > 1]
    held = [a[1] for a in p["init"] if a[0] == "holding"]
    s = []
    s.append(f"Sobre una mesa hay {len(blocks_)} bloques, del {B(blocks_[0])} al {B(blocks_[-1])} "
             f"(uno por cada letra)." if es else
             f"There are {len(blocks_)} blocks on a table, from {B(blocks_[0])} to {B(blocks_[-1])} (one per letter).")
    for t in towers:
        top = list(reversed(t))
        s.append(f"Hay una torre en la que, de arriba hacia abajo, están {_join([B(x) for x in top], lang)}."
                 if es else f"There is a tower that contains, from top to bottom, {_join([B(x) for x in top], lang)}.")
    if len(towers) < len(piles):
        s.append("Todos los demás bloques están sueltos, cada uno directamente sobre la mesa." if es else
                 "Every other block lies loose, each one directly on the table.")
    if held:
        s.append(f"El brazo tiene tomado el bloque {B(held[0])}." if es else f"The arm is holding block {B(held[0])}.")
    else:
        s.append("El brazo está desocupado." if es else "The arm is idle.")
    # meta: cadenas descritas de arriba hacia abajo
    on_goal = {a[1]: a[2] for a in p["goal"] if a[0] == "on"}
    under = set(on_goal.values())
    tops = _nsort([x for x in on_goal if x not in under])
    chains = []
    for t in tops:
        ch = [t]
        while ch[-1] in on_goal:
            ch.append(on_goal[ch[-1]])
        chains.append(ch)
    g = []
    for ch in chains:
        g.append(f"una torre que, de arriba hacia abajo, tenga {_join([B(x) for x in ch], lang)}" if es else
                 f"a tower that has, from top to bottom, {_join([B(x) for x in ch], lang)}")
    extra = [a for a in p["goal"] if a[0] != "on"]
    goal = (f"Se quiere formar {_join(g, lang)}; no importa sobre qué quede el bloque de más abajo "
            "ni dónde terminen los bloques que no se mencionan." if es else
            f"The aim is to build {_join(g, lang)}; it does not matter what the lowest block rests on "
            "or where the blocks not mentioned end up.")
    for a in extra:
        if a[0] == "ontable":
            goal += (f" Además, {B(a[1])} debe acabar directamente sobre la mesa." if es else
                     f" Also, {B(a[1])} must end up directly on the table.")
        elif a[0] == "clear":
            goal += (f" Además, {B(a[1])} no debe tener nada encima." if es else
                     f" Also, {B(a[1])} must have nothing on top of it.")
    return " ".join(s) + "\n\n" + goal + "\n"


# Logistics
def logistics(p, lang):
    es = lang == "es"
    o = p["objects"]
    city_of = {a[1]: a[2] for a in p["init"] if a[0] == "in-city"}
    cities = _nsort(set(city_of.values()))
    places = defaultdict(lambda: {"location": [], "airport": []})
    for pl, c in city_of.items():
        places[c][o[pl]].append(pl)
    s = []
    desc = []
    for c in cities:
        loc, apt = places[c]["location"], places[c]["airport"]
        parts = []
        if loc:
            parts.append((f"la ubicación urbana {_join(_nsort(loc), lang)}" if es else
                          f"the city location {_join(_nsort(loc), lang)}"))
        if apt:
            parts.append((f"el aeropuerto {_join(_nsort(apt), lang)}" if es else f"the airport {_join(_nsort(apt), lang)}"))
        desc.append(f"{c} ({_join(parts, lang)})")
    s.append(("La red de reparto abarca estas ciudades con sus lugares: " if es else
              "The delivery network covers these cities and their places: ") + "; ".join(desc) + ".")

    def ref(place):
        c = city_of[place]
        same = places[c][o[place]]
        if len(same) == 1:
            if o[place] == "airport":
                return f"el aeropuerto de {c}" if es else f"the airport of {c}"
            return f"la ubicación urbana de {c}" if es else f"the city location of {c}"
        return place

    at = {a[1]: a[2] for a in p["init"] if a[0] == "at"}
    trucks = _nsort([x for x in o if o[x] == "truck"])
    planes = _nsort([x for x in o if o[x] == "airplane"])
    tdesc = [f"{t} está en {ref(at[t])}" if es else f"{t} is at {ref(at[t])}" for t in trucks if t in at]
    s.append(("Camiones: " if es else "Trucks: ") + "; ".join(tdesc) + ".")
    pdesc = [f"{a} está en {ref(at[a])}" if es else f"{a} is at {ref(at[a])}" for a in planes if a in at]
    s.append(("Aviones: " if es else "Airplanes: ") + "; ".join(pdesc) + ".")
    by_place = defaultdict(list)
    for x in o:
        if o[x] == "package" and x in at:
            by_place[at[x]].append(x)
    pk = []
    for pl in _nsort(by_place):
        pk.append(f"{_range(by_place[pl], lang)} en {ref(pl)}" if es else f"{_range(by_place[pl], lang)} at {ref(pl)}")
    s.append(("Los paquetes están así: " if es else "The packages are placed as follows: ") + "; ".join(pk) + ".")
    for a in sorted(p["init"]):
        if a[0] == "in":
            s.append(f"Además, {a[1]} ya va cargado en {a[2]}." if es else f"Also, {a[1]} is already loaded in {a[2]}.")
    # metas agrupadas por destino, con referencia relativa
    dest = defaultdict(list)
    for a in p["goal"]:
        dest[a[2]].append(a[1])
    g = []
    for d in _nsort(dest):
        g.append(f"{_join(_nsort(dest[d]), lang)} a {ref(d)}" if es else f"{_join(_nsort(dest[d]), lang)} to {ref(d)}")
    goal = ("Pedido: hay que entregar " if es else "Order: deliver ") + "; ".join(g) + "."
    goal += (" Los demás paquetes pueden quedar donde sea." if es else " The remaining packages may end up anywhere.")
    return " ".join(s) + "\n\n" + goal.replace(" a el ", " al ") + "\n"


# Depots
def depots(p, lang):
    es = lang == "es"
    o = p["objects"]
    at = {a[1]: a[2] for a in p["init"] if a[0] == "at"}
    places = _nsort([x for x in o if o[x] in ("depot", "distributor")])
    hoist_of, pallet_of = defaultdict(list), defaultdict(list)
    for x in o:
        if o[x] == "hoist":
            hoist_of[at[x]].append(x)
        if o[x] == "pallet":
            pallet_of[at[x]].append(x)
    above = {a[2]: a[1] for a in p["init"] if a[0] == "on"}

    def pallet_ref(pal):
        pl = at[pal]
        return (f"la tarima de {pl}" if es else f"the pallet of {pl}") if len(pallet_of[pl]) == 1 else pal

    s = []
    lst = []
    for pl in places:
        kind = ("depósito" if o[pl] == "depot" else "distribuidor") if es else o[pl]
        lst.append(f"{pl} ({kind}; grúa {_join(_nsort(hoist_of[pl]), lang)}, tarima {_join(_nsort(pallet_of[pl]), lang)})"
                   if es else
                   f"{pl} ({kind}; hoist {_join(_nsort(hoist_of[pl]), lang)}, pallet {_join(_nsort(pallet_of[pl]), lang)})")
    s.append(("Instalaciones: " if es else "Facilities: ") + "; ".join(lst) + ".")
    for pl in places:
        for pal in _nsort(pallet_of[pl]):
            pile = []
            cur = pal
            while cur in above:
                cur = above[cur]
                pile.append(cur)
            if pile:
                top = list(reversed(pile))
                s.append((f"Sobre {pallet_ref(pal)} hay apiladas, de arriba hacia abajo, {_join(top, lang)}."
                          if len(top) > 1 else f"Sobre {pallet_ref(pal)} está solo {top[0]}.") if es else
                         (f"On {pallet_ref(pal)} there are stacked, from top to bottom, {_join(top, lang)}."
                          if len(top) > 1 else f"On {pallet_ref(pal)} there is only {top[0]}."))
    empties = [pal for pal in _nsort([x for x in o if o[x] == "pallet"]) if pal not in above]
    if empties:
        s.append(("Las demás tarimas están vacías." if es else "The remaining pallets are empty."))
    for t in _nsort([x for x in o if o[x] == "truck"]):
        pl = at[t]
        h = hoist_of[pl]
        where = (f"donde trabaja la grúa {h[0]}" if len(h) == 1 else pl) if es else \
                (f"where hoist {h[0]} works" if len(h) == 1 else pl)
        s.append(f"El camión {t} está estacionado {where}." if es else f"Truck {t} is parked {where}.")
    for a in sorted(p["init"]):
        if a[0] == "in":
            s.append(f"{a[1]} viaja dentro de {a[2]}." if es else f"{a[1]} is travelling inside {a[2]}.")
        if a[0] == "lifting":
            s.append(f"La grúa {a[1]} tiene suspendida a {a[2]}." if es else f"Hoist {a[1]} is holding {a[2]} in the air.")
    busy = [a[1] for a in p["init"] if a[0] == "lifting"]
    s.append(("Ninguna grúa está ocupada." if es else "No hoist is busy.") if not busy else
             ("Las demás grúas están libres." if es else "The other hoists are free."))
    g = []
    for a in sorted(p["goal"]):
        if a[0] == "on":
            tgt = pallet_ref(a[2]) if o.get(a[2]) == "pallet" else a[2]
            g.append(f"{a[1]} sobre {tgt}" if es else f"{a[1]} on {tgt}")
        elif a[0] == "at":
            g.append(f"{a[1]} en {a[2]}" if es else f"{a[1]} at {a[2]}")
    goal = (("Se requiere dejar " if es else "It is required to leave ") + _join(g, lang) + "." +
            (" No importa dónde terminen las demás cajas ni los camiones." if es else
             " It does not matter where the other crates or the trucks end up."))
    return " ".join(s) + "\n\n" + goal + "\n"


# Ambulancia
def _paths(edges):
    """Descompone un grafo no dirigido en rutas (caminos) que cubren cada arista una vez."""
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    used, paths = set(), []
    nodes = _nsort(adj)
    while True:
        start = next((n for n in nodes if any(tuple(sorted((n, m))) not in used for m in adj[n])
                      and len(adj[n]) % 2 == 1), None) or \
                next((n for n in nodes if any(tuple(sorted((n, m))) not in used for m in adj[n])), None)
        if start is None:
            break
        path = [start]
        cur = start
        while True:
            nxt = next((m for m in _nsort(adj[cur]) if tuple(sorted((cur, m))) not in used), None)
            if nxt is None:
                break
            used.add(tuple(sorted((cur, nxt))))
            path.append(nxt)
            cur = nxt
        paths.append(path)
    return paths


def ambulance(p, lang):
    es = lang == "es"
    o = p["objects"]
    locs = _nsort([x for x in o if o[x] == "location"])
    edges = {tuple(sorted(a[1:])) for a in p["init"] if a[0] == "connected"}
    hosp = [a[1] for a in p["init"] if a[0] == "hospital"][0]
    amb_at = {a[1]: a[2] for a in p["init"] if a[0] == "ambulance-at"}
    ambs = _nsort(amb_at)
    pats = _nsort([x for x in o if o[x] == "patient"])
    pat_at = {a[1]: a[2] for a in p["init"] if a[0] == "patient-at"}
    s = [f"La zona tiene las ubicaciones {_range(locs, lang)}." if es else f"The area has locations {_range(locs, lang)}."]
    routes = ["–".join(pt) for pt in _paths(edges)]
    s.append(("Las calles son de doble sentido y forman estas rutas, donde cada guion une dos ubicaciones "
              f"vecinas: {_join(routes, lang)}." if es else
              "Streets are two-way and form these routes, where each dash joins two neighbouring "
              f"locations: {_join(routes, lang)}."))
    in_h = [a for a in ambs if amb_at[a] == hosp]
    s.append(f"El hospital está en {hosp}." if es else f"The hospital is at {hosp}.")
    for a in in_h:
        s.append(f"La ambulancia {a} espera en el hospital." if es else f"Ambulance {a} is waiting at the hospital.")
    rest = [a for a in ambs if a not in in_h]
    for a in rest:
        s.append(f"La ambulancia {a} está en {amb_at[a]}." if es else f"Ambulance {a} is at {amb_at[a]}.")
    s.append(("Ninguna ambulancia lleva pacientes." if es else "No ambulance is carrying patients."))
    by_loc = defaultdict(list)
    for x in pats:
        by_loc[pat_at[x]].append(x)
    s.append((f"Hay {len(pats)} pacientes ({_range(pats, lang)}) esperando traslado." if es else
              f"There are {len(pats)} patients ({_range(pats, lang)}) waiting to be moved."))
    groups = sorted(by_loc.items(), key=lambda kv: -len(kv[1]))
    if len(groups) > 1:
        main_loc, _ = groups[0]
        for loc, ps in sorted(groups[1:], key=lambda kv: kv[0]):
            s.append((f"{_join(_nsort(ps), lang)} {'está' if len(ps) == 1 else 'están'} en {loc}." if es else
                      f"{_join(_nsort(ps), lang)} {'is' if len(ps) == 1 else 'are'} at {loc}."))
        s.append(f"Todos los demás están en {main_loc}." if es else f"All the others are at {main_loc}.")
    else:
        s.append(f"Todos están en {groups[0][0]}." if es else f"All of them are at {groups[0][0]}.")
    goal = ("Cada paciente debe terminar en el hospital; las ambulancias pueden terminar en cualquier lugar."
            if es else "Every patient must end up at the hospital; the ambulances may end anywhere.")
    return " ".join(s) + "\n\n" + goal + "\n"


DESCRIBERS = {"blocksworld": blocks, "logistics": logistics, "depots": depots, "ambulance": ambulance}
