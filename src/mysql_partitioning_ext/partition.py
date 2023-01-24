import enum
import typing as t
from abc import abstractmethod
from datetime import date

from dateutil.relativedelta import relativedelta  # type: ignore

from .error import PartitioningError
from .schema import SchemaEditor


class TimePartitionUnit(enum.Enum):
    YEARS = "years"
    MONTHS = "months"
    WEEKS = "weeks"
    DAYS = "days"


class TimePartitionSize:
    unit: TimePartitionUnit
    value: int

    def __init__(
            self,
            years: t.Optional[int] = None,
            months: t.Optional[int] = None,
            weeks: t.Optional[int] = None,
            days: t.Optional[int] = None,
    ) -> None:
        sizes = [years, months, weeks, days]

        if not any(sizes):
            raise PartitioningError("Partition cannot be 0 in size.")

        if len([size for size in sizes if size and size > 0]) > 1:
            raise PartitioningError(
                "Partition can only have on size unit."
            )

        if years:
            self.unit = TimePartitionUnit.YEARS
            self.value = years
        elif months:
            self.unit = TimePartitionUnit.MONTHS
            self.value = months
        elif weeks:
            self.unit = TimePartitionUnit.WEEKS
            self.value = weeks
        elif days:
            self.unit = TimePartitionUnit.DAYS
            self.value = days
        else:
            raise PartitioningError(
                "Unsupported time partitioning unit"
            )

    @t.final
    def as_delta(self) -> relativedelta:
        if self.unit == TimePartitionUnit.YEARS:
            return relativedelta(years=self.value)

        if self.unit == TimePartitionUnit.MONTHS:
            return relativedelta(months=self.value)

        if self.unit == TimePartitionUnit.WEEKS:
            return relativedelta(weeks=self.value)

        if self.unit == TimePartitionUnit.DAYS:
            return relativedelta(days=self.value)

        raise PartitioningError(
            "Unsupported time partitioning unit: %s" % self.unit
        )

    @t.final
    def start(self, day: date) -> date:
        if self.unit == TimePartitionUnit.YEARS:
            return self._ensure_datetime(day.replace(month=1, day=1))

        if self.unit == TimePartitionUnit.MONTHS:
            return self._ensure_datetime(day.replace(day=1))

        if self.unit == TimePartitionUnit.WEEKS:
            return self._ensure_datetime(day - relativedelta(days=day.weekday()))

        return self._ensure_datetime(day)

    @staticmethod
    def _ensure_datetime(day: date) -> date:
        return date(year=day.year, month=day.month, day=day.day)

    def __repr__(self) -> str:
        return "TimePartitionSize<%s, %s>" % (self.unit, self.value)


class Partition:
    """Base class for a table partition."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Generates/computes the name for this partition."""

    @abstractmethod
    async def exists(self, schema_editor: SchemaEditor) -> bool:
        """Checks this partition in the database."""

    @abstractmethod
    async def add(self, schema_editor: SchemaEditor) -> None:
        """Creates this partition in the database."""

    @abstractmethod
    async def truncate(self, schema_editor: SchemaEditor) -> None:
        """Truncate this partition from the database."""

    @abstractmethod
    async def drop(self, schema_editor: SchemaEditor) -> None:
        """Deletes this partition from the database."""


__all__ = (
    "Partition",
    "TimePartitionUnit",
    "TimePartitionSize",
)
