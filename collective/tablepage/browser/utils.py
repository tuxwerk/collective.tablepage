from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

class TableRowStyles(object):

    @classmethod
    def get(cls, context):
        utility = queryUtility(ITinyMCE)
        if utility:
            translation_service = getToolByName(context, 'translation_service')
            return [[style.split('|')[1],
                     translation_service.utranslate(msgid=style.split('|')[0],
                                                    domain="plone.tinymce",
                                                    context=context)] \
                            for style in utility.tablerowstyles.splitlines()]
        return None
    
