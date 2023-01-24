Here implementation of python-client of [mysql partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning-overview.html)

* `config` - configuration for partitioning a specific table according to the specified strategy.
* `manager` - creates a partitioning plan for one partitioning config.
* `partition` - base interface for table partition. 
* `plan` - describes the partitions that are going to be created/deleted for a particular partitioning config. A "partitioning config" applies to one model.
* `schema` - schema editor, DDL for partitioning purpose.
* `strategy` - base class for implementing a partitioning strategy for a partitioned table.