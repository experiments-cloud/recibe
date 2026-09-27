"""Clientes para los modelos de lenguaje, con reintentos.

Proveedores:
  gemini          API de Google (paquete google-genai).
  openai_compat   API compatible con OpenAI (OpenAI, OpenRouter, Ollama, etc.).

Las claves se leen de las variables de entorno indicadas en config.yaml.
"""
import os
import random
import time


class LLMError(Exception):
    pass


def _retryable(exc):
    txt = f"{type(exc).__name__} {exc}".lower()
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    if code in (408, 409, 429, 500, 502, 503, 504, 529):
        return True
    return any(k in txt for k in ("rate", "quota", "timeout", "temporarily", "overloaded",
                                   "unavailable", "connection", "429", "503"))


class Client:
    def __init__(self, spec):
        self.spec = spec
        self.provider = spec["provider"]
        self.model = spec.get("model")
        self.temperature = spec.get("temperature")   # None: valor por defecto del proveedor
        self.max_tokens = spec.get("max_tokens", 4096)
        self.max_retries = spec.get("max_retries", 6)
        try:
            self._init_provider()
        except ImportError as e:
            raise LLMError(f"falta el paquete {e.name} (pip install -r requirements.txt)") from e

    def _init_provider(self):
        p = self.provider
        if p == "gemini":
            from google import genai
            env = self.spec.get("api_key_env", "GEMINI_API_KEY")
            key = os.environ.get(env)
            if not key:
                raise LLMError(f"falta la variable de entorno {env}")
            self._c = genai.Client(api_key=key)
        elif p == "openai_compat":
            from openai import OpenAI
            env = self.spec.get("api_key_env", "OPENAI_API_KEY")
            key = os.environ.get(env, "ollama" if "11434" in self.spec.get("base_url", "") else None)
            if not key:
                raise LLMError(f"falta la variable de entorno {env}")
            self._c = OpenAI(api_key=key, base_url=self.spec.get("base_url"))
        else:
            raise LLMError(f"proveedor desconocido: {p}")

    def generate(self, prompt):
        """Regresa un dict con text, finish_reason, model_version, tokens_in, tokens_out,
        latency_s y attempts."""
        last = None
        for attempt in range(self.max_retries):
            t0 = time.time()
            try:
                out = self._call(prompt)
                out["latency_s"] = round(time.time() - t0, 2)
                out["attempts"] = attempt + 1
                return out
            except Exception as e:  # noqa: BLE001
                last = e
                if not _retryable(e) or attempt == self.max_retries - 1:
                    break
                wait = min(120, 5 * 2 ** attempt) + random.uniform(0, 3)
                print(f"   reintento {attempt + 1} ({type(e).__name__}), espera {wait:.0f} s")
                time.sleep(wait)
        raise LLMError(f"{type(last).__name__}: {last}")

    def _call(self, prompt):
        if self.provider == "gemini":
            from google.genai import types
            cfg = {"max_output_tokens": self.max_tokens}
            if self.temperature is not None:
                cfg["temperature"] = self.temperature
            r = self._c.models.generate_content(model=self.model, contents=prompt,
                                                config=types.GenerateContentConfig(**cfg))
            um = getattr(r, "usage_metadata", None)
            try:
                fr = str(r.candidates[0].finish_reason)
            except (AttributeError, IndexError, TypeError):
                fr = None
            return {"text": r.text, "finish_reason": fr, "model_version": getattr(r, "model_version", self.model),
                    "tokens_in": getattr(um, "prompt_token_count", None),
                    "tokens_out": getattr(um, "candidates_token_count", None)}
        kw = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        if self.temperature is not None:
            kw["temperature"] = self.temperature
        if self.spec.get("use_max_completion_tokens"):
            kw["max_completion_tokens"] = self.max_tokens
        else:
            kw["max_tokens"] = self.max_tokens
        r = self._c.chat.completions.create(**kw)
        u = getattr(r, "usage", None)
        return {"text": r.choices[0].message.content, "finish_reason": r.choices[0].finish_reason,
                "model_version": getattr(r, "model", self.model),
                "tokens_in": getattr(u, "prompt_tokens", None),
                "tokens_out": getattr(u, "completion_tokens", None)}
