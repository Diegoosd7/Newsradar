import ipaddress
import urllib.request
from urllib.parse import urlparse

from fastapi import HTTPException

_BLOCKED_TLDS = frozenset([".invalid", ".local", ".internal", ".test", ".localhost"])

_BLOCKED_HOSTNAMES = frozenset(["localhost", "127.0.0.1", "::1"])


def validate_url_safety(url_str: str) -> None:
    """Reject URLs pointing to loopback/private IPs or known-unresolvable TLDs."""
    try:
        parsed = urlparse(url_str)
        hostname = parsed.hostname or ""

        if not hostname:
            raise HTTPException(status_code=422, detail="URL no contiene host válido")

        hostname_lower = hostname.lower()

        if hostname_lower in _BLOCKED_HOSTNAMES:
            raise HTTPException(status_code=422, detail="Dominio no accesible")

        for tld in _BLOCKED_TLDS:
            if hostname_lower.endswith(tld):
                raise HTTPException(status_code=422, detail="Dominio no accesible")

        # Si parece una IP directa, comprobar que no sea privada
        try:
            ip_obj = ipaddress.ip_address(hostname)
            if ip_obj.is_loopback or ip_obj.is_private:
                raise HTTPException(
                    status_code=422,
                    detail="URL no accesible: IP privada o de loopback no permitida",
                )
        except ValueError:
            pass  # No es una IP, es un hostname normal — aceptar

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=422, detail="URL no accesible")


def validate_rss_url(url_str: str) -> None:
    """Validate URL safety and that it serves RSS/XML content when reachable."""
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
        return