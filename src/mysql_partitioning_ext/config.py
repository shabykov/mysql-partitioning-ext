from .strategy import PartitioningStrategy


class PartitioningConfig:
    """Configuration for mysql_partitioning_ext a specific table according to the
    specified strategy."""

    def __init__(
        self,
        strategy: PartitioningStrategy,
    ) -> None:
        self.strategy = strategy


__all__ = (
    "PartitioningConfig",
)
