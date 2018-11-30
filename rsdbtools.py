"""rsdbtools.py
Tools to access the run selection database.
Author: Stefan Nae
        <stefan@lip.pt>
"""

import psycopg2
from settings import RSDB

rsdb_write = ""
rsdb_write += 'host='+RSDB['HOST']
rsdb_write += ' port='+str(RSDB['PORT'])
rsdb_write += ' dbname='+RSDB['NAME']
rsdb_write += ' user='+RSDB['WRITE']['USER']
rsdb_write += ' password='+RSDB['WRITE']['PASS']

def upload_data(table,run,table_object):
    c = None

    try:
        print 'Connecting to rsdb ...'
        c = psycopg2.connect(rsdb_write)
        # print 'You are now connected.'
        cr = c.cursor()

        query = "INSERT INTO %s (run_number, data)" % table # python way
        query += " VALUES (%s, %s);" # sql way
        # print 'QUERY:', query

        data = (run, table_object)
        # print 'DATA:', data

        cr.execute(query, data)

        c.commit()

        return 0

    except psycopg2.OperationalError as e:
        print 'The connection could not be established!'
        print 'Error: ', e

        return 1

    except psycopg2.DatabaseError as e:
        if c:
            c.rollback()

        print 'Error %s' % e

        return 1

    except Exception as e:
        print 'The connection could not be established!'
        print 'Error:', e

        return 1

    finally:
        if c:
            c.close()
print 'The connection to rsdb is closed.'