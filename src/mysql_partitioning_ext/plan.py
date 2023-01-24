from dataclasses import dataclass, field
from typing import List, final

from .config import PartitioningConfig
from .schema import SchemaEditor
from .partition import Partition


@dataclass
class TablePartitioningPlan:
    """Describes the partitions that are going to be created/deleted for a
    particular mysql_partitioning_ext config.

    A "mysql_partitioning_ext config" applies to one model.
    """

    config: PartitioningConfig
    schema_editor: SchemaEditor
    creations: List[Partition] = field(default_factory=list)
    deletions: List[Partition] = field(default_factory=list)

    @final
    async def apply(self) -> None:
        for partition in self.creations:
            await partition.add(self.schema_editor)

        for partition in self.deletions:
            await partition.truncate(self.schema_editor)
            await partition.drop(self.schema_editor)


__all__ = ("TablePartitioningPlan",)
