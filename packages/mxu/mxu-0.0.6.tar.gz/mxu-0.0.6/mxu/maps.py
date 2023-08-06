# -*- coding:utf-8 -*-
#
# Copyright (C) 2020, Maximilian Köhl <mkoehl@cs.uni-saarland.de>

from __future__ import annotations

import typing as t


KeyT = t.TypeVar("KeyT")
ValueT = t.TypeVar("ValueT")


class _IdentityKey(t.Generic[KeyT]):
    __slots__ = ["wrapped"]

    wrapped: KeyT

    def __init__(self, wrapped: KeyT) -> None:
        self.wrapped = wrapped

    def __hash__(self) -> int:
        return object.__hash__(self.wrapped)

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, _IdentityKey):
            return self.wrapped is other.wrapped
        return False


class IdentityMap(t.MutableMapping[KeyT, ValueT], t.Generic[KeyT, ValueT]):
    _dict: t.Dict[_IdentityKey[KeyT], ValueT]

    def __init__(
        self,
        base: t.Optional[t.Mapping[KeyT, ValueT]] = None,
        *,
        _dict: t.Optional[t.Dict[_IdentityKey[KeyT], ValueT]] = None,
    ) -> None:
        if base is not None:
            assert _dict is None, "`_dict` must be None if `base` is given"
            self._dict = {_IdentityKey(key): value for key, value in base.items()}
        elif _dict is not None:
            self._dict = _dict
        else:
            self._dict = {}
        self._hash = None

    def __getitem__(self, key: KeyT) -> ValueT:
        return self._dict[_IdentityKey(key)]

    def __setitem__(self, key: KeyT, value: ValueT) -> None:
        self._dict[_IdentityKey(key)] = value

    def __delitem__(self, key: KeyT) -> None:
        del self._dict[_IdentityKey(key)]

    def __iter__(self) -> t.Iterator[KeyT]:
        return (key.wrapped for key in self._dict.keys())

    def __len__(self) -> int:
        return len(self._dict)

    def __repr__(self) -> str:
        return f"<IdentityMap {self._dict!r}>"


class FrozenMap(t.Hashable, t.Mapping[KeyT, ValueT]):
    _dict: t.Dict[KeyT, ValueT]
    _hash: t.Optional[int]

    @classmethod
    def transfer_ownership(cls, dict: t.Dict[KeyT, ValueT]) -> FrozenMap[KeyT, ValueT]:
        """ You should no longer modify `dict`. """
        return cls(_dict=dict)

    def __init__(
        self,
        base: t.Optional[t.Mapping[KeyT, ValueT]] = None,
        *,
        _dict: t.Optional[t.Dict[KeyT, ValueT]] = None,
    ) -> None:
        if base is not None:
            assert _dict is None, "`_dict` must be None if `base` is given"
            self._dict = dict(base)
        elif _dict is not None:
            self._dict = _dict
        else:
            self._dict = {}
        self._hash = None

    def __getitem__(self, key: KeyT) -> ValueT:
        return self._dict[key]

    def __iter__(self) -> t.Iterator[KeyT]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __repr__(self) -> str:
        return f"<FrozenMap {self._dict!r}>"

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash((FrozenMap, tuple(self._dict.items())))
        return self._hash

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, FrozenMap):
            return NotImplemented
        return tuple(self._dict.items()) == tuple(other._dict.items())

    def setitem(self, key: KeyT, value: ValueT) -> FrozenMap[KeyT, ValueT]:
        return self.__class__(_dict={**self._dict, key: value})

    def delitem(self, key: KeyT) -> FrozenMap[KeyT, ValueT]:
        _dict = dict(self._dict)
        del _dict[key]
        return FrozenMap(_dict=_dict)

    def copy(self) -> FrozenMap[KeyT, ValueT]:
        return self
