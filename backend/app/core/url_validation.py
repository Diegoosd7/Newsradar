import ipaddress
import urllib.request
from urllib.parse import urlparse

from fastapi import HTTPException

_BLOCKED_TLDS = frozenset([".invalid", ".local", ".internal", ".test", ".localhost"])

_BLOCKED_HOSTNAMES = frozenset(["localhost", "127.0.0.1", "::1"])


def validate_url_safety(url_str: str) -> None:
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

        try:
            ip_obj = ipaddress.ip_address(hostname)
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
    validate_url_safety(url_str)

    rss_mime_hints = (
        "application/rss",
        "application/atom",
        "application/rdf",
        "application/xml",
        "text/xml",
    )
    rss_content_prefixes = (b"<?xml", b"<rss", b"<feed", b"<atom", b"<rdf:")

    url_lower = url_str.lower()
    has_rss_url_hint = any(
        hint in url_lower
        for hint in ("rss", "feed", "atom", ".xml", ".rdf")
    )

    try:
        req = urllib.request.Request(
            url_str,
            headers={"User-Agent": "NewsRadar/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            content_type = response.headers.get("Content-Type", "").lower()

            if any(mime in content_type for mime in rss_mime_hints):
                return

            content = response.read(512)
            if content.strip().lower().startswith(rss_content_prefixes):
                return

            raise HTTPException(
                status_code=422,
                detail="La URL no contiene contenido RSS/XML válido",
            )

    except HTTPException:
        raise
    except Exception:
        if has_rss_url_hint:
            return

        raise HTTPException(
            status_code=422,
            detail="No se pudo verificar que la URL sea un feed RSS válido",
        )