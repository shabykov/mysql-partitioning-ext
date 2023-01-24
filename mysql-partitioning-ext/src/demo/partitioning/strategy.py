from datetime import date
from typing import Generator

from dateutil.relativedelta import relativedelta  # type: ignore

from mysql_partitioning_ext import TimePartitionSize
from mysql_partitioning_ext.strategy import PartitioningStrategy

from .partition import LogDatePartition


class RangePartitioningStrategy(PartitioningStrategy):
    """Strategy for partitioning a specific table according to the
    specified date range partitioning."""

    date_shift = relativedelta(days=0)

    def __init__(
            self,
            table: str,
            size: TimePartitionSize,
            count: int,
            max_age: relativedelta,
    ) -> None:
        self.table = table
        self.size = size
        self.count = count
        self.max_age = max_age

    def to_add(self) -> Generator[LogDatePartition, None, None]:
        log_date = self.size.start(self.get_start_date())
        for _ in range(self.count):
            yield LogDatePartition(
                self.table,
                log_date=log_date
            )
            log_date += self.size.as_delta()

    def to_drop(self) -> Generator[LogDatePartition, None, None]:
        log_date = self.size.start(self.get_start_date() - self.max_age)
        while True:
            yield LogDatePartition(
                self.table,
                log_date=log_date
            )
            log_date -= self.size.as_delta()

    def get_start_date(self) -> date:
        return date.today() - self.date_shift


__all__ = ("RangePartitioningStrategy",)
