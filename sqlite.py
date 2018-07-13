# -*- coding: utf-8 -*-
import sqlite3
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def nmz(c):
    '''
    normaliza los campos del sqlite
    '''
    c = c.lower()
    c = c.replace(' ', '_')
    c = c.replace('-', '_')
    c = c.replace('@', '_')
    return c

def createTable(db, table, cols, p=''):
    try:
        cls = []
        for c in cols:
            cls.append(nmz(c))
        conn = sqlite3.connect(db)
        c = conn.cursor()
        cols =[ "'%s%s'" %(p,cl) for cl in cls ]
        cols.sort()
        columns = ', '.join(cols)
        sql = 'create table if not exists %s(%s)' %(table, columns)
        c.execute(sql)
        conn.commit()
    except Exception as e:
        if str(e) == 'unable to open database file':
            folder = ''
            if len(db.split('/'))>1 and os.path.isdir('/'.join(db.split('/')[0:-1]))==False:
                os.makedirs('/'.join(db.split('/')[0:-1]))
                return createTable(db, table, cols, p=p)
        print e
    return


def getFields(rows):
    fields = set([])
    for r in rows:
        for k in r.keys():
            fields.add(k)
    result = list(fields)
    result.sort()
    return result


def dict2sqlite(db, table, rows, p=''):
    fields = getFields(rows)
    createTable(db, table, fields, p=p)
    conn = sqlite3.connect(db)
    #conn.isolation_level = None
    c = conn.cursor()
    for r in rows:
        vals = r.values()
        fields = ', '.join(["'%s%s'" %(p,nmz(k)) for k in r.keys()])
        #fix type values
        for n,v in enumerate(vals):
            if type(v) is list:
                vals[n]=str(v)

        values = ', '.join(['?' for v in vals])
        sql = 'insert into %s(%s) values (%s)' %(table,fields,values)
        try:
            c.execute(sql, tuple(vals) )
        except Exception as e:
            if ' '.join(str(e).split(' ')[:6]) == 'table %s has no column named' %(table):
                print '>>>> do new column', e
                addColumns(db, table, [str(e).split(' ')[-1]])
                return dict2sqlite(db, table, rows)
            print '!!!!!!!!!!!!!!!!!!!!!!!!!'
            print sql
            print e
            print r
    conn.commit()
    return


def getRows(db, table, limit=None, fields=None, groupby=None):
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    c = conn.cursor()

    if fields == None:
        fields = ' * '
    else:
        fields = ", ".join(fields)

    sql = "select %s from  %s" %(fields, table)

    if groupby != None:
        sql+= ' group by %s' %(groupby)

    if limit is not None:
        sql += ' limit %s' %(limit)

    print sql
    c.execute(sql)
    return c.fetchall()


def getRow(db, table, id=1,fields=None):
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    c = conn.cursor()

    if fields == None:
        fields = '*'
    else:
        fields = ", ".join(fields)

    sql = "select %s from  %s" % (fields, table)
    sql += ' where ROWID = %s' %(id)

    c.execute(sql)

    return c.fetchone()


def addColumns(db, table, fields):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for f in fields:
        try:
            c.execute ('ALTER TABLE %s ADD COLUMN %s' %(table, f))
            conn.commit()
        except Exception as e:
            print e
    conn.close()
    return


#sqlite.update(db, table, {'lat':pos[0], 'lng': pos[1]}, {'ROWID':r})

def update(db, table, results, cond):
    '''
    :param db:
    :param table:
    :param results:
    :param cond:
    :return:

    isolation_level
    f you want autocommit mode, then set isolation_level to None.
    Otherwise leave it at its default, which will result in a plain “BEGIN” statement, or set it to one of SQLite’s supported isolation levels: “DEFERRED”, “IMMEDIATE” or “EXCLUSIVE”.
    '''

    conn = sqlite3.connect(db)
    c = conn.cursor()
    #conn.execute("PRAGMA read_uncommitted = true;");
    conn.isolation_level = None
    print ':::', conn.isolation_level

    for values in results:
        sql = 'update %s set ' %(table)
        for k in values:
            sql += " %s = '%s', " %(k, values[k])
        sql = sql.strip(', ')
        sql+= ' where '
        for cc in cond:
            sql += ' %s = %s, ' %(cc, cond[cc])
        sql = sql.strip(', ')
        print sql
        print '.'
        c.execute(sql)
    conn.commit()
    return


def getTables():
    return


def sql(db, sql):
    '''
    pragma table_info(booksfull)
    '''
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(sql)
    try :
        result = c.fetchall()
    except:
        result = None
    return result


if __name__ == "__main__":
    print