# -*- coding: utf-8 -*-

from zope.i18n import translate
from zope.interface import implements
try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getAdapters
from collective.tablepage import tablepageMessageFactory as _
from collective.tablepage.interfaces import IColumnField


class ColumnTypesVocabulary(object):
    """Vocabulary factory for column types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        request = context.REQUEST
        adapters = getAdapters((context, context.REQUEST), IColumnField)
        elements = [a[0] for a in adapters]
        elements.sort(cmp=lambda x,y: cmp(translate(_(x), context=request),
                                          translate(_(y), context=request)))
        terms = [SimpleTerm(value=e, token=e, title=_(e)) for e in elements]
        return SimpleVocabulary(terms)

columnTypesVocabularyFactory = ColumnTypesVocabulary()
