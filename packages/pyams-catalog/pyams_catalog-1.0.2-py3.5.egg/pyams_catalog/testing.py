#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_catalog.testing module

Package testing utilities.
"""

import sys

from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import Interface, implementer
from zope.schema import TextLine
from zope.schema.fieldproperty import FieldProperty

from pyams_i18n.schema import I18nTextLineField

__docformat__ = 'restructuredtext'


if sys.argv[-1].endswith('/bin/test'):

    class IContentInterface(Interface):
        """Content interface"""
        value = TextLine(title="Value property")

    @implementer(IContentInterface)
    class MyContent(Persistent, Contained):
        """Content persistent class"""
        value = FieldProperty(IContentInterface['value'])

    class MyOtherContent(Persistent, Contained):
        """Other content class"""
        value = 'Other content value'

    class II18nContentInterface(Interface):
        """I18n content interface"""
        i18n_value = I18nTextLineField(title="I18n value property")

    @implementer(II18nContentInterface)
    class I18nContent(Persistent, Contained):
        """I18n content class"""
        i18n_value = FieldProperty(II18nContentInterface['i18n_value'])
