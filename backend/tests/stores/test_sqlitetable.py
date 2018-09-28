import sqlite3
from src.stores.sqlite.sqlitetable import SqliteTable

class TableTest(SqliteTable):

    def __init__(self, conn):
        self._name = 'tablename'
        self._fields = {'fieldname': {'type': 'BOOLEAN'}}
        super().__init__(conn)


class TableTestNew(SqliteTable):

    def __init__(self, conn):
        self._name = 'tablename'
        self._fields = {'fieldname': {'type': 'BOOLEAN'},
                        'newfield': {'type': 'BOOLEAN'}}
        super().__init__(conn)

def _create_conn():
    return sqlite3.connect(':memory:')

def test_sqlite_table_init():
    table = TableTest(_create_conn())
    assert table
    assert table.is_table_exist()

def test_sqlite_table_clean():
    table = TableTest(_create_conn())
    assert table
    assert table.is_table_exist()
    table.clean()
    assert not table.is_table_exist()

def test_sqlite_table_fields():
    table = TableTest(_create_conn())
    assert table
    assert table.is_table_exist()
    fields = table._fields
    assert table
    assert len(fields) == 1
    assert fields['fieldname']
    assert fields['fieldname']['type'] == 'BOOLEAN'

def test_sqlite_table_getfields():
    table = TableTest(_create_conn())
    assert table
    assert table.is_table_exist()
    fields = table._get_fields()
    assert fields
    assert len(fields) == 1
    assert fields[0] == 'fieldname'
    dbfields = table._get_db_fields()
    assert dbfields
    assert len(dbfields) == 1
    assert dbfields[0] == 'fieldname'

def test_sqlite_table_update_schema():
    conn = _create_conn()
    table = TableTest(conn)
    assert table
    assert table.is_table_exist()
    fields = table._fields
    assert fields['fieldname']
    tablenew = TableTestNew(conn)
    assert tablenew
    assert tablenew.is_table_exist()
    fieldsnew = tablenew._fields
    assert fieldsnew['fieldname']
    assert fieldsnew['newfield']