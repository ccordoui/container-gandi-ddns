"""
Gandi Dynamic DNS 1.2

Dynamic DNS Update Client for Gandi's LiveDNS

Copyright (C) 2024 Winston Astrachan
Released under the terms of the MIT license
"""

import os
from pathlib import Path
import requests
from typing import Optional, Dict, Tuple


def _get_cache_value(key: str) -> Optional[str]:
    """Returns a value for a cache key, or None"""
    address = None
    try:
        with Path(key).open() as f:
            address = f.read()
    except FileNotFoundError:
        address = None
    return address


def _set_cache_value(key: str, value: str) -> str:
    """Sets or updates the value for a cache key"""
    Path(key).write_text(value)
    return value


def _get_gandi_headers() -> Dict[str, str]:
    """Returns API request headers for the Gandi API"""
    return {
        "X-Api-Key": GANDI_KEY,
        "Content-Type": "application/json",
    }


def get_ipv4() -> Tuple[Optional[str], bool]:
    """Gets the current public IPV4 address

    Returns:
        (address, changed)
            address: (str) current ipv4 address
            changed: (bool) True if ipv4 address has changed

    """
    try:
        response = requests.get("https://ipv4.icanhazip.com/")
        response.raise_for_status()
    except Exception:
        address = None
    else:
        address = response.text.strip()
    changed = False
    if address and address != _get_cache_value(CACHE_KEY_IPV4):
        _set_cache_value(CACHE_KEY_IPV4, address)
        changed = True
    return (address, changed)


def get_ipv6() -> Tuple[Optional[str], bool]:
    """Gets the current public IPV6 address

    Returns:
        (address, changed)
            address: (str) current ipv6 address
            changed: (bool) True if ipv6 address has changed

    """
    try:
        response = requests.get("https://ipv6.icanhazip.com/")
        response.raise_for_status()
    except Exception:
        address = None
    else:
        address = response.text.strip()
    changed = False
    if address and address != _get_cache_value(CACHE_KEY_IPV6):
        _set_cache_value(CACHE_KEY_IPV6, address)
        changed = True
    return (address, changed)


def update_a_record() -> None:
    """Check public IPV4 address and update A record if a change has occured"""
    ip, changed = get_ipv4()
    if not ip:
        print("Unable to fetch current IPV4 address")
    elif changed:
        try:
            payload = {"rrset_values": [f"{ip}"]}
            response = requests.put(
                                    f"{GANDI_URL}domains/{GANDI_DOMAIN}/records/{GANDI_RECORD}/A",
                                    json=payload,
                                    headers=_get_gandi_headers(),
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Unable to update DNS record: {e}")
        else:
            print(f"Set IP to {ip} for A record '{GANDI_RECORD}' for {GANDI_DOMAIN}")
    else:
        print(f"No change in external IP ({ip}), not updating A record")


def update_aaaa_record() -> None:
    """Check public IPV6 address and update AAAA record if a change has occured"""
    ip, changed = get_ipv6()
    if not ip:
        print("Unable to fetch current IPV6 address")
    elif changed:
        try:
            payload = {"rrset_values": [f"{ip}"]}
            response = requests.put(
                f"{GANDI_URL}domains/{GANDI_DOMAIN}/records/{GANDI_RECORD}/AAAA",
                json=payload,
                headers=_get_gandi_headers(),
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Unable to update DNS record: {e}")
        else:
            print(f"Set IP to {ip} for AAAA record '{GANDI_RECORD}' for {GANDI_DOMAIN}")
    else:
        print(f"No change in external IP ({ip}), not updating AAAA record")


if __name__ == "__main__":
    CACHE_KEY_IPV4 = os.environ.get("CACHE_KEY_IPV4", "/run/ipv4.last")
    CACHE_KEY_IPV6 = os.environ.get("CACHE_KEY_IPV6", "/run/ipv6.last")
    GANDI_URL = os.environ.get("GANDI_URL", "https://dns.api.gandi.net/api/v5/")
    GANDI_KEY = os.environ.get("GANDI_KEY", '')
    GANDI_DOMAIN = os.environ.get("GANDI_DOMAIN", False)
    GANDI_RECORD = os.environ.get("GANDI_RECORD", "@")
    update_a_record()
    update_aaaa_record()
