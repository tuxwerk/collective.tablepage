# -*- coding: utf-8 -*-

import unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

from collective.tablepage.interfaces import IDataStorage
from collective.tablepage.testing import TABLE_PAGE_INTEGRATION_TESTING


class HtmlFieldTestCase(unittest.TestCase):
    
    layer = TABLE_PAGE_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.invokeFactory(type_name='TablePage', id='table_page', title="The Table Document")
        tp = portal.table_page
        tp.edit(pageColumns=[{'id': 'the_html_data', 'label': 'A text', 'description': '',
                              'type': 'Html', 'vocabulary': '', 'options': []}
        ])
        self.storage = IDataStorage(tp)

    def test_access_creation_form(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        view = getMultiAdapter((tp, request), name='edit-record')
        self.assertIn('<textarea cols="80" rows="5" id="the_html_data" class="mce_editable"', view())

    def test_access_edit_form(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        self.storage.add({'__creator__': 'foo', 'the_html_data': 'foo data'})
        request.form['row-index'] = 0
        view = getMultiAdapter((tp, request), name='edit-record')
        self.assertIn('name="the_html_data">foo data</textarea>', view())

    def test_save(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        request.form['form.submitted'] = '1'
        request.form['the_html_data'] = '<b>Lorem</b> ipsum'
        view = getMultiAdapter((tp, request), name='edit-record')
        view()
        self.assertEqual(self.storage[0]['the_html_data'], '<b>Lorem</b> ipsum')

    def test_required(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        configuration = tp.getPageColumns()
        configuration[0]['options'] = ['required']
        tp.setPageColumns(configuration)
        request.form['form.submitted'] = '1'
        view = getMultiAdapter((tp, request), name='edit-record')
        view()
        self.assertIn('The field "A text" is required', view())

    def test_unique(self):
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        configuration = tp.getPageColumns()
        configuration[0]['options'] = ['unique']
        tp.setPageColumns(configuration)
        self.storage.add({'__creator__': 'user1', 'the_html_data': 'foo bar baz'})
        request.form['form.submitted'] = '1'
        request.form['the_html_data'] = 'foo bar baz'
        view = getMultiAdapter((tp, request), name='edit-record')
        output = view()
        self.assertIn('The value "foo bar baz" is already present in the column "A text"', output)

    def test_unique_2(self):
        """Prevent regression: when saving an existing record ignore the record itself""" 
        portal = self.layer['portal']
        request = self.layer['request']
        tp = portal.table_page
        configuration = tp.getPageColumns()
        configuration[0]['options'] = ['unique']
        tp.setPageColumns(configuration)
        self.storage.add({'__creator__': 'user1', 'the_html_data': 'foo bar baz', '__uuid__': 'aaa-bbb'})
        request.form['form.submitted'] = '1'
        request.form['row-index'] = 0
        request.form['the_html_data'] = 'foo bar baz'
        view = getMultiAdapter((tp, request), name='edit-record')
        output = view() or ''
        self.assertNotIn('The value "foo bar baz" is already present in the column "A text"', output)
        self.assertEqual(len(self.storage), 1)
