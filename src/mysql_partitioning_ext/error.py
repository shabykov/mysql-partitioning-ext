class PartitioningError(RuntimeError):
    """Raised when the partitioning configuration is broken or automatically
    creating/deleting partitions fails."""


__all__ = ("PartitioningError",)
