from __future__ import annotations
import typing as t

from piccolo.query.base import Query
from piccolo.querystring import QueryString

if t.TYPE_CHECKING:
    from piccolo.table import Table


class Create(Query):
    """
    Creates a database table.
    """

    __slots__ = ("if_not_exists",)

    def __init__(self, table: t.Type[Table], if_not_exists: bool = False):
        super().__init__(table)
        self.if_not_exists = if_not_exists

    @property
    def querystrings(self) -> t.Sequence[QueryString]:
        prefix = "CREATE TABLE"
        if self.if_not_exists:
            prefix += " IF NOT EXISTS"

        base = f"{prefix} {self.table._meta.tablename}"
        columns = ", ".join(["{}" for i in self.table._meta.columns])
        query = f"{base} ({columns})"
        return [
            QueryString(
                query, *[i.querystring for i in self.table._meta.columns]
            )
        ]
