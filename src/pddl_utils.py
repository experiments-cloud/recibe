"""Lectura y escritura de problemas PDDL STRIPS con tipos.

Se usan para comparar :objects, :init y :goal con la referencia. La validez
sintáctica la decide el traductor de Fast Downward, no este módulo.
"""
import re


class PDDLParseError(Exception):
    pass


def _tokenize(text):
    text = re.sub(r";[^\n]*", " ", text)          # quitar comentarios
    text = text.replace("(", " ( ").replace(")", " ) ")
    return text.lower().split()


def parse_sexpr(text):
    tokens = _tokenize(text)
    if not tokens:
        raise PDDLParseError("texto vacío")
    pos = 0

    def read():
        nonlocal pos
        if pos >= len(tokens):
            raise PDDLParseError("fin inesperado del texto")
        tok = tokens[pos]
        pos += 1
        if tok == "(":
            lst = []
            while True:
                if pos >= len(tokens):
                    raise PDDLParseError("paréntesis sin cerrar")
                if tokens[pos] == ")":
                    pos += 1
                    return lst
                lst.append(read())
        if tok == ")":
            raise PDDLParseError("paréntesis de cierre inesperado")
        return tok

    expr = read()
    return expr, tokens[pos:]


def _typed_list(items):
    """['a','b','-','t','c'] -> {'a':'t','b':'t','c':'object'}"""
    out, pending = {}, []
    i = 0
    while i < len(items):
        it = items[i]
        if it == "-":
            if i + 1 >= len(items):
                raise PDDLParseError("tipo faltante tras '-'")
            typ = items[i + 1]
            if isinstance(typ, list):
                typ = " ".join(map(str, typ))
            for p in pending:
                out[p] = typ
            pending = []
            i += 2
            continue
        if isinstance(it, list):
            raise PDDLParseError("lista inesperada en :objects")
        pending.append(it)
        i += 1
    for p in pending:
        out[p] = "object"
    return out


def _atoms(expr, allow_and=True):
    """Devuelve (conjunto de átomos positivos, es_conjuncion_simple)."""
    simple = True
    atoms = set()
    if not expr:
        return atoms, simple
    if isinstance(expr, list) and expr and expr[0] == "and" and allow_and:
        for sub in expr[1:]:
            a, s = _atoms(sub, allow_and=True)
            atoms |= a
            simple = simple and s
        return atoms, simple
    if isinstance(expr, list) and expr and isinstance(expr[0], str):
        if expr[0] in ("not", "or", "forall", "exists", "when", "imply", "="):
            return atoms, False
        if all(isinstance(x, str) for x in expr):
            atoms.add(tuple(expr))
            return atoms, simple
    return atoms, False


def parse_problem(text):
    """Extrae nombre, dominio, objetos, init y goal de un problema PDDL."""
    expr, rest = parse_sexpr(text)
    if not isinstance(expr, list) or len(expr) < 2 or expr[0] != "define":
        raise PDDLParseError("no empieza con (define ...)")
    info = {"name": None, "domain": None, "objects": {}, "init": set(),
            "goal": set(), "init_simple": True, "goal_simple": True,
            "trailing_tokens": len(rest)}
    for part in expr[1:]:
        if not isinstance(part, list) or not part:
            continue
        head = part[0]
        if head == "problem" and len(part) > 1:
            info["name"] = part[1]
        elif head == ":domain" and len(part) > 1:
            info["domain"] = part[1]
        elif head == ":objects":
            info["objects"] = _typed_list(part[1:])
        elif head == ":init":
            for a in part[1:]:
                at, simple = _atoms(a, allow_and=False)
                info["init"] |= at
                info["init_simple"] = info["init_simple"] and simple
        elif head == ":goal":
            if len(part) > 1:
                at, simple = _atoms(part[1])
                info["goal"] = at
                info["goal_simple"] = simple
    return info


def parse_domain_types(text):
    """Devuelve {tipo: supertipo} y {predicado: aridad} de un dominio."""
    expr, _ = parse_sexpr(text)
    types, preds = {}, {}
    for part in expr[1:]:
        if isinstance(part, list) and part and part[0] == ":types":
            types = _typed_list(part[1:])
        if isinstance(part, list) and part and part[0] == ":predicates":
            for p in part[1:]:
                if isinstance(p, list) and p:
                    preds[p[0]] = len([x for x in p[1:] if isinstance(x, str) and x.startswith("?")])
    return types, preds


def write_problem(name, domain, objects, init, goal):
    """objects: {obj: tipo}; init/goal: iterables de tuplas."""
    by_type = {}
    for o, t in objects.items():
        by_type.setdefault(t, []).append(o)
    lines = [f"(define (problem {name})", f"  (:domain {domain})", "  (:objects"]
    for t in sorted(by_type):
        lines.append("    " + " ".join(sorted(by_type[t])) + f" - {t}")
    lines.append("  )")
    lines.append("  (:init")
    for a in sorted(init):
        lines.append("    (" + " ".join(a) + ")")
    lines.append("  )")
    lines.append("  (:goal (and")
    for a in sorted(goal):
        lines.append("    (" + " ".join(a) + ")")
    lines.append("  ))")
    lines.append(")")
    return "\n".join(lines) + "\n"


def extract_problem_text(response, lang):
    """Extrae el problema PDDL de la respuesta del modelo.

    Toma el texto entre las etiquetas si existen, quita las marcas de bloque
    de código de Markdown y regresa el primer bloque (define ...) balanceado.
    """
    if response is None:
        return None, "sin_respuesta"
    tags = {"es": ("[INICIO_PROBLEMA]", "[FIN_PROBLEMA]"),
            "en": ("[BEGIN_PROBLEM]", "[END_PROBLEM]")}[lang]
    body, how = None, None
    i = response.find(tags[0])
    if i >= 0:
        j = response.find(tags[1], i)
        body = response[i + len(tags[0]): j if j >= 0 else len(response)]
        how = "etiquetas" if j >= 0 else "etiqueta_inicial"
    else:
        body, how = response, "sin_etiquetas"
    body = re.sub(r"```[a-zA-Z]*", "", body)
    k = body.lower().find("(define")
    if k < 0:
        return None, how + "+sin_define"
    depth, end = 0, None
    for idx in range(k, len(body)):
        c = body[idx]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                end = idx + 1
                break
    if end is None:
        return body[k:].strip(), how + "+sin_cerrar"
    return body[k:end].strip(), how
