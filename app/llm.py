"""Gemini wrapper for mechanism/memo synthesis with a deterministic fallback.

Supports two live routes plus a deterministic fallback:

1. OpenAI-compatible (OpenRouter) — used when ``OPENROUTER_API_KEY`` is set, or
   when ``GEMINI_BASE_URL`` is set, or when the ``GEMINI_API_KEY`` value looks
   like an OpenRouter key (``sk-or...``). Calls ``{base}/chat/completions``.
2. Native Gemini — used when ``GEMINI_API_KEY`` is a native Google key.
3. Deterministic fallback — no key, no network call.

Contract: works with no key, never makes a network call without a key, never
raises. Any failure falls back transparently and reports the mode.
"""

from __future__ import annotations

import os

try:
    from netguard import assert_safe_url
except ModuleNotFoundError:  # package import context
    from app.netguard import assert_safe_url

_OPENROUTER_BASE = "https://openrouter.ai/api/v1"

_SAFETY_FOOTER = (
    "This is a research-workflow troubleshooting memo. It does not diagnose, "
    "predict viability, or recommend a transplant/discard or treatment decision. "
    "A senior scientist must review before any protocol change."
)


def _resolve_provider() -> dict | None:
    """Decide which live route to use from the environment. ``None`` = fallback."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    base_url = os.getenv("GEMINI_BASE_URL")

    # Explicit OpenRouter key wins.
    if openrouter_key:
        return {
            "provider": "openrouter",
            "key": openrouter_key,
            "base_url": (base_url or _OPENROUTER_BASE).rstrip("/"),
            "model": os.getenv("OPENROUTER_MODEL") or os.getenv("GEMINI_MODEL") or "google/gemini-2.5-flash",
        }

    if gemini_key:
        # An explicit base URL, or a key that looks like OpenRouter, => OpenAI-compatible.
        if base_url or gemini_key.startswith("sk-or"):
            return {
                "provider": "openrouter",
                "key": gemini_key,
                "base_url": (base_url or _OPENROUTER_BASE).rstrip("/"),
                "model": os.getenv("GEMINI_MODEL") or "google/gemini-2.5-flash",
            }
        # Otherwise treat as a native Google Gemini key.
        return {
            "provider": "gemini",
            "key": gemini_key,
            "base_url": None,
            "model": os.getenv("GEMINI_MODEL") or "gemini-2.5-flash",
        }

    return None


def gemini_status() -> dict:
    """Report LLM availability and route without making a network call."""
    provider = _resolve_provider()
    if provider is None:
        return {"available": False, "mode": "fallback", "missing": ["GEMINI_API_KEY or OPENROUTER_API_KEY"]}
    return {
        "available": True,
        "mode": "live",
        "provider": provider["provider"],
        "model": provider["model"],
    }


def _fallback_memo(structured: dict, hypotheses: list[dict], evidence: list[dict],
                   measurements: list[dict], question: str) -> str:
    domain = structured.get("domain", "biotech experiment")
    signals = ", ".join(structured.get("signals_detected", [])) or "the reported readouts"
    top = hypotheses[0]["mechanism"] if hypotheses else "an undetermined mechanism"
    first_measure = measurements[0]["measurement"] if measurements else "a discriminating assay"
    if len(hypotheses) > 1:
        hypothesis_line = (
            f"**Most testable hypothesis first:** {top}, alongside "
            + ", ".join(h["mechanism"] for h in hypotheses[1:3]) + "."
        )
    else:
        hypothesis_line = f"**Most testable hypothesis first:** {top}."
    lines = [
        f"**Domain:** {domain}.",
        f"**What we see:** {signals}. These macro signals are underdetermined — "
        "several mechanisms remain consistent with them.",
        hypothesis_line,
        f"**Next best measurement:** {first_measure} — chosen to discriminate between the "
        "leading mechanisms, not to confirm a single answer.",
        f"**Open question for a human expert:** {question}",
        f"\n_{_SAFETY_FOOTER}_",
    ]
    return "\n\n".join(lines)


def _build_prompt(structured: dict, hypotheses: list[dict], evidence: list[dict],
                  measurements: list[dict], question: str) -> str:
    hyp = "; ".join(h["mechanism"] for h in hypotheses)
    meas = "; ".join(m["measurement"] for m in measurements)
    ev = "; ".join(f"{e['source']}: {e['claim']}" for e in evidence)
    return (
        "You are a careful biotech R&D troubleshooting assistant. Write a short memo "
        "(max ~120 words) for a senior scientist debugging an ambiguous living-tissue "
        "experiment. Use only the structured inputs. Write concise prose — do NOT invent a "
        "date, recipient, or letterhead. Frame mechanisms as POSSIBLE, never certain. Do NOT "
        "diagnose, predict viability, or recommend transplant/discard or treatment. End by "
        "naming the single next measurement that best reduces uncertainty and restating that "
        "a human must review.\n\n"
        f"Note: {structured.get('raw_note', '')}\n"
        f"Candidate mechanisms: {hyp}\n"
        f"Evidence: {ev}\n"
        f"Candidate measurements: {meas}\n"
        f"Human review question: {question}\n"
    )


def _call_openrouter(provider: dict, prompt: str) -> str:
    import requests

    base_url = assert_safe_url(provider["base_url"])  # SSRF guard on env-configured URL
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {provider['key']}",
            "HTTP-Referer": "https://github.com/biosignal-navigator",
            "X-Title": "BioSignal Navigator",
        },
        json={
            "model": provider["model"],
            "messages": [
                {"role": "system", "content": "You are a careful biotech R&D troubleshooting assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 400,
        },
        timeout=20,
        allow_redirects=False,
    )
    response.raise_for_status()
    payload = response.json()
    return (payload["choices"][0]["message"]["content"] or "").strip()


def _call_gemini(provider: dict, prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=provider["key"])
    model = genai.GenerativeModel(provider["model"])
    response = model.generate_content(prompt)
    return (getattr(response, "text", "") or "").strip()


def synthesize_memo(structured: dict, hypotheses: list[dict], evidence: list[dict],
                    measurements: list[dict], question: str) -> dict:
    """Return ``{text, mode, detail}``; LLM-enriched when a key is present."""
    fallback = _fallback_memo(structured, hypotheses, evidence, measurements, question)
    provider = _resolve_provider()
    if provider is None:
        return {"text": fallback, "mode": "fallback",
                "detail": "No LLM key set; deterministic memo used."}

    prompt = _build_prompt(structured, hypotheses, evidence, measurements, question)
    label = f"{provider['provider']}:{provider['model']}"
    try:
        if provider["provider"] == "openrouter":
            text = _call_openrouter(provider, prompt)
        else:
            text = _call_gemini(provider, prompt)
    except Exception as exc:  # noqa: BLE001 - demo must never crash on partner failure
        return {"text": fallback, "mode": "fallback",
                "detail": f"LLM call failed via {label} ({type(exc).__name__}); deterministic memo used."}

    if not text:
        return {"text": fallback, "mode": "fallback",
                "detail": f"LLM ({label}) returned no text; deterministic memo used."}
    return {"text": f"{text}\n\n_{_SAFETY_FOOTER}_", "mode": "live",
            "detail": f"Memo synthesized via {label}."}
