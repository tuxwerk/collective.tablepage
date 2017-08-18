# -*- coding: utf-8 -*-

from collective.tablepage.browser.table import TableViewView


class MultipleTablesView(TableViewView):
    """View with multiple tables"""

    def __call__(self):
        return self.index()

    def is_label(self, row):
        if row == 0:
            # Where does the 0 come from???
            return None
        if '__label__' in row.keys():
            return row['__label__']
        return None

    def getHeader(self, col_index):
        return self.headers()[col_index]
