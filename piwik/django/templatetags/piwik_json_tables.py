# -*- coding: utf-8 -*-
from django.template import Node, Library
from django.conf import settings

register = Library()

def piwik_json_tables(data, metadata = None):
    """
    >>> settings.PIWIK_URL = 'http://example.com/'
    >>> piwik_json_tables({}, [{'metrics': {}}])
    {'table': [], 'metadata': []}
    >>> piwik_json_tables([], [{'metrics': {}}])
    {'table': [], 'metadata': []}
    >>> piwik_json_tables({'label': 12}, [{'metrics': {}}])
    {'table': [[('t', 12)]], 'metadata': ['label']}
    >>> piwik_json_tables({'label': 12}, [{'metrics': {'label': 'Label'}}])
    {'table': [[('t', 12)]], 'metadata': ['Label']}
    >>> piwik_json_tables([{'label': 12}], [{'metrics': {'label': 'Label'}}])
    {'table': [[('t', 12)]], 'metadata': ['Label']}
    >>> piwik_json_tables([{'uniq': 42, 'label': 12}], [{'metrics': {}}])
    {'table': [[('t', 12), ('t', 42)]], 'metadata': ['label', 'uniq']}
    >>> piwik_json_tables([{'logoHeight': 42, 'logoWidth': 12}], [{'metrics': {}}])
    {'table': [], 'metadata': []}
    >>> piwik_json_tables({'logo': 'pouet.gif'}, [{'metrics': {}}])
    {'table': [[('logo', 'http://example.com/pouet.gif')]], 'metadata': ['logo']}
    """
    th = []
    table = data
    if hasattr(data, 'keys'):
        table = [data]
    keys = []
    if len(table) > 0:
        keys = table[0].keys()
    keys.sort()
    try:
        keys.remove('label') # label in first
        keys.insert(0, 'label')
    except ValueError:
        pass
    try:
        keys.remove('logoHeight')
    except ValueError:
        pass
    try:
        keys.remove('logoWidth')
    except ValueError:
        pass
    for t in keys:
        try:
            th.append(metadata[0]['metrics'][t])
        except KeyError:
            th.append(t)
    rows = []
    site = settings.PIWIK_URL
    for r in table:
        row = []
        for key in keys:
            if key == 'logo':
                row.append(('logo', site + r[key]))
            else:
                row.append(('t', r[key]))
        if len(row) > 0:
            rows.append(row)
    return {'table'     : rows,
            'metadata' : th}

register.inclusion_tag('admin/piwik/table.html')(piwik_json_tables)
