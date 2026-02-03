"""Fixed weather data loader with proper resource management."""

import csv
from pathlib import Path
from typing import Iterator, Optional
from functools import lru_cache
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class WeatherDataLoader:
    """Memory-efficient weather data loader."""

    MAX_CACHE_SIZE = 1000

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self._cache: dict = {}
        self._cache_hits = 0
        self._cache_misses = 0

    @contextmanager
    def _open_file(self, filepath: Path):
        """Context manager for safe file handling."""
        handle = None
        try:
            handle = open(filepath, "r", newline="", encoding="utf-8")
            yield handle
        finally:
            if handle:
                handle.close()

    def load_csv(self, filename: str) -> Iterator[dict]:
        """Load CSV file with proper resource management."""
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        with self._open_file(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def load_chunked(
        self,
        filename: str,
        chunk_size: int = 10000
    ) -> Iterator[list[dict]]:
        """Load large files in memory-efficient chunks."""
        chunk = []
        for row in self.load_csv(filename):
            chunk.append(row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def get_cached(self, key: str) -> Optional[dict]:
        """Get item from bounded cache."""
        if key in self._cache:
            self._cache_hits += 1
            return self._cache[key]
        self._cache_misses += 1
        return None

    def set_cached(self, key: str, value: dict) -> None:
        """Set item in bounded cache with eviction."""
        if len(self._cache) >= self.MAX_CACHE_SIZE:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = value

    def clear_cache(self) -> None:
        """Clear the cache."""
        self._cache.clear()
        logger.info("Cache cleared")

    @property
    def cache_stats(self) -> dict:
        """Get cache statistics."""
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": hit_rate,
            "size": len(self._cache)
        }
