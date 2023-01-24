import typing as t
from abc import abstractmethod
from datetime import date


class SchemaEditor:
    sql_add_partition = (
        "ALTER TABLE %s ADD PARTITION "
        "(PARTITION %s VALUES IN ('%s'));"
    )
    sql_drop_partition = (
        "ALTER TABLE %s DROP PARTITION %s;"
    )
    sql_truncate_partition = (
        "ALTER TABLE %s TRUNCATE PARTITION %s;"
    )
    sql_get_partition = (
        "SELECT PARTITION_NAME FROM INFORMATION_SCHEMA.PARTITIONS "
        "WHERE PARTITION_NAME = '%s' and TABLE_NAME = '%s';"
    )

    @abstractmethod
    async def add_partition(
            self,
            table: str,
            name: str,
            log_date: date
    ) -> None:
        """Add partition to table"""

    @abstractmethod
    async def drop_partition(
            self,
            table: str,
            name: str
    ) -> None:
        """Drop partition from table"""

    @abstractmethod
    async def truncate_partition(
            self,
            table: str,
            name: str
    ) -> None:
        """Truncate partition table"""

    @abstractmethod
    async def get_partition(
            self,
            table: str,
            name: str
    ) -> t.Optional[str]:
        """Get partition"""
