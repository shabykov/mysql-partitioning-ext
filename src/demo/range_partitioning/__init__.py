from databases import Database  # type: ignore
from dateutil.relativedelta import relativedelta  # type: ignore

from mysql_partitioning_ext import (
    TimePartitionSize,
    PartitioningConfig,
    PartitioningManager,
)
from .schema import RangePartitioningSchemaEditor
from .strategy import RangePartitioningStrategy


def init_manager(db: Database):
    return PartitioningManager(
        configs=[
            PartitioningConfig(
                strategy=RangePartitioningStrategy(
                    table="tbl_city_features",       # table name
                    count=10,                        # number of partitions in days
                    size=TimePartitionSize(days=1),  # partition period size in days
                    max_age=relativedelta(days=3)    # partition live time in days
                )
            ),
            PartitioningConfig(
                strategy=RangePartitioningStrategy(
                    table="tbl_rider_features",      # table name
                    count=10,                        # number of partitions in days
                    size=TimePartitionSize(days=1),  # partition period size in days
                    max_age=relativedelta(days=3)    # partition live time in days
                )
            ),
            PartitioningConfig(
                strategy=RangePartitioningStrategy(
                    table="tbl_driver_features",     # table name
                    count=10,                        # number of partitions in days
                    size=TimePartitionSize(days=1),  # partition period size in days
                    max_age=relativedelta(days=3)    # partition live time in days
                )
            )
        ],
        schema_editor=RangePartitioningSchemaEditor(db)
    )


__all__ = ("init_manager",)

