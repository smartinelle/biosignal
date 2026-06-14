"""Tavily wrapper for live literature/source retrieval with a curated fallback.

Contract:
- Works with no ``TAVILY_API_KEY`` (returns no live sources, never calls network).
- When the key is present, augments evidence with retrieved web/literature sources.
- Never raises; any failure falls back transparently and reports the mode.

Relevance/accuracy strategy:
- Build a focused scientific query from the detected signals + top mechanisms.
- Over-fetch, then *post-filter and tier* results ourselves. Tavily's
  ``include_domains`` is not reliably honoured on this endpoint, so we rank by
  source trust: peer-reviewed journals first, then reputable vendor/protocol
  docs, then general web — and drop low-trust hosts (forums, social, blogs).
- Within a tier, rank by Tavily's own relevance score.

The curated evidence in ``app/agents/evidence_agent.py`` remains the reliable
demo backbone; Tavily results are presented as additional, clearly-labelled
live sources so the jury can see real evidence routing when keys are set.
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

_TAVILY_ENDPOINT = "https://api.tavily.com/search"

# Tier 0 — peer-reviewed journals, preprint servers, and peer-reviewed protocols.
_PEER_REVIEWED = {
    "pubmed.ncbi.nlm.nih.gov", "pmc.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov", "europepmc.org",
    "nature.com", "science.org", "sciencemag.org", "cell.com", "sciencedirect.com",
    "biorxiv.org", "medrxiv.org", "preprints.org",
    "thelancet.com", "nejm.org", "bmj.com",
    "frontiersin.org", "springer.com", "link.springer.com", "springeropen.com",
    "wiley.com", "onlinelibrary.wiley.com", "mdpi.com", "plos.org", "journals.plos.org",
    "academic.oup.com", "oup.com", "jbc.org", "asm.org", "journals.asm.org",
    "pnas.org", "embopress.org", "rupress.org", "elifesciences.org",
    "biomedcentral.com", "tandfonline.com", "sagepub.com", "journals.sagepub.com",
    "aacrjournals.org", "royalsocietypublishing.org", "physiology.org",
    "jove.com", "protocols.io", "bio-protocol.org",
}

# Tier 1 — reputable assay/reagent vendors and protocol authorities. For *experiment
# troubleshooting* these are often the most actionable sources, so they rank just
# below peer-reviewed work rather than being discarded.
_REPUTABLE_VENDOR = {
    "idtdna.com", "thermofisher.com", "lifetechnologies.com", "neb.com", "qiagen.com",
    "bio-rad.com", "biorad.com", "sigmaaldrich.com", "merckmillipore.com", "promega.com",
    "takarabio.com", "agilent.com", "abcam.com", "biocompare.com", "labmanager.com",
    "biosearchtech.com", "pcrbio.com", "addgene.org", "azurebiosystems.com", "biotium.com",
    "lgcgroup.com", "thermofisher.cn",
}

# Tier 3 — low-trust hosts we never surface as evidence.
_EXCLUDE = {
    "reddit.com", "quora.com", "facebook.com", "twitter.com", "x.com", "instagram.com",
    "youtube.com", "tiktok.com", "pinterest.com", "medium.com", "wordpress.com",
    "blogspot.com", "linkedin.com", "wikipedia.org", "studocu.com", "coursehero.com",
    "chegg.com",
}

_TIER_NAME = {0: "peer-reviewed", 1: "vendor/protocol", 2: "general web"}
# Trust bonus added to Tavily's relevance score so ranking balances *relevance*
# and *source trust* instead of hard-prioritising one over the other.
_TIER_BONUS = {0: 0.30, 1: 0.10, 2: 0.0}

# Below this Tavily relevance score a result is treated as a weak/tangential lead.
_MIN_SCORE = 0.4

_LIVE_CAVEAT = (
    "Live web/literature retrieval — relevance and quality vary; treat as a lead to "
    "verify, not validated evidence."
)
_WEAK_CAVEAT = (
    "Low-relevance / general-web lead — likely tangential; verify directly before using."
)


def tavily_status() -> dict:
    """Report Tavily availability without making a network call."""
    if os.getenv("TAVILY_API_KEY"):
        return {"available": True, "mode": "live"}
    return {"available": False, "mode": "fallback", "missing": ["TAVILY_API_KEY"]}


def _build_query(structured: dict, hypotheses: list[dict]) -> str:
    """A focused scientific query grounded in the actual run, not just the domain."""
    domain = structured.get("domain", "biotech experiment")
    mechs = [h["mechanism"] for h in hypotheses[:3] if h.get("mechanism")]
    signals = list(structured.get("signals_detected", [])[:5])
    mech_str = "; ".join(mechs) if mechs else "failure mechanisms"
    query = f"{mech_str} in {domain}: mechanism, biomarkers, and discriminating assays"
    if signals:
        query += f". Observed signals: {', '.join(signals)}"
    query += ". Peer-reviewed studies and methods."
    return query


def _host(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def _matches(host: str, domains: set[str]) -> bool:
    return any(host == d or host.endswith("." + d) for d in domains)


def _tier(url: str) -> int:
    """0 peer-reviewed · 1 vendor/protocol · 2 general web · 3 excluded."""
    host = _host(url)
    if not host or _matches(host, _EXCLUDE):
        return 3
    if _matches(host, _PEER_REVIEWED):
        return 0
    if _matches(host, _REPUTABLE_VENDOR):
        return 1
    return 2


def _tavily_call(api_key: str, query: str, max_results: int) -> list[dict]:
    """One Tavily request. Returns raw result dicts (may be empty); raises on error."""
    import requests

    response = requests.post(
        _TAVILY_ENDPOINT,
        json={
            "api_key": api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced",
            "topic": "general",
        },
        timeout=15,
        allow_redirects=False,
    )
    response.raise_for_status()
    return list(response.json().get("results") or [])


def search_evidence(structured: dict, hypotheses: list[dict], max_results: int = 3) -> dict:
    """Return ``{results, mode, detail}``. Network only when a key is present."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"results": [], "mode": "fallback",
                "detail": "TAVILY_API_KEY not set; curated evidence used."}

    query = _build_query(structured, hypotheses)
    try:
        # Over-fetch so trust-tiering and score ranking have material to work with.
        raw = _tavily_call(api_key, query, max(max_results * 4, 12))
    except Exception as exc:  # noqa: BLE001 - demo must never crash on partner failure
        return {"results": [], "mode": "fallback",
                "detail": f"Tavily call failed ({type(exc).__name__}); curated evidence used."}

    # Annotate, drop excluded hosts, then rank by blended (relevance + trust) score.
    def _blended(ti: tuple[int, dict]) -> float:
        tier, item = ti
        return (item.get("score") or 0.0) + _TIER_BONUS.get(tier, 0.0)

    candidates = [(_tier(item.get("url", "")), item) for item in raw]
    candidates = [(t, item) for t, item in candidates if t != 3]
    candidates.sort(key=_blended, reverse=True)

    selected = candidates[:max_results]
    # Always include at least one peer-reviewed source when one exists, for
    # credibility — then keep the most relevant vendor/web leads alongside it.
    peer = [c for c in candidates if c[0] == 0]
    if peer and max_results >= 1 and not any(t == 0 for t, _ in selected):
        selected = selected[: max_results - 1] + [peer[0]]
        selected.sort(key=_blended, reverse=True)

    results = []
    for tier, item in selected:
        score = item.get("score")
        snippet = (item.get("content") or "").strip()
        weak = tier == 2 or (score is not None and score < _MIN_SCORE)
        results.append({
            "source": item.get("title") or item.get("url") or "Tavily source",
            "claim": snippet[:400] + ("…" if len(snippet) > 400 else ""),
            "caveat": _WEAK_CAVEAT if weak else _LIVE_CAVEAT,
            "url": item.get("url", ""),
            "relevance_score": round(score, 2) if isinstance(score, (int, float)) else None,
            "source_tier": _TIER_NAME[tier],
            "live": True,
        })

    if not results:
        return {"results": [], "mode": "fallback",
                "detail": "Tavily returned no usable sources; curated evidence used."}

    n_peer = sum(1 for tier, _ in selected if tier == 0)
    detail = (f"Tavily returned {len(results)} ranked source(s) "
              f"({n_peer} peer-reviewed) for: {query}")
    return {"results": results, "mode": "live", "detail": detail}
