from datetime import date

from mysql_partitioning_ext import Partition
from mysql_partitioning_ext import SchemaEditor


class LogDatePartition(Partition):
    _log_date_format = "%Y_%m_%d"

    def __init__(
            self,
            table: str,
            log_date: date
    ) -> None:
        self.table = table
        self.log_date = log_date

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return "p{log_date}".format(
            log_date=self.log_date.strftime(self._log_date_format).lower()
        )

    async def exists(
            self,
            schema_editor: SchemaEditor
    ) -> bool:
        res = await schema_editor.get_partition(
            self.table,
            self.name
        )
        return res is not None

    async def add(
            self,
            schema_editor: SchemaEditor
    ) -> None:
        await schema_editor.add_partition(
            self.table,
            self.name,
            log_date=self.log_date,
        )

    async def truncate(
            self,
            schema_editor: SchemaEditor,
    ) -> None:
        await schema_editor.truncate_partition(
            self.table,
            self.name
        )

    async def drop(
            self,
            schema_editor: SchemaEditor
    ) -> None:
        await schema_editor.drop_partition(
            self.table,
            self.name
        )


__all__ = ("LogDatePartition",)
