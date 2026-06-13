"""Tavily wrapper for live literature/source retrieval with a curated fallback.

Contract:
- Works with no ``TAVILY_API_KEY`` (returns no live sources, never calls network).
- When the key is present, augments evidence with retrieved web/literature sources.
- Never raises; any failure falls back transparently and reports the mode.

The curated evidence in ``app/agents/evidence_agent.py`` remains the reliable
demo backbone; Tavily results are presented as additional, clearly-labelled
live sources so the jury can see real evidence routing when keys are set.
"""

from __future__ import annotations

import os

_TAVILY_ENDPOINT = "https://api.tavily.com/search"
_LIVE_CAVEAT = (
    "Live web/literature retrieval — relevance and quality vary; treat as a lead to "
    "verify, not validated evidence."
)


def tavily_status() -> dict:
    """Report Tavily availability without making a network call."""
    if os.getenv("TAVILY_API_KEY"):
        return {"available": True, "mode": "live"}
    return {"available": False, "mode": "fallback", "missing": ["TAVILY_API_KEY"]}


def _build_query(structured: dict, hypotheses: list[dict]) -> str:
    domain = structured.get("domain", "biotech experiment")
    mechs = ", ".join(h["mechanism"] for h in hypotheses[:3])
    return f"{domain}: evidence for {mechs} biomarkers and assays"


def search_evidence(structured: dict, hypotheses: list[dict], max_results: int = 3) -> dict:
    """Return ``{results, mode, detail}``. Network only when a key is present."""
    if not os.getenv("TAVILY_API_KEY"):
        return {"results": [], "mode": "fallback",
                "detail": "TAVILY_API_KEY not set; curated evidence used."}

    query = _build_query(structured, hypotheses)
    try:
        import requests

        response = requests.post(
            _TAVILY_ENDPOINT,
            json={
                "api_key": os.environ["TAVILY_API_KEY"],
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
            },
            timeout=12,
        )
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:  # noqa: BLE001 - demo must never crash on partner failure
        return {"results": [], "mode": "fallback",
                "detail": f"Tavily call failed ({type(exc).__name__}); curated evidence used."}

    results = []
    for item in (payload.get("results") or [])[:max_results]:
        snippet = (item.get("content") or "").strip()
        results.append({
            "source": item.get("title") or item.get("url") or "Tavily source",
            "claim": snippet[:400] + ("…" if len(snippet) > 400 else ""),
            "caveat": _LIVE_CAVEAT,
            "url": item.get("url", ""),
            "live": True,
        })
    detail = f"Tavily returned {len(results)} source(s) for: {query}"
    if not results:
        detail = "Tavily returned no usable sources; curated evidence used."
    return {"results": results, "mode": "live", "detail": detail}
