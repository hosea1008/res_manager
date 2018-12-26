import pickle
import os
import time
import hashlib


class MetaInfo(object):
    def __init__(self, manager_path):
        """
        This stores the meta info of the data manager
        :param manager_path: path to DataManager directory
        """
        self.data_path = manager_path

        self.names = []
        self.save_times = []
        self.comments = []
        self.paths = []


class DataManager(object):
    def __init__(self, manager_path):
        """
        Create data manager
        :param manager_path: path to data directory
        """
        assert os.path.exists(manager_path), "Data manager path not exists"

        if not os.path.exists("%s/meta_info.info" % manager_path):
            self.meta_info = MetaInfo(manager_path)
        else:
            with open("%s/meta_info.info" % manager_path, 'rb') as f:
                self.meta_info = pickle.load(f)
        self.manager_path = manager_path

    def save_data(self, data, topic='', name='', commit_comment=''):
        save_time = time.localtime()
        curr_time_str = time.strftime("%Y-%m-%d_%H:%M:%S", save_time)
        if name == '':
            name = hashlib.md5(''.join([curr_time_str, commit_comment]).encode('utf-8')).hexdigest()
        data_type_str = str(type(data)).split("'")[1]
        save_full_path = "%s/%s_%s_%s.%s" % (
        self.manager_path, topic.replace(' ', '_'), name.replace(' ', '_'), curr_time_str, data_type_str)
        with open(save_full_path, 'wb') as f:
            pickle.dump(data, f)

        self.meta_info.names.append(name)
        self.meta_info.save_times.append(save_time)
        self.meta_info.comments.append(commit_comment)
        self.meta_info.paths.append(save_full_path)
        with open("%s/meta_info.info" % self.manager_path, 'wb') as f:
            pickle.dump(self.meta_info, f)

    def print_meta_info(self):
        for k, v in self.meta_info.__dict__.items():
            print("%s\t%s" % (k, v))

    def print_data_names(self):
        for name in self.meta_info.names:
            print(name)

    def load_data_by_name(self, data_name):
        data_id = self.meta_info.names.index(data_name)
        data_path = self.meta_info.paths[data_id]
        with open(data_path, 'rb') as f:
            return pickle.load(f)


if __name__ == '__main__':
    dm = DataManager('data')
    # dm.save_data([1, 2, 3,5], name='arreduce_uv', commit_comment='test saving')
    dm.print_meta_info()
    # dm.print_data_names()
    # print(dm.load_data_by_name('reduce_uv'))
