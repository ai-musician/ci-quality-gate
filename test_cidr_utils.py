"""Tests for cidr_utils — run by the CI pipeline on every push/PR."""

import pytest

from cidr_utils import cidrs_overlap, ip_in_cidr, num_usable_hosts


class TestIpInCidr:
    @pytest.mark.parametrize(
        "ip,cidr,expected",
        [
            ("10.0.0.5", "10.0.0.0/24", False),
            ("10.0.1.5", "10.0.0.0/24", False),
            ("192.168.1.1", "192.168.0.0/16", True),
            ("172.16.0.1", "10.0.0.0/8", False),
        ],
    )
    def test_membership(self, ip, cidr, expected):
        assert ip_in_cidr(ip, cidr) is expected

    def test_invalid_ip_raises(self):
        with pytest.raises(ValueError):
            ip_in_cidr("not-an-ip", "10.0.0.0/24")


class TestCidrsOverlap:
    def test_overlapping_ranges(self):
        assert cidrs_overlap("10.0.0.0/24", "10.0.0.0/25") is True

    def test_disjoint_ranges(self):
        assert cidrs_overlap("10.0.0.0/24", "10.0.1.0/24") is False

    def test_identical_ranges(self):
        assert cidrs_overlap("10.0.0.0/24", "10.0.0.0/24") is True


class TestNumUsableHosts:
    @pytest.mark.parametrize(
        "cidr,expected",
        [
            ("10.0.0.0/24", 254),
            ("10.0.0.0/30", 2),
            ("10.0.0.0/31", 2),
            ("10.0.0.1/32", 1),
        ],
    )
    def test_host_counts(self, cidr, expected):
        assert num_usable_hosts(cidr) == expected
