from __future__ import unicode_literals
import frappe

def execute():
    """
    This patch updates the collections import to use collections.abc
    """
    try:
        from collections.abc import Mapping, MutableMapping
    except ImportError:
        from collections import Mapping, MutableMapping