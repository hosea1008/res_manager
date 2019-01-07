from __future__ import print_function, unicode_literals
import pickle
import warnings
import os
import datetime
import hashlib
import sqlite3

from prettytable import PrettyTable


class ResultManager(object):
    def __init__(self, manager_path):
        """
        Create result manager
        :param manager_path: path to data directory
        """
        assert os.path.exists(manager_path), "Result manager path not exists"

        self.manager_path = manager_path

        self.db_path = "%s/data.db" % self.manager_path

        if not os.path.exists("%s/data.db" % self.manager_path):
            print("No previous database found, creating a new one...")
            self._create_table()

    def _create_table(self):
        conn, cursor = self._get_conn_cursor()
        cursor.execute(
            "CREATE TABLE META_INFO(ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME NVARCHAR(200), TOPIC NVARCHAR(200), DATATYPE VARCHAR(50), INFO NVARCHAR(1000), [SAVETIME] TIMESTAMP)")
        cursor.execute("CREATE TABLE DATA(ID INTEGER PRIMARY KEY AUTOINCREMENT, DATAFIELD BLOB)")
        self._commit_release(conn, cursor)

    def _get_conn_cursor(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        return conn, cursor

    def _commit_release(self, conn, cursor):
        cursor.close()
        conn.commit()
        conn.close()

    def save_data(self, data, topic='', name='', commit_comment=''):
        """
        Save data
        :param data: data to be saved
        :param topic: topic of the current data, a higher level than name, helps you to manager data of different topic
        :param name: name of the data, can be empty
        :param commit_comment: comment of the saving data
        :return:
        """
        assert len(name + commit_comment) > 0, "Name and comment cannot be all None"

        save_time = datetime.datetime.now()
        curr_time_str = save_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        data_type_str = str(type(data)).split("'")[1].split('.')[-1]

        pdata = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        conn, cursor = self._get_conn_cursor()
        cursor.execute(
            "INSERT INTO META_INFO (NAME, TOPIC, DATATYPE, INFO, SAVETIME) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                name, topic, data_type_str, commit_comment, curr_time_str))
        cursor.execute("INSERT INTO DATA (DATAFIELD) VALUES (?)", (sqlite3.Binary(pdata),))
        self._commit_release(conn, cursor)

    def print_meta_info(self):
        """
        Print all meta info of saved data
        :return:
        """
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Topic", "Type", "Commit comments", "Save time"]

        conn, cursor = self._get_conn_cursor()
        meta_infos = cursor.execute("SELECT * FROM META_INFO").fetchall()
        cursor.close()
        conn.close()
        for line in meta_infos:
            table.add_row(line)
        print(table)

    def print_data_names(self):
        """
        Print all data names
        :return:
        """
        conn, cursor = self._get_conn_cursor()
        lines = cursor.execute("SELECT ID, NAME FROM META_INFO").fetchall()
        cursor.close()
        conn.close()
        for line in lines:
            print("ID: %d\t\tName: %s" % (line[0], line[1]))

    def print_data_comments(self):
        """
        Print all comments
        :return:
        """
        conn, cursor = self._get_conn_cursor()
        lines = cursor.execute("SELECT ID, INFO FROM META_INFO").fetchall()
        cursor.close()
        conn.close()
        for line in lines:
            print("ID: %d\t\tName: %s" % (line[0], line[1]))

    def load_data_by_name(self, data_name):
        """
        Load data by name, Assertion happens when given a wrong name, and if there are 2 data of the same name, a warning would appear.
        :param data_name: str, name of the saved data
        :return: Saved data
        """

        conn, cursor = self._get_conn_cursor()
        names = [line[0] for line in cursor.execute("SELECT NAME FROM META_INFO").fetchall()]
        assert data_name in names, "%s not found" % data_name

        ids = [line[0] for line in cursor.execute("SELECT id FROM meta_info WHERE name=?", (data_name,)).fetchall()]
        cursor.close()
        conn.close()

        if len(ids) > 1:
            data_list = []
            for id in ids:
                data_list.append(self.load_data_by_id(id))
            return tuple(data_list)
        return self.load_data_by_id(ids[0])

    def load_data_by_id(self, data_id):
        """
        Load data by ID
        :param data_id: int, Data id, can be found by printing the meta info.
        :return: Saved data
        """
        conn, cursor = self._get_conn_cursor()
        data = pickle.loads(cursor.execute("SELECT DATAFIELD FROM DATA WHERE ID=?", (data_id,)).fetchone()[0])
        return data

    def delete_data_by_id(self, data_id):
        conn, cursor = self._get_conn_cursor()
        cursor.execute("DELETE FROM META_INFO WHERE ID=?", (data_id,))
        cursor.execute("DELETE FROM DATA WHERE ID=?", (data_id,))
        self._commit_release(conn, cursor)
