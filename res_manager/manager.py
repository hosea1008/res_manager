from __future__ import print_function, unicode_literals

import datetime
import os
import pickle
import sqlite3
import warnings

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

    class _ConnCursor:
        def __init__(self, db_path):
            self.db_path = db_path

        def __enter__(self):
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.cursor.close()
            self.conn.close()

    def _create_table(self):
        with self._ConnCursor(self.db_path) as [conn, cursor]:
            cursor.execute(
                "CREATE TABLE META_INFO(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                                        "NAME NVARCHAR(200), "
                                        "TOPIC NVARCHAR(200), "
                                        "DATATYPE VARCHAR(50), "
                                        "INFO NVARCHAR(1000), "
                                        "[SAVETIME] TIMESTAMP)")

            cursor.execute("CREATE TABLE DATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                            " DATAFIELD BLOB)")
            conn.commit()

    def save(self, data, topic='', name='', comment=''):
        """
        Save data
        :param data: data to be saved
        :param topic: topic of the current data, a higher level than name, helps you to manager data of different topic
        :param name: name of the data, can be empty
        :param comment: comment of the saving data
        :return:
        """
        for string, field_name in zip([topic, name, comment], ['topic', 'name', 'comment']):
            assert string.find("''") < 0, "Illegal string \"''\" found in %s" % field_name

        save_time = datetime.datetime.now()
        curr_time_str = save_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        data_type_str = str(type(data)).split("'")[1].split('.')[-1]

        pdata = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        with self._ConnCursor(self.db_path) as [conn, cursor]:
            cursor.execute(
                "INSERT INTO META_INFO (NAME, TOPIC, DATATYPE, INFO, SAVETIME) VALUES (?, ?, ?, ?, ?)",
                (name, topic, data_type_str, comment, curr_time_str))

            cursor.execute("INSERT INTO DATA (DATAFIELD) VALUES (?)", (sqlite3.Binary(pdata),))

            conn.commit()

    def delete_by_id(self, data_id):
        """
        Delete data by ID
        :param data_id: int, Data id, can be found by printing the meat info
        :return:
        """
        with self._ConnCursor(self.db_path) as [conn, cursor]:
            cursor.execute("DELETE FROM META_INFO WHERE ID=?", (data_id,))
            cursor.execute("DELETE FROM DATA WHERE ID=?", (data_id,))
            conn.commit()

    def update_meta(self, id, name=None, topic=None, comment=None):
        """
        Update meta info by ID
        :param id: Data ID
        :param name: Data name
        :param topic: Data topic
        :param comment: Data comment
        :return:
        """

        for string, field_name in zip([topic, name, comment], ['topic', 'name', 'comment']):
            assert string.find("''") < 0, "Illegal string \"''\" found in %s" % field_name

        with self._ConnCursor(self.db_path) as [conn, cursor]:
            for field_name, value in zip(["NAME", "TOPIC", "INFO"], [name, topic, comment]):
                if value is not None:
                    cursor.execute("UPDATE META_INFO SET %s=? WHERE ID=?" % field_name, (value, id,))
            conn.commit()

    # THE FOLLOWING FUNCTIONS EXIT WITHOUT COMMIT TO SQLITE (READ ONLY)

    def print_meta_info(self):
        """
        Print all meta info of saved data
        :return:
        """
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Topic", "Type", "Commit comments", "Save time"]

        with self._ConnCursor(self.db_path) as [_, cursor]:
            meta_infos = cursor.execute("SELECT * FROM META_INFO").fetchall()
            for line in meta_infos:
                table.add_row(line)
            print(table)

    def print_names(self):
        """
        Print all data names
        :return:
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            lines = cursor.execute("SELECT ID, NAME FROM META_INFO").fetchall()
            for line in lines:
                print("ID: %d\t\tName: %s" % (line[0], line[1]))

    def print_comments(self):
        """
        Print all comments
        :return:
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            lines = cursor.execute("SELECT ID, INFO FROM META_INFO").fetchall()
            for line in lines:
                print("ID: %d\t\tName: %s" % (line[0], line[1]))

    def _load_by_name(self, data_name):
        """
        Load data by name, Assertion happens when given a wrong name, and if there are 2 data of the same name, a warning would appear.
        :param data_name: str, name of the saved data
        :return: Saved data
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            names = [line[0] for line in cursor.execute("SELECT NAME FROM META_INFO").fetchall()]
            if data_name not in names:
                warnings.warn("Data %s not found" % data_name)
                return_data = None
            else:
                ids = [line[0] for line in
                       cursor.execute("SELECT id FROM meta_info WHERE name=?", (data_name,)).fetchall()]

                if len(ids) > 1:
                    data_list = []
                    for id in ids:
                        data_list.append(self._load_by_id(id))
                    return_data = tuple(data_list)
                    warnings.warn("Found more than one instance of \"%s\"" % data_name)
                else:
                    return_data = self._load_by_id(ids[0])
        return return_data

    def _load_by_id(self, data_id):
        """
        Load data by ID
        :param data_id: int, Data id, can be found by printing the meta info.
        :return: Saved data
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            ids = [line[0] for line in cursor.execute("SELECT id FROM meta_info").fetchall()]
            if data_id not in ids:
                warnings.warn("Data ID %d not found" % data_id)
                data = None
            else:
                data = pickle.loads(cursor.execute("SELECT DATAFIELD FROM DATA WHERE ID=?", (data_id,)).fetchone()[0])
        return data

    def load(self, id=None, name=None):
        """
        Load data by ID or Name, load by ID by default
        :param id: Data ID
        :param name: Data Name
        :return:
        """
        if id:
            return self._load_by_id(id)
        elif name:
            return self._load_by_name(name)
        else:
            warnings.warn("At least one of ID or Name should be provided")
            return None
