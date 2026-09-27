# NL2PDDL

Code and data for an experiment that measures how well large language models translate natural language descriptions of planning problems, in Spanish and in English, into PDDL problem files. The PDDL domain file is part of the input.

The code comments, file names and command-line options are in Spanish.

## Design

- **Problems.** 40 test problems from four domains, 10 per domain. Blocksworld (4 operators, typed), Logistics (typed) and Depots come from the International Planning Competition via [pddl-instances](https://github.com/potassco/pddl-instances). The Ambulance domain and its problems were generated for this experiment with seed 2026. Each domain also has one extra problem that serves as the worked example of prompt P1.
- **Descriptions.** 240 descriptions, generated from the reference problem files with templates: 40 problems × 3 styles × 2 languages (`es`, `en`).
  - `explicito`: one sentence per fact.
  - `implicito`: facts are grouped, and some of them follow from others (for example, which blocks are clear follows from the stacks).
  - `indirecto`: almost no fact is stated literally. The text uses relative references, complements ("all the other blocks"), ranges ("p1 to p5"), stacks from top to bottom and routes that must be expanded into two-way connections.
- **Prompts.** `P0` with no example and `P1` with one worked example from the same domain and style (`prompts/`).
- **Runs.** Each combination of model, prompt, language, style and problem is run 3 times: 1,440 outputs per model.

## Contents

| Path | Contents |
| --- | --- |
| `data/domains/` | The four domain files. |
| `data/problems/` | Reference problem files (`<domain>-01` to `-10` for testing, `<domain>-ex` for the worked example). |
| `data/descriptions/`, `data/examples/` | Descriptions of the test problems and of the example problems. |
| `data/manifest.json` | Source and size of each problem. |
| `prompts/` | Prompt templates in Spanish and English. |
| `config.yaml` | Models, repetitions and tool paths. |
| `src/build_dataset.py`, `src/indirect.py` | Generation of `data/` from the reference files. |
| `src/run_experiment.py` | Calls to the models. |
| `src/evaluate.py` | Evaluation with Fast Downward, VAL and a comparison with the reference. |
| `src/analyze.py` | Tables, statistical tests and figures. |
| `src/predicados_error.py` | Predicates omitted or added in the wrong outputs. |
| `src/verificacion_cruzada.py` | Post hoc cross-check between pairs of models. |
| `tests/test_referencias.py` | Check that every reference file passes all the metrics. |
| `results/` | Raw responses, evaluation and generated problem files of the experiment. |

## Installation

Tested on Ubuntu (also under WSL) with Python 3.11 and 3.14.

```bash
sudo apt install -y python3-venv git cmake g++ make
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./instalar_herramientas.sh          # Fast Downward, VAL and pddl-instances in ../tools
python3 tests/test_referencias.py   # should end with "todas las referencias pasan"
```

The script checks out the versions used in the experiment:

| Tool | Commit |
| --- | --- |
| Fast Downward | `9b81c7e` |
| VAL | `3c7a1f3` |
| pddl-instances | `cf19edf` |

## Running the experiment

API keys are read from environment variables:

```bash
export GEMINI_API_KEY=...
export OPENROUTER_API_KEY=...
```

```bash
python3 src/run_experiment.py         # 5,760 calls; can be interrupted and resumed
python3 src/evaluate.py --procesos 1  # writes results/evaluacion.csv
python3 src/analyze.py --idioma en    # writes results/analisis/
python3 src/predicados_error.py
python3 src/verificacion_cruzada.py
```

`results/` already contains the responses obtained in the experiment, so the evaluation and the analysis can be repeated without calling the models. The descriptions can be regenerated with `python3 src/build_dataset.py --ipc ../tools/pddl-instances`, which produces the same files as those in `data/`.

Model identifiers, providers and token limits are in `config.yaml`. The temperature was left at each provider's default.

## Metrics

| Column in `evaluacion.csv` | Meaning |
| --- | --- |
| `sintaxis_ok` | The Fast Downward translator accepts the domain and the generated problem. |
| `resoluble` | Fast Downward (`lama-first`, 300 s) finds a plan. |
| `plan_valido_ref` | VAL accepts that plan on the reference problem. |
| `exacto` | Objects with their types, `:init` and `:goal` equal to the reference. An output also needs valid syntax to count as exact in the analysis. |
| `init_f1`, `goal_f1` | F1 per fact. |
| `error_principal` | First failure: `sin_pddl`, `sintaxis`, `objetos_o_tipos`, `init_hechos_omitidos`, `init_hechos_extra`, `init_hechos_cambiados` or `meta`. |

The analysis reports Wilson 95% confidence intervals and exact McNemar tests on paired outputs, with Holm's correction.
