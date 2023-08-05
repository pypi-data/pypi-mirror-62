# coding: utf-8
#
# Copyright 2019 Geocom Informatik AG / VertiGIS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# noinspection PyUnresolvedReferences
"""
The **validate** module can be used to verify if certain values are "truthy".
Most of the functions in this module return a **boolean** (True/False).

Exceptions to this rule are the :func:`pass_if` and :func:`raise_if` functions, which can be used for data assertions
and therefore serve as an alternative to the ``assert`` statement (which should not be used in production environments).

    >>> def test(text):
    >>>     pass_if(isinstance(text, str), TypeError, 'test() requires text input')
    >>>     print(text)
    >>>
    >>> test('Hello World')
    'Hello World'
    >>>
    >>> test(123)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: test() requires text input
"""

import types as _types
from numbers import Number as _Number

import gpf.common.const as _const
import gpf.common.guids as _guids


def is_text(value, allow_empty=True):
    """
    Returns ``True`` if **value** is a string-like object.

    :param value:       The value to check.
    :param allow_empty: If ``True`` (default), empty string values are allowed.
                        If ``False``, empty strings will evaluate as "falsy".
    :type allow_empty:  bool
    :rtype:             bool
    """
    if isinstance(value, _types.StringTypes):
        return allow_empty or value != _const.CHAR_EMPTY
    return False


def is_number(value, allow_bool=False):
    """
    Returns ``True`` if *value* is a built-in numeric object (e.g. ``int``, ``float``, ``long``, ``Decimal``, etc.).

    Note that :func:`is_number` will return ``False`` for booleans by default, which is non-standard behaviour,
    because ``bool`` is a subclass of ``int``:

        >>> isinstance(True, int)
        True
        >>> is_number(True)
        False

    :param value:       The value to check.
    :param allow_bool:  If the standard Python boolean evaluation behavior is desired, set this to ``True``.
    :type allow_bool:   bool
    :rtype:             bool
    """
    if isinstance(value, bool):
        return allow_bool
    return isinstance(value, _Number)


def is_iterable(value):
    # noinspection PyUnresolvedReferences
    """
    Returns ``True`` if *value* is an iterable container (e.g. ``list`` or ``tuple`` but not a **generator**).

    Note that :func:`is_iterable` will return ``False`` for string-like objects as well, even though they are iterable.
    The same applies to **generators** and **sets**:

        >>> my_list = [1, 2, 3]
        >>> is_iterable(my_list)
        True
        >>> is_iterable(set(my_list))
        False
        >>> is_iterable(v for v in my_list)
        False
        >>> is_iterable(str(my_list))
        False

    :param value:   The value to check.
    :rtype:         bool
    """
    return hasattr(value, '__iter__') and hasattr(value, '__getitem__')


def is_guid(value):
    """
    Returns ``True`` when the given *value* is a GUID-like object and ``False`` otherwise.
    The function effectively tries to parse the value as a :class:`gpf.tools.guids.Guid` object.

    :param value:   A string or a GUID-like object.
    :rtype:         bool
    """
    try:
        _guids.Guid(value)
    except (_guids.Guid.BadGuidError, _guids.Guid.MissingGuidError):
        return False
    return True


def has_value(obj, strip=False):
    """
    Returns ``True`` when *obj* is "truthy".

    Note that :func:`has_value` will return ``True`` for the ``False`` boolean and ``0`` integer values.
    Python normally evaluates these values as "falsy", but for databases for example, these values are perfectly valid.
    This is why :func:`has_value` considers them to be "truthy":

        >>> my_int = 0
        >>> my_bool = False
        >>> if not (my_int and my_bool):
        >>>     print('Both values are "falsy".')
        'Both values are "falsy".'
        >>> has_value(my_int)
        True
        >>> has_value(my_bool)
        True

    Other usage examples:

        >>> has_value(None)
        False
        >>> has_value({})
        False
        >>> has_value('test')
        True
        >>> has_value('   ', strip=True)
        False

    :param obj:     The object for which to evaluate its value.
    :param strip:   If ``True`` and *obj* is a ``str``, *obj* will be stripped before evaluation. Defaults to ``False``.
    :type strip:    bool
    :rtype:         bool
    """
    if not obj:
        return obj == 0
    if is_text(obj):
        return (obj.strip() if strip else obj) != _const.CHAR_EMPTY
    return True


def signature_matches(func, template_func):
    """
    Checks if the given *func* is of type `function` or `instancemethod`.
    If it is, it also verifies if the argument count matches the one from the given *template_func*.
    When the function is not callable or the signature does not match, ``False`` is returned.

    :param func:            A callable function or instance method.
    :param template_func:   A template function to which the callable function argument count should be compared.
    :rtype:                 bool
    """

    def _get_argcount(f):
        """ Returns the argument count for a function (offset by 1 if the function is an instance method). """
        offset = 0
        if hasattr(f, 'im_func'):
            # Function is an instance method (with a 'self' argument): offset argument count by 1
            f = f.im_func
            offset = 1
        if not hasattr(f, 'func_code'):
            return None
        return f.func_code.co_argcount - offset

    f_args = _get_argcount(func)
    t_args = _get_argcount(template_func)

    if f_args is None or t_args is None:
        # One or both functions are not of type `function` or `instancemethod`
        return False

    return f_args == t_args


def pass_if(expression, exc_type, exc_val=_const.CHAR_EMPTY):
    """
    Raises an error of type *err_type* when *expression* is **falsy** and silently passes otherwise.
    Opposite of :func:`raise_if`.

    :param expression:  An expression or value to evaluate.
    :param exc_type:    The error to raise when *expression* evaluates to ``False``, e.g. ``AttributeError``.
    :param exc_val:     An optional message or exception value to include with the error (recommended).
    :rtype:             bool
    :return:            Returns ``True`` if evaluation was successful.

    :Examples:

        >>> my_value = 0
        >>> pass_if(my_value)
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
        AssertionError
        >>> pass_if(my_value == 0)
        >>> pass_if(my_value == 1, ValueError, 'my_value should be 1')
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
        ValueError: my_value should be 1
    """
    if not expression:
        raise exc_type(exc_val)
    return True


def raise_if(expression, exc_type, exc_val=_const.CHAR_EMPTY):
    """
    Raises an error of type *err_type* when *expression* is **truthy** and silently passes otherwise.
    Opposite of :func:`pass_if`.

    :param expression:  An expression or value to evaluate.
    :param exc_type:    The error to raise when *expression* evaluates to ``True``, e.g. ``AttributeError``.
    :param exc_val:     An optional message or exception value to include with the error (recommended).
    :rtype:             bool
    :return:            Returns ``True`` if evaluation was unsuccessful.

    :Examples:

        >>> my_value = 0
        >>> raise_if(my_value)
        >>> raise_if(my_value == 1)
        >>> raise_if(my_value == 0, ValueError, 'my_value should not be 0')
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
        ValueError: my_value should not be 0
    """
    if expression:
        raise exc_type(exc_val)
    return True
