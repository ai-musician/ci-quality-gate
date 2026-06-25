"""Small CIDR / IP helper utilities (standard library only).

A tiny, dependency-free module used to demo a CI/CD pipeline. The functions
are pure and easy to test exhaustively — exactly the kind of code a CI gate
should run on every push.
"""

from __future__ import annotations

import ipaddress


def ip_in_cidr(ip: str, cidr: str) -> bool:
    """Return True if ``ip`` falls within the ``cidr`` network range."""
    return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)


def cidrs_overlap(cidr_a: str, cidr_b: str) -> bool:
    """Return True if two CIDR ranges share any addresses."""
    net_a = ipaddress.ip_network(cidr_a, strict=False)
    net_b = ipaddress.ip_network(cidr_b, strict=False)
    return net_a.overlaps(net_b)


def num_usable_hosts(cidr: str) -> int:
    """Number of usable host addresses in a CIDR block.

    For IPv4 blocks of /30 or larger, the network and broadcast addresses are
    not usable hosts, so 2 are subtracted. /31 and /32 are special-cased to
    the common convention of 2 and 1 usable addresses respectively.
    """
    net = ipaddress.ip_network(cidr, strict=False)
    total = net.num_addresses
    if net.version == 4 and net.prefixlen <= 30:
        return total - 2
    return total
