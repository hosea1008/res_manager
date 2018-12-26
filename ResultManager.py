from __future__ import print_function
import pickle
import warnings
import os
import datetime
import hashlib

from prettytable import PrettyTable


class MetaInfo(object):
    def __init__(self, manager_path):
        """
        This stores the meta info of the data manager
        :param manager_path: path to DataManager directory
        """
        self.data_path = manager_path

        self.topics = []
        self.names = []
        self.save_times = []
        self.comments = []
        self.paths = []


class ResultManager(object):
    def __init__(self, manager_path):
        """
        Create result manager
        :param manager_path: path to data directory
        """
        assert os.path.exists(manager_path), "Result manager path not exists"

        self.manager_path = manager_path
        self._load_meta_info()

    def _load_meta_info(self):
        if not os.path.exists("%s/meta_info.info" % self.manager_path):
            self._meta_info = MetaInfo(self.manager_path)
        else:
            with open("%s/meta_info.info" % self.manager_path, 'rb') as f:
                self._meta_info = pickle.load(f)

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
        curr_time_str = save_time.strftime("%Y-%m-%d_%H:%M:%S.%f")
        if name == '':
            name = hashlib.md5(''.join([curr_time_str, commit_comment]).encode('utf-8')).hexdigest()
        name_str = name.replace(' ', '_')
        data_type_str = str(type(data)).split("'")[1].split('.')[-1]

        save_full_path = "%s/%s_%s.%s" % (
            self.manager_path, name_str, curr_time_str, data_type_str)

        if topic != '':
            topic_str = topic.replace(' ', '_')
            if not os.path.exists("%s/%s" % (self.manager_path, topic_str)):
                os.mkdir("%s/%s" % (self.manager_path, topic_str))
            save_full_path = "%s/%s/%s_%s.%s" % (self.manager_path, topic_str, name.replace(' ', '_'), curr_time_str, data_type_str)

        with open(save_full_path, 'wb') as f:
            pickle.dump(data, f)

        self._meta_info.topics.append(topic_str)
        self._meta_info.names.append(name_str)
        self._meta_info.save_times.append(save_time)
        self._meta_info.comments.append(commit_comment)
        self._meta_info.paths.append(save_full_path)
        with open("%s/meta_info.info" % self.manager_path, 'wb') as f:
            pickle.dump(self._meta_info, f)

    def print_meta_info(self):
        """
        Print all meta info of saved data
        :return:
        """
        table = PrettyTable()
        table.add_column("ID", [i for i in range(len(self._meta_info.names))])
        table.add_column("Topic", self._meta_info.topics)
        table.add_column("Name", self._meta_info.names)
        table.add_column("Save time", [item.strftime("%Y-%m-%d %H:%M:%S") for item in self._meta_info.save_times])
        table.add_column("Comment", self._meta_info.comments)
        table.add_column("Path", self._meta_info.paths)

        print(table)

    def print_data_names(self):
        """
        Print all data names
        :return:
        """
        for idx, name in enumerate(self._meta_info.names):
            print("%s: %s" % (idx, name))

    def print_data_comments(self):
        """
        Print all comments
        :return:
        """
        for idx, comment in enumerate(self._meta_info.comments):
            print("%s: %s" % (idx, comment))

    def load_data_by_name(self, data_name):
        """
        Load data by name, Assertion happens when given a wrong name, and if there are 2 data of the same name, a warning would appear.
        :param data_name: str, name of the saved data
        :return: Saved data
        """
        assert data_name in self._meta_info.names, "%s not found" % data_name
        if self._meta_info.names.count(data_name) > 1:
            warnings.warn("More than 1 instance of '%s' found, returning the first one" % data_name)
        data_id = self._meta_info.names.index(data_name)
        return self.load_data_by_id(data_id)

    def load_data_by_id(self, data_id):
        """
        Load data by ID
        :param data_id: int, Data id, can be found by printing the meta info.
        :return: Saved data
        """
        data_path = self._meta_info.paths[data_id]
        with open(data_path, 'rb') as f:
            return pickle.load(f)

    def clear_data(self):
        """
        Clear all saved data and delete meta info.
        :return:
        """
        for path in self._meta_info.paths:
            os.remove(path)
        for topic in set(self._meta_info.topics):
            os.rmdir("%s/%s" % (self.manager_path, topic))
        if os.path.exists("%s/meta_info.info" % self.manager_path):
            os.remove("%s/meta_info.info" % self.manager_path)
        self._meta_info = MetaInfo(self.manager_path)


if __name__ == '__main__':
    dm = ResultManager('data')
    dm.clear_data()
    dm.save_data({0:1,2:9}, topic='topic1', name='test', commit_comment='saving')
    dm.save_data([1,2,3], topic='topic 2', name='test 2', commit_comment='saving tet')
    dm.save_data([1, 2, 3], topic='topic 2', name='test 2', commit_comment='saving tet')
    dm.save_data(dm, topic='topic 2', name='test 3', commit_comment='saving tet')
    dm.save_data(dm, topic='topic 2', name='', commit_comment='aa')
    dm.print_meta_info()
    # dm.print_data_names()
    # dm.print_data_comments()
    # print(dm.load_data_by_name('test_2'))
    # print(dm.load_data_by_id(1))
