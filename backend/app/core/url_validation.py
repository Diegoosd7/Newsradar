import ipaddress
import socket
import urllib.request
from urllib.parse import urlparse

from fastapi import HTTPException

_BLOCKED_TLDS = frozenset([".invalid", ".local", ".internal", ".test", ".localhost", ".example"])


def validate_url_safety(url_str: str) -> None:
    """Reject URLs pointing to loopback/private IPs or known-unresolvable TLDs."""
    try:
        parsed = urlparse(url_str)
        hostname = parsed.hostname or ""

        if not hostname:
            raise HTTPException(status_code=422, detail="URL no contiene host válido")

        hostname_lower = hostname.lower()
        for tld in _BLOCKED_TLDS:
            if hostname_lower.endswith(tld):
                raise HTTPException(status_code=422, detail="Dominio no accesible")

        try:
            ip_str = socket.gethostbyname(hostname)
        except socket.gaierror:
            raise HTTPException(status_code=422, detail="Dominio no resolvible")

        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_loopback or ip_obj.is_private:
                raise HTTPException(
                    status_code=422,
                    detail="URL no accesible: IP privada o de loopback no permitida",
                )
        except ValueError:
            pass

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=422, detail="URL no accesible")


def validate_rss_url(url_str: str) -> None:
    """Validate URL safety and that it serves RSS/XML content when reachable.

    If the URL cannot be fetched (network timeout, connection error) but passed
    safety checks, we accept it — only reject when the server responds with
    clearly non-RSS content (HTML, JSON, etc.).
    """
    validate_url_safety(url_str)

    try:
        req = urllib.request.Request(url_str, headers={"User-Agent": "NewsRadar/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            if any(ct in content_type for ct in ("xml", "rss", "atom")):
                return
            content = response.read(512)
            if content.strip().startswith((b"<?xml", b"<rss", b"<feed", b"<atom")):
                return
            raise HTTPException(
                status_code=422,
                detail="La URL no contiene contenido RSS/XML válido",
            )
    except HTTPException:
        raise
    except Exception:
        # Network errors (timeout, DNS, connection refused) are not treated as
        # validation failures — the URL passed safety checks, so accept it.
        return
