from zope.i18nmessageid import MessageFactory
import pkg_resources


_ = MessageFactory('ftw.contacts')
IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'
