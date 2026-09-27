"""Tablas, pruebas estadísticas y figuras a partir de results/evaluacion.csv.

Archivos en results/analisis/:
  tabla_modelos.csv            métricas por modelo, con intervalos de Wilson al 95 %
  tabla_condiciones.csv        modelo x prompt x idioma x estilo
  tabla_dominios.csv           coincidencia exacta por modelo y dominio
  pruebas_mcnemar.csv          pruebas de McNemar exactas pareadas, con ajuste de Holm
  pruebas_mcnemar_casos.csv    las mismas pruebas por caso (mayoría de las 3 repeticiones)
  consistencia.csv             acuerdo entre repeticiones
  errores.csv                  error principal por modelo y estilo
  sensibilidad_sin_vacias.csv  coincidencia exacta sin las respuestas vacías
  idioma_sin_vacias.csv        es frente a en, solo pares sin respuestas vacías
  respuestas_vacias.csv        respuestas vacías por modelo, idioma y estilo
  figura_embudo.png, figura_idioma_estilo.png (600 dpi)
  reporte.md                   todas las tablas anteriores

  python3 src/analyze.py [--idioma es|en]
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from statsmodels.stats.contingency_tables import mcnemar  # noqa: E402
from statsmodels.stats.multitest import multipletests  # noqa: E402
from statsmodels.stats.proportion import proportion_confint  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGES = [("sintaxis_ok", "Sintaxis válida"), ("resoluble", "Resoluble"),
          ("plan_valido_ref", "Plan válido en la referencia"), ("exacto", "Coincidencia exacta")]
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3dd"
SHORT = {"deepseek-v4.1-flash": "DeepSeek", "gemini-3.8-flash": "Gemini", "gpt-6-luna": "GPT-6 Luna",
         "mistral-small-4": "Mistral"}


def pct_ci(series):
    k, n = int(series.sum()), int(series.count())
    if n == 0:
        return "-"
    lo, hi = proportion_confint(k, n, method="wilson")
    return f"{100 * k / n:.1f} [{100 * lo:.1f}, {100 * hi:.1f}]"


def funnel_table(d, by):
    rows = []
    for key, g in d.groupby(by, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        r = dict(zip(by, key))
        r["n"] = len(g)
        for col, name in STAGES:
            r[name + " % [IC95]"] = pct_ci(g[col].astype(bool))
        r["F1 init (media)"] = round(g["init_f1"].mean(), 3)
        r["F1 meta (media)"] = round(g["goal_f1"].mean(), 3)
        rows.append(r)
    return pd.DataFrame(rows)


def paired_test(d, factor, a, b, keys, outcome="exacto"):
    """McNemar exacto pareando las salidas que solo difieren en `factor`."""
    x = d[d[factor] == a].set_index(keys)[outcome].astype(bool)
    y = d[d[factor] == b].set_index(keys)[outcome].astype(bool)
    j = pd.concat([x.rename("a"), y.rename("b")], axis=1, join="inner")
    if j.empty:
        return None
    n01 = int((~j.a & j.b).sum())
    n10 = int((j.a & ~j.b).sum())
    tbl = [[int((j.a & j.b).sum()), n10], [n01, int((~j.a & ~j.b).sum())]]
    p = mcnemar(tbl, exact=True).pvalue
    return {"A": a, "B": b, "pares": len(j), "% A": round(100 * j.a.mean(), 1), "% B": round(100 * j.b.mean(), 1),
            "diferencia B-A (pp)": round(100 * (j.b.mean() - j.a.mean()), 1),
            "solo A acierta": n10, "solo B acierta": n01, "p (McNemar exacto)": p}


def style_axes(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


LBL = {
    "es": {"stages": [s for _, s in STAGES], "y1": "Salidas (%)", "y2": "Coincidencia exacta (%)",
           "lang": {"es": "Español", "en": "Inglés"},
           "style": {"explicito": "Estilo explícito", "implicito": "Estilo implícito",
                     "indirecto": "Estilo indirecto"}},
    "en": {"stages": ["Valid syntax", "Solvable", "Plan valid on reference", "Exact match"],
           "y1": "Outputs (%)", "y2": "Exact match (%)",
           "lang": {"es": "Spanish", "en": "English"},
           "style": {"explicito": "Explicit style", "implicito": "Implicit style",
                     "indirecto": "Indirect style"}},
}
L = LBL["es"]


def fig_funnel(d, models, path):
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=600)
    n = len(models)
    width = 0.8 / n
    for i, m in enumerate(models):
        g = d[d.model == m]
        vals = [100 * g[c].astype(bool).mean() for c, _ in STAGES]
        xs = [s + (i - (n - 1) / 2) * width for s in range(len(STAGES))]
        bars = ax.bar(xs, vals, width=width - 0.02, color=PALETTE[i % len(PALETTE)], label=SHORT.get(m, m),
                      edgecolor="white", linewidth=1)
        for x, v in zip(xs, vals):
            ax.text(x, v + 1.2, f"{v:.0f}", ha="center", va="bottom", fontsize=7, color=INK)
    ax.set_xticks(range(len(STAGES)))
    ax.set_xticklabels(L["stages"], color=INK, fontsize=9)
    ax.set_ylim(0, 108)
    ax.set_ylabel(L["y1"], color=MUTED, fontsize=9)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=8, ncol=min(n, 4), loc="upper center", bbox_to_anchor=(0.5, 1.12))
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_lang_style(d, models, path):
    styles = [s for s in ["explicito", "implicito", "indirecto"] if s in set(d["style"])]
    fig, axes = plt.subplots(1, len(styles), figsize=(3.2 * len(styles) + 1.5, 3.6), dpi=600, sharey=True, squeeze=False)
    colors = {"es": PALETTE[0], "en": PALETTE[1]}
    names = L["lang"]
    for ax, st in zip(axes[0], styles):
        for j, lang in enumerate(["es", "en"]):
            vals = [100 * d[(d.model == m) & (d["style"] == st) & (d.lang == lang)]["exacto"].astype(bool).mean()
                    for m in models]
            xs = [i + (j - 0.5) * 0.38 for i in range(len(models))]
            ax.bar(xs, vals, width=0.36, color=colors[lang], label=names[lang], edgecolor="white", linewidth=1)
            for x, v in zip(xs, vals):
                ax.text(x, v + 1.2, f"{v:.0f}", ha="center", va="bottom", fontsize=7, color=INK)
        ax.set_title(L["style"][st], fontsize=10, color=INK)
        ax.set_xticks(range(len(models)))
        ax.set_xticklabels([SHORT.get(m, m) for m in models], fontsize=8, color=INK)
        ax.set_ylim(0, 108)
        style_axes(ax)
    axes[0][0].set_ylabel(L["y2"], color=MUTED, fontsize=9)
    axes[0][-1].legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def md(df):
    return df.to_markdown(index=False) if hasattr(df, "to_markdown") else df.to_string(index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=os.path.join(ROOT, "results", "evaluacion.csv"))
    ap.add_argument("--salida", default=None)
    ap.add_argument("--idioma", choices=["es", "en"], default="es", help="idioma de las etiquetas de las figuras")
    args = ap.parse_args()
    out = args.salida or os.path.join(os.path.dirname(args.entrada), "analisis")
    os.makedirs(out, exist_ok=True)

    d = pd.read_csv(args.entrada)
    for c, _ in STAGES:
        d[c] = d[c].astype(bool)
    # una salida solo cuenta como exacta si además Fast Downward la acepta
    n_corr = int((d["exacto"] & ~d["sintaxis_ok"]).sum())
    d["exacto"] = d["exacto"] & d["sintaxis_ok"]
    d.loc[~d["exacto"] & d["error_principal"].isna(), "error_principal"] = "sintaxis"
    models = list(dict.fromkeys(d["model"]))

    t_mod = funnel_table(d, ["model"])
    t_cond = funnel_table(d, ["model", "prompt", "lang", "style"])
    t_dom = d.pivot_table(index="model", columns="domain", values="exacto", aggfunc="mean").mul(100).round(1).reset_index()
    t_mod.to_csv(os.path.join(out, "tabla_modelos.csv"), index=False)
    t_cond.to_csv(os.path.join(out, "tabla_condiciones.csv"), index=False)
    t_dom.to_csv(os.path.join(out, "tabla_dominios.csv"), index=False)

    tests = []
    base = ["model", "prompt", "lang", "style", "problem", "rep"]
    for factor, a, b in [("lang", "en", "es"), ("prompt", "P0", "P1"), ("style", "explicito", "implicito"),
                         ("style", "explicito", "indirecto")]:
        keys = [k for k in base if k != factor]
        for m in models + ["(todos)"]:
            sub = d if m == "(todos)" else d[d.model == m]
            r = paired_test(sub, factor, a, b, keys)
            if r:
                tests.append({"comparación": f"{factor}: {a} vs {b}", "modelo": m, **r})
    t_tests = pd.DataFrame(tests)
    if not t_tests.empty:
        t_tests["p (Holm)"] = multipletests(t_tests["p (McNemar exacto)"], method="holm")[1]
        for c in ("p (McNemar exacto)", "p (Holm)"):
            t_tests[c] = t_tests[c].map(lambda v: f"{v:.4f}" if v >= 0.0001 else "<0.0001")
    t_tests.to_csv(os.path.join(out, "pruebas_mcnemar.csv"), index=False)

    # robustez: las mismas pruebas por caso (correcto si al menos 2 de 3 repeticiones son exactas)
    cases = (d.groupby(["model", "prompt", "lang", "style", "problem"])["exacto"].sum().ge(2)
             .rename("exacto").reset_index())
    base_c = ["model", "prompt", "lang", "style", "problem"]
    tests_c = []
    for factor, a, b in [("lang", "en", "es"), ("prompt", "P0", "P1"), ("style", "explicito", "implicito"),
                         ("style", "explicito", "indirecto")]:
        keys = [k for k in base_c if k != factor]
        for m in models + ["(todos)"]:
            sub = cases if m == "(todos)" else cases[cases.model == m]
            r = paired_test(sub, factor, a, b, keys)
            if r:
                tests_c.append({"comparación": f"{factor}: {a} vs {b}", "modelo": m, **r})
    t_tests_c = pd.DataFrame(tests_c)
    t_tests_c["p (Holm)"] = multipletests(t_tests_c["p (McNemar exacto)"], method="holm")[1]
    for c in ("p (McNemar exacto)", "p (Holm)"):
        t_tests_c[c] = t_tests_c[c].map(lambda v: f"{v:.4f}" if v >= 0.0001 else "<0.0001")
    t_tests_c.to_csv(os.path.join(out, "pruebas_mcnemar_casos.csv"), index=False)

    grp = d.groupby(["model", "prompt", "lang", "style", "problem"])["exacto"]
    cons = grp.agg(lambda s: s.nunique() == 1).groupby(level="model").mean().mul(100).round(1)
    t_cons = cons.rename("% de casos con las repeticiones de acuerdo").reset_index()
    t_cons.to_csv(os.path.join(out, "consistencia.csv"), index=False)

    # sensibilidad: sin las respuestas que no contienen PDDL
    ne = d[d.error_principal != "sin_pddl"]
    t_sens = ne.pivot_table(index="model", columns="lang", values="exacto", aggfunc="mean").mul(100).round(1)
    t_sens["n excluidas"] = d[d.error_principal == "sin_pddl"].groupby("model").size().reindex(t_sens.index).fillna(0).astype(int)
    t_sens = t_sens.reset_index()
    t_sens.to_csv(os.path.join(out, "sensibilidad_sin_vacias.csv"), index=False)
    # control: salidas exactas que Fast Downward no resolvió
    t_inc = d[d["exacto"] & ~d["resoluble"]][["run_id", "fd_rc"]]
    t_inc.to_csv(os.path.join(out, "control_exactas_no_resueltas.csv"), index=False)

    # pruebas de idioma sin respuestas vacías (fuera del ajuste de Holm)
    d["_vacia"] = d["error_principal"] == "sin_pddl"
    kl = ["model", "prompt", "style", "problem", "rep"]
    en = d[d.lang == "en"].set_index(kl)[["exacto", "_vacia"]]
    es = d[d.lang == "es"].set_index(kl)[["exacto", "_vacia"]]
    jj = en.join(es, lsuffix="_en", rsuffix="_es", how="inner")
    jj = jj[~jj["_vacia_en"] & ~jj["_vacia_es"]]
    tasa = d.groupby("model")["_vacia"].mean()
    sin_vacias = [m for m in models if tasa.get(m, 0) < 0.05]
    extra = []
    for m in models + ["(todos)", "(modelos con < 5 % de vacías)"]:
        if m == "(todos)":
            sub = jj
        elif m.startswith("(modelos"):
            sub = jj[jj.index.get_level_values("model").isin(sin_vacias)]
        else:
            sub = jj[jj.index.get_level_values("model") == m]
        if sub.empty:
            continue
        a, b = sub["exacto_en"].astype(bool), sub["exacto_es"].astype(bool)
        n10, n01 = int((a & ~b).sum()), int((~a & b).sum())
        p = mcnemar([[int((a & b).sum()), n10], [n01, int((~a & ~b).sum())]], exact=True).pvalue
        extra.append({"modelo": m, "pares sin respuestas vacías": len(sub), "% en": round(100 * a.mean(), 1),
                      "% es": round(100 * b.mean(), 1), "solo en acierta": n10, "solo es acierta": n01,
                      "p (McNemar exacto, sin ajustar)": round(p, 4)})
    t_extra = pd.DataFrame(extra)
    t_extra.to_csv(os.path.join(out, "idioma_sin_vacias.csv"), index=False)
    t_vac = d[d["_vacia"]].groupby(["model", "lang", "style"]).size().rename("respuestas vacías").reset_index()
    t_vac.to_csv(os.path.join(out, "respuestas_vacias.csv"), index=False)

    t_err = pd.crosstab([d.model, d["style"]], d.error_principal.fillna("ninguno (exacto)")).reset_index()
    t_err.to_csv(os.path.join(out, "errores.csv"), index=False)

    global L
    L = LBL[args.idioma]
    suf = "" if args.idioma == "es" else "_en"
    fig_funnel(d, models, os.path.join(out, f"figura_embudo{suf}.png"))
    fig_lang_style(d, models, os.path.join(out, f"figura_idioma_estilo{suf}.png"))

    tok = d.groupby("model")[["tokens_in", "tokens_out"]].sum(min_count=1).round(0).astype("Int64")
    rep = ["# Reporte de resultados", "",
           f"Salidas evaluadas: {len(d)}. Modelos: {', '.join(models)}.", "",
           "## Embudo por modelo (porcentaje e intervalo de confianza de 95 %, Wilson)", "", md(t_mod), "",
           "## Por condición", "", md(t_cond), "",
           "## Coincidencia exacta por dominio (%)", "", md(t_dom), "",
           "## Pruebas pareadas (McNemar exacto sobre coincidencia exacta; p ajustada por Holm)", "",
           md(t_tests) if not t_tests.empty else "Sin pares suficientes.", "",
           "## Pruebas pareadas por caso (mayoría de 2 de 3 repeticiones; p ajustada por Holm)", "",
           md(t_tests_c), "",
           "## Consistencia entre repeticiones", "", md(t_cons), "",
           "## Error principal por modelo y estilo (conteos)", "", md(t_err), "",
           "## Sensibilidad: coincidencia exacta (%) excluyendo respuestas vacías", "", md(t_sens), "",
           f"Salidas con hechos idénticos a la referencia pero rechazadas por Fast Downward, contadas como no exactas: {n_corr}.", "",
           "## Control de medición: salidas exactas que Fast Downward no resolvió", "",
           (f"{len(t_inc)} casos. Códigos de salida: {t_inc.fd_rc.value_counts().to_dict()}."
            if len(t_inc) else "0 casos."), "",
           "## Idioma sin respuestas vacías (pares en los que ninguna de las dos respuestas está vacía; p sin ajustar)", "",
           md(t_extra), f"Modelos con menos de 5 % de respuestas vacías: {', '.join(sin_vacias)}.", "",
           "## Respuestas vacías por modelo, idioma y estilo", "", md(t_vac) if not t_vac.empty else "Ninguna.", "",
           "## Tokens", "", md(tok.reset_index()), ""]
    open(os.path.join(out, "reporte.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print(f"Resultados en {out}")


if __name__ == "__main__":
    main()
