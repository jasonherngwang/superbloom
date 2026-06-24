from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable


class BloomFilter:
    """Probabilistic membership test with no false negatives."""

    def __init__(self, capacity: int, error_rate: float = 0.01) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate must be between 0 and 1")

        self.capacity = capacity
        self.error_rate = error_rate
        self.size = self._optimal_size(capacity, error_rate)
        self.hash_count = self._optimal_hash_count(capacity, self.size)
        self.bits = bytearray(math.ceil(self.size / 8))
        self.items_added = 0

    def add(self, value: str) -> None:
        """Add a value to the filter."""
        for index in self._hashes(value):
            bucket, offset = divmod(index, 8)
            self.bits[bucket] |= 1 << offset
        self.items_added += 1

    def update(self, values: Iterable[str]) -> None:
        for value in values:
            self.add(value)

    def __contains__(self, value: str) -> bool:
        return all(self._is_set(index) for index in self._hashes(value))

    @property
    def fill_ratio(self) -> float:
        filled = sum(byte.bit_count() for byte in self.bits)
        return filled / self.size

    def _is_set(self, index: int) -> bool:
        bucket, offset = divmod(index, 8)
        return bool(self.bits[bucket] & (1 << offset))

    def _hashes(self, value: str) -> Iterable[int]:
        encoded = value.encode("utf-8")
        digest = hashlib.blake2b(encoded, digest_size=16).digest()
        left = int.from_bytes(digest[:8], "big")
        right = int.from_bytes(digest[8:], "big")

        for seed in range(self.hash_count):
            yield (left + seed * right) % self.size

    @staticmethod
    def _optimal_size(capacity: int, error_rate: float) -> int:
        numerator = capacity * math.log(error_rate)
        denominator = math.log(2) ** 2
        return math.ceil(-numerator / denominator)

    @staticmethod
    def _optimal_hash_count(capacity: int, size: int) -> int:
        return max(1, round((size / capacity) * math.log(2)))


def bloom_report(filter_: BloomFilter, probes: Iterable[str]) -> dict[str, bool]:
    return {name: name in filter_ for name in probes}


if __name__ == "__main__":
    wildflowers = BloomFilter(capacity=128, error_rate=0.02)
    wildflowers.update(["poppy", "lupine", "clarkia", "brodiaea"])

    results = bloom_report(wildflowers, ["poppy", "phacelia", "sage"])
    print(f"fill ratio: {wildflowers.fill_ratio:.2%}")
    print(results)
