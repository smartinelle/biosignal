# Security Policy

BioSignal Navigator is a **research-workflow demo**, not a clinical, diagnostic, or
production medical system. It is built for the {Tech: Europe} Munich AI Hackathon.
Security is still treated as a first-class concern.

## Reporting a vulnerability

Please report security issues privately to **sacha.martinelle@sciencespo.fr** rather
than opening a public issue. We aim to acknowledge reports within a few days.

## Security posture

- **No secrets in the repo.** All credentials are read from environment variables
  (`.env`, gitignored). `.env.example` ships placeholders only. There are no API
  keys in the source tree or git history.
- **Safe by default.** Every partner integration (Gemini/OpenRouter, Tavily,
  Pioneer) has a deterministic, no-network fallback. The app never calls the network
  unless the corresponding key is set, and a failed partner call degrades gracefully
  instead of crashing or leaking errors to the user.
- **No dangerous execution.** No `eval`, `exec`, `pickle`, `yaml.load`, `os.system`,
  `subprocess`, or `shell=True`. No deserialization of untrusted input.
- **No SSRF surface.** All outbound requests go to fixed, vendor endpoints (overridable
  only via trusted environment variables, never via end-user input) and use explicit
  timeouts.
- **No HTML/JS injection.** Streamlit escapes user content by default. The single use
  of `unsafe_allow_html` renders a static CSS block only — no user input flows into it.
- **Loopback by default.** `.streamlit/config.toml` binds to `127.0.0.1`, disables
  usage telemetry, and keeps XSRF/CORS protection on. Bind to `0.0.0.0` only when you
  intentionally need remote access.

## Dependencies

Python dependencies are listed in `requirements.txt` with security-conscious floors
(e.g. `requests>=2.32.4` for CVE-2024-47081). Run an SCA/secret scan before each
submission:

```bash
pip install -r requirements.txt
pip-audit            # optional: dependency CVE check
```

This repository is also scanned with [Aikido](https://www.aikido.dev/) for SCA,
secrets, and SAST findings as part of the hackathon security side challenge.

## Scope and limitations

This is a hackathon demo with **no authentication** — do not deploy it publicly with
real or sensitive data, and do not treat its output as medical or clinical guidance.
All outputs require human expert review.
