import pandas.api.types as pdt
import pandas as pd
from typing import Sequence

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_generic

    relations = [IdentityRelation(cls, visions_generic)]
    return relations


class visions_timedelta(VisionsBaseType):
    """**Timedelta** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.Timedelta(days=i) for i in range(3)])
        >>> x in visions_timedelta
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_timedelta64_dtype(series)
