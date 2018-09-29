import sqlite3
from src.stores.sqlite.sqlitetable import SqliteTable


class TableTest(SqliteTable):

    def __init__(self, conn):
        self._name = 'tablename'
        self._fields = {'fieldname': {'type': 'bool', 'default': False}}
        super().__init__(conn)

    def add(self, value):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(value)

    def insert_object(self, value):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + str(value) + '")'
        self._conn.execute(sql)
        self._conn.commit()


class TableTestNew(SqliteTable):

    def __init__(self, conn):
        self._name = 'tablename'
        self._fields = {'fieldname': {'type': 'bool', 'default': False},
                        'newfield': {'type': 'str', 'default': ''},
                        'newfield2': {'type': 'bool', 'default': False}
                        }
        super().__init__(conn)

    def add(self, value, value2):
        if not self.is_table_exist():
            self.create_table()
        self.insert_object(value, value2)

    def insert_object(self, value, value2, value3):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + str(value) + '", '
        sql += '"' + str(value2) + '", '
        sql += '"' + str(value3) + '")'
        self._conn.execute(sql)
        self._conn.commit()


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
    assert fields['fieldname']['type'] == 'bool'


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


def test_sqlite_table_schema():
    table = TableTest(_create_conn())
    assert table
    schema = table._get_schema()
    assert schema['fieldname']
    assert 'type' in schema['fieldname']
    assert schema['fieldname']['type'] == 'bool'
    assert len(schema.keys()) == 1


def test_sqlite_table_update_schema():
    conn = _create_conn()
    table = TableTest(conn)
    assert table
    assert table.is_table_exist()
    fields = table._fields
    assert fields['fieldname']
    table.add(True)
    tablenew = TableTestNew(conn)
    assert tablenew
    assert tablenew.is_table_exist()
    fieldsnew = tablenew._fields
    assert fieldsnew['fieldname']
    assert fieldsnew['newfield']
    assert fieldsnew['newfield2']
    data = tablenew._get_alls()
    assert data
    assert len(data) == 1
    assert data[0]['fieldname']
    assert data[0]['newfield'] == ''
    assert not data[0]['newfield2']
