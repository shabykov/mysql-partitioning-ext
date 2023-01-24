import typing as t
from datetime import date

from databases import Database  # type: ignore

from mysql_partitioning_ext import schema


class SchemaEditor(schema.SchemaEditor):

    def __init__(self, db: Database):
        self.db = db

    async def add_partition(
            self,
            table: str,
            name: str,
            log_date: date
    ) -> None:
        sql = self.sql_add_partition % (table, name, log_date)
        await self.db.execute(sql)

    async def drop_partition(
            self,
            table: str,
            name: str
    ) -> None:
        sql = self.sql_drop_partition % (table, name)
        await self.db.execute(sql)

    async def truncate_partition(
            self,
            table: str,
            name: str
    ) -> None:
        sql = self.sql_truncate_partition % (table, name)
        await self.db.execute(sql)

    async def get_partition(
            self,
            table: str,
            name: str
    ) -> t.Optional[str]:
        sql = self.sql_get_partition % (name, table)

        item = await self.db.fetch_one(sql)
        if item is None:
            return None

        return dict(item)['PARTITION_NAME']


class RangePartitioningSchemaEditor(SchemaEditor):
    sql_add_partition = (
        "ALTER TABLE %s REORGANIZE PARTITION `p_max` INTO "
        "(PARTITION %s VALUES LESS THAN (to_days('%s')), "
        "PARTITION p_max VALUES LESS THAN MAXVALUE);"
    )


__all__ = (
    "SchemaEditor",
    "RangePartitioningSchemaEditor",
)
