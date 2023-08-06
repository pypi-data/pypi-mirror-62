import pandas as pd
from ipaddress import _BaseAddress, ip_address
from typing import Sequence

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType
from visions.utils.coercion import test_utils


def to_ip(series: pd.Series) -> pd.Series:
    return series.apply(ip_address)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_object, visions_string

    relations = [
        IdentityRelation(cls, visions_object),
        InferenceRelation(
            cls,
            visions_string,
            relationship=test_utils.coercion_test(to_ip),
            transformer=to_ip,
        ),
    ]
    return relations


class visions_ip(VisionsBaseType):
    """**IP Address** (v4 and v6) implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> from ipaddress import IPv4Address
        >>> x = pd.Series([IPv4Address('127.0.0.1'), IPv4Address('128.0.1.2')])
        >>> x in visions_ip
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, _BaseAddress) for x in series)
