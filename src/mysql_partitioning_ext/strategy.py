from abc import abstractmethod
from typing import Generator

from .partition import Partition


class PartitioningStrategy:
    """Base class for implementing a partitioning strategy for a partitioned
    table."""

    @abstractmethod
    def to_add(
        self,
    ) -> Generator[Partition, None, None]:
        """Generates a list of partitions to be created."""

    @abstractmethod
    def to_drop(
        self,
    ) -> Generator[Partition, None, None]:
        """Generates a list of partitions to be deleted."""


__all__ = ("PartitioningStrategy",)
