"""
Gandi Dynamic DNS 1.2

Dynamic DNS Update Client for Gandi's LiveDNS

Copyright (C) 2024 Winston Astrachan
Released under the terms of the MIT license
"""

import os
from pathlib import Path
import requests
from typing import Optional, Tuple


class Cache(object):
    def __init__(self, base_folder: Path):
        self._base_folder = base_folder

    def _get_file_path(self, key: str) -> Path:
        return self._base_folder / key

    def get(self, key: str) -> Optional[str]:
        cache_path = self._get_file_path(key)
        if cache_path.exists():
            return cache_path.read_text()
        return None

    def set(self, key: str, value: str) -> None:
        cache_path = self._get_file_path(key)
        cache_path.write_text(value)


class GandiUpdater(object):
    def __init__(self, cache: Cache, token: str, base_url: str, domain: str, record: str, ttl: int):
        self._cache = cache
        self._update_url = f"{base_url}/domains/{domain}/records/{record}"
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._record_mapping = {
            'ipv4': 'A',
            'ipv6': 'AAAA',
        }
        self._domain = domain
        self._record = record
        self._ttl = ttl

    def get_ip(self, version: str) -> Tuple[Optional[str], bool]:
        """Gets the current public IP address
        version: ipv4 or ipv6

        Returns:
            (address, changed)
                address: (str) current ip address
                changed: (bool) True if ip address has changed

        """

        response = requests.get(f"https://{version}.icanhazip.com")
        address = response.text.strip() if response.ok else None
        old_address = self._cache.get(version)
        if old_address is None:
            old_address = self.get_record(version).strip()
        changed = address is not None and address != old_address
        if address and changed:
            self._cache.set(version, address)
        return (address, changed)

    def update_record(self, version: str) -> None:
        record_type = self._record_mapping[version]
        ip, changed = self.get_ip(version)
        if not ip:
            print(f"Unable to fetch current {version} address")
        elif changed:
            try:
                response = requests.put(
                                        f"{self._update_url}/{record_type}",
                                        headers=self._headers,
                                        json={
                                            "rrset_values": [f"{ip}"],
                                            "rrset_ttl": self._ttl
                                        },
                           )
                response.raise_for_status()
            except Exception as e:
                print(f"Unable to update DNS record: {e}")
            else:
                print(f"Set IP to {ip} for {record_type} record '{self._record}' for {self._domain}")
        else:
            print(f"No change in external IP ({ip}), not updating {record_type} record")

    def get_record(self, version: str) -> str:
        record_type = self._record_mapping[version]
        try:
            response = requests.get(
                                    f"{self._update_url}/{record_type}",
                                    headers=self._headers,
                       )
            response.raise_for_status()
        except Exception as e:
            print(f"Unable to get DNS record: {e}")
        return response.json()['rrset_values'][0]


if __name__ == "__main__":
    cache = Cache(Path(os.environ.get('CACHE_PATH', 'data')))
    url = os.environ.get("GANDI_URL", "https://dns.api.gandi.net/api/v5")
    token = os.environ.get("GANDI_TOKEN", '')
    domain = os.environ.get("GANDI_DOMAIN")
    record = os.environ.get("GANDI_RECORD", "@")
    protocols = os.environ.get("PROTOCOLS", 'ipv4,ipv6').split(',')
    ttl = os.environ.get("GANDI_TTL", "300")
    if domain is None:
        print('Invalid domain specified')
    else:
        gandi = GandiUpdater(cache, token, url, domain, record, int(ttl))
        for protocol in protocols:
            gandi.update_record(protocol)
