# -*- coding: utf-8 -*-
from logging import getLogger

import time

logger = getLogger(__name__)

METRICNAME = '_THEME_TRANSFORM_START_'


def metrics_entry(event):
    if event.name != 'plone.app.theming.transform':
        continue
    setattr(event.request, METRICNAME, time.time())


def metrics_exit(event):
    if event.name != 'plone.app.theming.transform':
        continue
    start = getattr(event.request, METRICNAME)
    delta = (time.time() - start) * 1000
    logger.info('transform took {0:4.1f}ms'.format(delta))
