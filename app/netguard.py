"""Outbound URL guard to mitigate SSRF on env-configurable endpoints.

Partner base URLs (``GEMINI_BASE_URL``, ``PIONEER_BASE_URL``) are read from the
environment. Before issuing a request we require https and verify the host does
not resolve to a private/loopback/link-local/reserved address — which blocks
attempts to reach internal services or the cloud metadata endpoint
(169.254.169.254). Raises ``ValueError`` on anything unsafe; callers run inside
try/except and fall back, so an unsafe URL degrades gracefully instead of firing.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse


def assert_safe_url(url: str) -> str:
    """Return ``url`` if it is a safe public https endpoint, else raise ValueError."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("outbound URL must use https")
    host = parsed.hostname
    if not host:
        raise ValueError("outbound URL has no host")

    try:
        infos = socket.getaddrinfo(host, parsed.port or 443, proto=socket.IPPROTO_TCP)
    except OSError as exc:  # DNS failure / unknown host
        raise ValueError(f"cannot resolve outbound host: {host}") from exc

    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"outbound URL resolves to non-public address {ip}")
    return url
