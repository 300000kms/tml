# -*- coding: utf-8 -*-

import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def createTable(db, table, cols, p=''):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print p, cols
    columns = ', '.join([str(p+co) for co in cols])
    sql = '''create table if not exists %s(%s)''' %(table, columns)
    sql = sql.lower()
    c.execute(sql)
    conn.commit()

    return

def getFields(rows):
    fields = set([])
    for r in rows:
        #print r
        for k in r.keys():
            fields.add(k)
    result = list(fields)
    result.sort()
    return result


def form(v):
    if type(v) is list:
        return str(v)
    else:
        return v

def dict2sqlite(db, table, rows, p=''):
    fields = getFields(rows)
    createTable(db, table, fields, p=p)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for r in rows:
        vals = r.values()
        fields = ', '.join( [str(p+rr) for rr in r.keys()] )
        values = ', '.join( ['?' for v in vals] )
        sql = 'insert into %s(%s) values (%s)' %(table,fields,values)
        try:
            c.execute(sql, tuple([form(v) for v in vals]) )
        except Exception as e:
            pass
            #print e
            #print sql
            #print tuple(vals)
            #print r
    conn.commit()
    return

if __name__ == "__main__":
    a =[
        {'pricing_quote__price__total__amount': 66, 'user__id': None,
         'pricing_quote__rate_with_service_fee__currency': u'EUR', 'listing__id': 19720843,
         'listing__person_capacity': 2, 'pricing_quote__rate__currency': u'EUR', 'user__is_superhost': None,
         'listing__lng': 2.1730616696154303, 'verified_card': False, 'listing__bathrooms': 1.0,
         'listing__is_rebookable': False, 'luxury_pdp': None, 'listing__guest_label': u'2 hu\xe9spedes',
         'pricing_quote__rate__amount': 59, 'listing__city': u'Barcelona', 'listing__is_new_listing': False,
         'listing__reviews_count': 5, 'listing__beds': 1, 'listing__lat': 41.40861118479532,
         'listing__is_superhost': False, 'pricing_quote__can_instant_book': False,
         'pricing_quote__rate_with_service_fee__amount': 66, 'verified_pdp': False,
         'pricing_quote__rate_type': u'nightly'},
        {'pricing_quote__price__total__amount': 47, 'user__id': None,
         'pricing_quote__rate_with_service_fee__currency': u'EUR', 'listing__id': 14408281,
         'listing__person_capacity': 1, 'pricing_quote__rate__currency': u'EUR', 'user__is_superhost': None,
         'listing__lng': 2.1517532503320393, 'verified_card': False, 'listing__bathrooms': 1.5,
         'listing__is_rebookable': False, 'luxury_pdp': None, 'listing__guest_label': u'1 hu\xe9sped',
         'pricing_quote__rate__amount': 41, 'listing__city': u'Barcelona', 'listing__is_new_listing': False,
         'listing__reviews_count': 9, 'listing__beds': 1, 'listing__lat': 41.40848965964156,
         'listing__is_superhost': False, 'pricing_quote__can_instant_book': False,
         'pricing_quote__rate_with_service_fee__amount': 47, 'verified_pdp': False,
         'pricing_quote__rate_type': u'nightly'},
        {'pricing_quote__price__total__amount': 113, 'user__id': None,
         'pricing_quote__rate_with_service_fee__currency': u'EUR', 'listing__id': 17409285,
         'listing__person_capacity': 4, 'pricing_quote__rate__currency': u'EUR', 'user__is_superhost': None,
         'listing__lng': 2.1816854829141232, 'verified_card': False, 'listing__bathrooms': 1.0,
         'listing__is_rebookable': False, 'luxury_pdp': None, 'listing__guest_label': u'4 hu\xe9spedes',
         'pricing_quote__rate__amount': 100, 'listing__city': u'Barcelona', 'listing__is_new_listing': False,
         'listing__reviews_count': 0, 'listing__beds': 1, 'listing__lat': 41.4100163954684,
         'listing__is_superhost': False, 'pricing_quote__can_instant_book': False,
         'pricing_quote__rate_with_service_fee__amount': 113, 'verified_pdp': False,
         'pricing_quote__rate_type': u'nightly'},
        {'pricing_quote__price__total__amount': 42, 'user__id': None,
         'pricing_quote__rate_with_service_fee__currency': u'EUR', 'listing__id': 14862340,
         'listing__person_capacity': 2, 'pricing_quote__rate__currency': u'EUR', 'user__is_superhost': None,
         'listing__lng': 2.2037196799827687, 'verified_card': False, 'listing__bathrooms': 1.0,
         'listing__is_rebookable': False, 'luxury_pdp': None, 'listing__guest_label': u'2 hu\xe9spedes',
         'pricing_quote__rate__amount': 37, 'listing__city': u'Santa Coloma de Gramenet',
         'listing__is_new_listing': False, 'listing__reviews_count': 7, 'listing__beds': 1,
         'listing__lat': 41.444852292911584, 'listing__is_superhost': False, 'pricing_quote__can_instant_book': False,
         'pricing_quote__rate_with_service_fee__amount': 42, 'verified_pdp': False,
         'pricing_quote__rate_type': u'nightly'}

    ]

    dict2sqlite('db.sqlite', 'tab', a, p='')
    print ''
