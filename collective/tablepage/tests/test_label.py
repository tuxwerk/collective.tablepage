# -*- coding: utf-8 -*-

import unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

from collective.tablepage.interfaces import IDataStorage
from collective.tablepage.testing import TABLE_PAGE_INTEGRATION_TESTING

class LabelTestCase(unittest.TestCase):

    layer = TABLE_PAGE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='TablePage', id='table_page', title="The Table Document")
        tp = portal.table_page
        tp.edit(pageColumns=[{'id': 'col_a', 'label': 'Col A', 'description': 'Th\xc3\xacs data is futile',
                              'type': 'String', 'vocabulary': '', 'options': []}])
        storage = IDataStorage(tp)
        storage.add({'__creator__': 'user1', 'col_a': 'F\xc3\xb2\xc3\xb2 data from user1',
                     '__uuid__': 'aaa'})
        storage.add({'__label__': 'A label'})
        storage.add({'__creator__': 'user1', 'col_a': 'Other data from user1',
                     '__uuid__': 'bbb'})
        storage.add({'__creator__': 'user1', 'col_a': 'Again data from user1',
                     '__uuid__': 'ccc'})
        self.storage = storage

    def test_view_pages_with_labels(self):
        # Basic test: all views, when labels are used, are working?
        request = self.layer['request']
        portal = self.layer['portal']
        tp = portal.table_page
        try:
            tp()
        except Exception:
            self.fail("Table view raised an unexpected error!")
        view = getMultiAdapter((tp, request), name=u'multiple-tables-view')
        try:
            view()
        except Exception:
            self.fail("Multiple tables view raised an unexpected error!")
        view = getMultiAdapter((tp, request), name=u'tablepage-edit')
        try:
            view()
        except Exception:
            self.fail("Edit view raised an unexpected error!")

    def test_create_new_label_form(self):
        request = self.layer['request']
        portal = self.layer['portal']
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        self.assertTrue('New label' in view())

    def test_create_new_notlast_label_form(self):
        request = self.layer['request']
        portal = self.layer['portal']
        form = request.form
        form['row-index'] = 1
        form['addLabel'] = '1'
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        self.assertTrue('New label' in view())

    def test_edit_label_form(self):
        request = self.layer['request']
        portal = self.layer['portal']
        form = request.form
        form['row-index'] = 1
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        self.assertTrue('Edit label' in view())

    def test_create_new_label(self):
        request = self.layer['request']
        portal = self.layer['portal']
        form = request.form
        form['label'] = 'foo'
        form['form.submitted'] = '1'
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        view()
        self.assertEqual(len(self.storage), 5)
        self.assertEqual(self.storage[-1].get('__label__'), 'foo')

    def test_create_new_notlast_label(self):
        request = self.layer['request']
        portal = self.layer['portal']
        form = request.form
        form['label'] = 'bar'
        form['row-index'] = 3
        form['addLabel'] = '1'
        form['form.submitted'] = '1'
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        view()
        self.assertEqual(len(self.storage), 5)
        self.assertEqual(self.storage[3].get('__label__'), 'bar')

    def test_edit_label(self):
        request = self.layer['request']
        portal = self.layer['portal']
        form = request.form
        form['label'] = 'bar'
        form['row-index'] = 1
        form['form.submitted'] = '1'
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name=u'edit-label')
        view()
        self.assertEqual(len(self.storage), 4)
        self.assertEqual(self.storage[1].get('__label__'), 'bar')
