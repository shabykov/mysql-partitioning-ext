class PartitioningError(RuntimeError):
    """Raised when the mysql_partitioning_ext configuration is broken or automatically
    creating/deleting partitions fails."""


__all__ = ("PartitioningError",)
