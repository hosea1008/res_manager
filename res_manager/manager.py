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
                "DATAID INTEGER, "
                "NAME NVARCHAR(200), "
                "TOPIC NVARCHAR(200), "
                "VERSION INTEGER ,"
                "DATATYPE VARCHAR(50), "
                "INFO NVARCHAR(1000), "
                "[SAVETIME] TIMESTAMP)")

            cursor.execute("CREATE TABLE DATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                           " DATAFIELD BLOB)")
            conn.commit()

    def _delete_by_id_nocommit(self, data_id, version, cursor):
        assert version in ['latest', 'first'] or isinstance(version, int), "version should be 'latest', 'first' or int version number"

        if not cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,)).fetchall():
            warnings.warn("Data %s not exists" % data_id)
            return
        else:
            if version == 'latest':
                curr_max_version = max(
                    [line[0] for line in
                     cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                uid = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                     (data_id, curr_max_version)).fetchone()[0]
            elif version == 'first':
                curr_max_version = min(
                    [line[0] for line in
                     cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                uid = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                     (data_id, curr_max_version)).fetchone()[0]
            else:
                uid_res = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                         (data_id, version)).fetchone()
                if uid_res is None:
                    warnings.warn("Version %s not exists for data %s" % (version, data_id))
                    return

                uid = uid_res[0]

            cursor.execute("DELETE FROM META_INFO WHERE ID=?", (uid,))
            cursor.execute("DELETE FROM DATA WHERE ID=?", (uid,))

    def save(self, data, name='', topic='', comment='', replace_version=None):
        """
        Save data
        :param replace_version: Version number or 'latest', 'first' if you want to replace. Pls note that
        the name and topic should be the same as the version to be replaced, otherwise it will save a new one
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

            data_ids = cursor.execute("SELECT DATAID FROM META_INFO").fetchall()
            curr_max_dataid = max([line[0] for line in data_ids]) if data_ids != [] else 0
            all_topic_names = set(cursor.execute("SELECT TOPIC, NAME, VERSION FROM META_INFO WHERE TOPIC=? AND NAME=?",
                                                 (topic, name,)).fetchall())

            # +------------+-----------+-----------------------+-------------------------------+
            # |            | 0 version | 1 version             | > 2 version                   |
            # +------------+-----------+-----------------------+-------------------------------+
            # | replace    | insert    | delete, insert        | delete, check version, insert |
            # +------------+-----------+-----------------------+-------------------------------+
            # | no replace | insert    | check version, insert | check version, insert         |
            # +------------+-----------+-----------------------+-------------------------------+

            if len(all_topic_names) > 1:  # multi versions of the same topic and name exist
                data_id = \
                    cursor.execute("SELECT DATAID FROM META_INFO WHERE TOPIC=? AND NAME=?", (topic, name)).fetchone()[0]

                if replace_version is not None:
                    self._delete_by_id_nocommit(data_id, version=replace_version, cursor=cursor)

                curr_max_version = max(
                    [line[0] for line in cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                cursor.execute(
                    "INSERT INTO META_INFO (DATAID, NAME, TOPIC, DATATYPE, VERSION, INFO, SAVETIME) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data_id, name, topic, data_type_str, curr_max_version + 1, comment, curr_time_str))

            elif len(all_topic_names) == 1 and replace_version:  # one version, need to replace
                data_id = \
                cursor.execute("SELECT DATAID FROM META_INFO WHERE TOPIC=? AND NAME=?", (topic, name)).fetchone()[0]
                self._delete_by_id_nocommit(data_id, version=replace_version, cursor=cursor)
                cursor.execute(
                    "INSERT INTO META_INFO (DATAID, NAME, TOPIC, DATATYPE, VERSION, INFO, SAVETIME) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data_id, name, topic, data_type_str, 1, comment, curr_time_str))

            elif len(all_topic_names) == 1 and replace_version is None:  # one version, don't need to replace
                data_id = \
                cursor.execute("SELECT DATAID FROM META_INFO WHERE TOPIC=? AND NAME=?", (topic, name)).fetchone()[0]
                curr_max_version = max(
                    [line[0] for line in cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                cursor.execute(
                    "INSERT INTO META_INFO (DATAID, NAME, TOPIC, DATATYPE, VERSION, INFO, SAVETIME) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data_id, name, topic, data_type_str, curr_max_version + 1, comment, curr_time_str))

            else:  # no version exists
                cursor.execute(
                    "INSERT INTO META_INFO (DATAID, NAME, TOPIC, DATATYPE, VERSION, INFO, SAVETIME) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (curr_max_dataid + 1, name, topic, data_type_str, 1, comment, curr_time_str))

            cursor.execute("INSERT INTO DATA (DATAFIELD) VALUES (?)", (sqlite3.Binary(pdata),))  # save data

            conn.commit()

    def delete_by_id(self, data_id, version='latest'):
        """
        Delete data by ID
        :param data_id: int, Data id, can be found by printing the meat info
        :param version: 'latest', 'first' or version number
        :return:
        """
        with self._ConnCursor(self.db_path) as [conn, cursor]:
            self._delete_by_id_nocommit(data_id, version, cursor)
            conn.commit()

    def update_meta(self, data_id, name=None, topic=None):
        """
        Update meta info by ID
        :param data_id: Data ID
        :param name: Data name
        :param topic: Data topic
        :return:
        """

        for string, field_name in zip([topic, name], ['topic', 'name']):
            assert string.find("''") < 0, "Illegal string \"''\" found in %s" % field_name

        with self._ConnCursor(self.db_path) as [conn, cursor]:
            for field_name, value in zip(["NAME", "TOPIC"], [name, topic]):
                if value is not None:
                    cursor.execute("UPDATE META_INFO SET %s=? WHERE DATAID=?" % field_name, (value, data_id,))
            conn.commit()

    # THE FOLLOWING FUNCTIONS EXIT WITHOUT COMMIT TO SQLITE (READ ONLY)

    def print_meta_info(self, topic=None):
        """
        Print all meta info of saved data
        :param topic: print only meta info for specific topic if given.
        :return:
        """
        table = PrettyTable()
        table.field_names = ["Data ID", "Name", "Topic", "Type", "Versions"]

        with self._ConnCursor(self.db_path) as [_, cursor]:
            if topic is not None:
                data_ids = set([line[0] for line in
                                cursor.execute("SELECT DATAID FROM META_INFO WHERE TOPIC=?", (topic,)).fetchall()])
                if data_ids == set():
                    warnings.warn("Topic \"%s\" not exists" % topic)
                    return
            else:
                data_ids = set([line[0] for line in cursor.execute("SELECT DATAID FROM META_INFO").fetchall()])

            for data_id in data_ids:
                meta_infos = cursor.execute("SELECT DATAID, NAME, TOPIC, DATATYPE FROM META_INFO WHERE DATAID=?",
                                            (data_id,)).fetchall()
                version_counts = len(meta_infos)
                line = list(meta_infos[0]) + [version_counts]
                table.add_row(line)

        print(table)

    def print_data_info(self, data_id):
        """
        Print data info of requested data
        :return:
        """
        table = PrettyTable()
        table.field_names = ["Data ID", "Name", "Topic", "Type", "Version", "Comment"]

        with self._ConnCursor(self.db_path) as [_, cursor]:
            meta_infos = cursor.execute(
                "SELECT DATAID, NAME, TOPIC, DATATYPE, VERSION, INFO FROM META_INFO WHERE DATAID=?",
                (data_id,)).fetchall()
            for line in meta_infos:
                table.add_row(line)

        print(table)

    def print_names(self):
        """
        Print all data names
        :return:
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            lines = set(cursor.execute("SELECT DATAID, NAME FROM META_INFO").fetchall())
            for line in lines:
                print("Data ID: %d\t\tName: %s" % (line[0], line[1]))

    def print_comments(self):
        """
        Print all comments
        :return:
        """
        with self._ConnCursor(self.db_path) as [_, cursor]:
            lines = set(cursor.execute("SELECT DATAID, VERSION, INFO FROM META_INFO").fetchall())
            for line in lines:
                print("Data ID: %d\tVersion: %d\tComment: %s" % (line[0], line[1], line[2]))

    def load(self, data_id, version='latest'):
        """
        Load data by ID
        :param version: 'latest', 'first' or version number
        :param data_id: int, Data id, can be found by printing the meta info.
        :return: Saved data
        """
        with self._ConnCursor(self.db_path) as [conn, cursor]:
            if not cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,)).fetchall():
                warnings.warn("Data %s not exists" % data_id)
                return
            else:
                if version == 'latest':
                    curr_max_version = max(
                        [line[0] for line in
                         cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                    uid = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                         (data_id, curr_max_version)).fetchone()[0]
                elif version == 'first':
                    curr_max_version = min(
                        [line[0] for line in
                         cursor.execute("SELECT VERSION FROM META_INFO WHERE DATAID=?", (data_id,))])
                    uid = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                         (data_id, curr_max_version)).fetchone()[0]
                else:
                    uid_res = cursor.execute("SELECT ID FROM META_INFO WHERE DATAID=? AND VERSION=?",
                                             (data_id, version)).fetchone()
                    if uid_res is None:
                        warnings.warn("Version %s not exists for data %s" % (version, data_id))
                        return

                    uid = uid_res[0]

            data = pickle.loads(cursor.execute("SELECT DATAFIELD FROM DATA WHERE ID=?", (uid,)).fetchone()[0])
        return data
