from typing import Optional, List, final

from .config import PartitioningConfig
from .plan import TablePartitioningPlan
from .schema import SchemaEditor


class PartitioningManager:
    def __init__(
            self,
            configs: List[PartitioningConfig],
            schema_editor: SchemaEditor
    ):
        self.configs = configs
        self.schema_editor = schema_editor

    @final
    async def apply_plans(self) -> None:
        for config in self.configs:
            plan = await self._plan_for_config(config)
            if plan:
                await plan.apply()

    @final
    async def _plan_for_config(
            self,
            config: PartitioningConfig,
    ) -> Optional[TablePartitioningPlan]:
        """Creates a mysql_partitioning_ext plan for one mysql_partitioning_ext config."""

        plan = TablePartitioningPlan(config, self.schema_editor)

        for partition in config.strategy.to_add():
            if await partition.exists(self.schema_editor):
                continue

            plan.creations.append(partition)

        for partition in config.strategy.to_drop():
            introspected_partition = await partition.exists(self.schema_editor)
            if not introspected_partition:
                break

            plan.deletions.append(partition)

        if len(plan.creations) == 0 and len(plan.deletions) == 0:
            return None

        return plan


__all__ = ("PartitioningManager",)
