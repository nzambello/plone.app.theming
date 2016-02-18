# -*- coding: utf-8 -*-
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getAvailableThemes
from plone.registry.interfaces import IRegistry
from xml.dom import minidom
from zope.component import getUtility


def importTheme(context):
    """Apply the theme with the id contained in the profile file theme.xml
    and enable the theme.
    """

    data = context.readDataFile('theme.xml')
    if not data:
        return

    logger = context.getLogger('plone.app.theming.exportimport')

    import ipdb; ipdb.set_trace()

    tree = minidom.parseString(data)
    themes = tree.getElementsByTagName('theme')
    all_themes = getAvailableThemes()
    for theme in themes:
        for node in theme.childNodes:

            value = node.firstChild.nodeValue.strip()

            if node.tagName == 'name':
                if value:
                    theme_info = None
                    for info in all_themes:
                        if info.__name__.lower() == value.lower():
                            theme_info = info
                            break

                    if theme_info is None:
                        raise ValueError(
                            "Theme {0:s} is not available".format(value))

                    applyTheme(theme_info)
                    logger.info('Theme {0:s} applied'.format(value))

            if node.tagName == 'enabled':
                settings = getUtility(IRegistry).forInterface(IThemeSettings, False)

                if value in ("y", "yes", "true", "t", "1", "on",):
                    settings.enabled = True
                    logger.info('Theme enabled')
                elif value in ("n", "no", "false", "f", "0", "off",):
                    settings.enabled = False
                    logger.info('Theme disabled')
                else:
                    raise ValueError(
                        "{0:s} is not a valid value for <enabled />".format(
                            value
                        )
                    )
