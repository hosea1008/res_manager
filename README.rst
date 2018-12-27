============================
Experimental Results Manager
============================

This project helps you to handle your experimental results efficiently when doing your research. Basically it uses ``pickle`` to save and load the data, now we provide you with some high-level interfaces so that you can get rid of pickle dumping and loading from disk all the time. Also, with a given ``topic`` parameter when saving data, it can automatically build different directories for different topic.


Usage
=====

Just start with ``from res_manager import ResultManager``, now you can create an object with ``rm = ResultManager(path)`` and then use it to save, load, clear and preview your data.

Install ResultManager with ``pip install res-manager``

::

    >>> from res_manager import ResultManager
    >>> rm = ResultManager('data')
    >>> rm.save_data([1, 2, 3], topic='test saving', name='data1', commit_comment='Test saving a list')
    >>> rm.save_data(65535, topic='test saving', commit_comment='Test saving a number without a name')
    >>> rm.save_data(rm, topic='topic 2', commit_comment='Test saving an object')
    >>> rm.save_data({0:1,1:'string'}, name='dict_without_topic')
    >>> rm.print_meta_info()
    +----+-------------+----------------------------------+---------------------+-------------------------------------+----------------------------------------------------------------------------------------+
    | ID |    Topic    |               Name               |      Save time      |               Comment               |                                          Path                                          |
    +----+-------------+----------------------------------+---------------------+-------------------------------------+----------------------------------------------------------------------------------------+
    | 0  | test_saving |              data1               | 2018-12-27 15:28:27 |          Test saving a list         |                 data/test_saving/data1_2018-12-27_15:28:27.450445.list                 |
    | 1  | test_saving | 3c4d730d441ac5609eb65466b31e2d5d | 2018-12-27 15:29:04 | Test saving a number without a name |    data/test_saving/3c4d730d441ac5609eb65466b31e2d5d_2018-12-27_15:29:04.386450.int    |
    | 2  |   topic_2   | e1ee543cabb7f375a70eaee11ee7b8bd | 2018-12-27 15:29:38 |        Test saving an object        | data/topic_2/e1ee543cabb7f375a70eaee11ee7b8bd_2018-12-27_15:29:38.070020.ResultManager |
    | 3  | test_saving |              data1               | 2018-12-27 15:32:14 |          Test saving a list         |                 data/test_saving/data1_2018-12-27_15:32:14.123759.list                 |
    | 4  | test_saving | 3fe39c0c1805fbcd3f728d04caa90da3 | 2018-12-27 15:32:16 | Test saving a number without a name |    data/test_saving/3fe39c0c1805fbcd3f728d04caa90da3_2018-12-27_15:32:16.008795.int    |
    | 5  |   topic_2   | 849b1b87a744286a494fd2121cdb69f7 | 2018-12-27 15:32:20 |        Test saving an object        | data/topic_2/849b1b87a744286a494fd2121cdb69f7_2018-12-27_15:32:20.075466.ResultManager |
    | 6  |             |        dict_without_topic        | 2018-12-27 15:32:22 |                                     |                data/dict_without_topic_2018-12-27_15:32:22.643238.dict                 |
    +----+-------------+----------------------------------+---------------------+-------------------------------------+----------------------------------------------------------------------------------------+
    >>> rm.load_data_by_id(5)
    <res_manager.manager.ResultManager object at 0x7f29c8587470>
    >>> rm.load_data_by_name('data1')
    >>> /home/hsli/Workshop/res_manager/res_manager/manager.py:123: UserWarning: More than 1 instance of 'data1' found, returning the first one
    warnings.warn("More than 1 instance of '%s' found, returning the first one" % data_name)
    [1, 2, 3]
    >>> rm.load_data_by_name('dict_without_topic')
    {0: 1, 1: 'string'}

ResultManager
=============

This project mainly provides:

* A class named ``ResultManager`` that provides functions to save, load, clear and preview data.
* ``ResultManager.save_data``: Save your data
* ``ResultManager.load_data_by_name`` and ``ResultManager.load_data_by_id``: Loading data by name or ID
* ``ResultManager.print_meta_info`` Print all meta info of saved data, including name, path, topic, comments etc.

Future Plan
===========

* Adding support to save and load figures for each piece of data
* Adding version control to maintain different version data
* Adding support to automatically backup data to some cloud storage

Authors
=======

* Author and lead developer: `Hongshan Li`_

.. _`Hongshan Li`: https://www.hsli.top

Documentation
=============

This project is still simple, therefore no docs...

Requirements
------------

* ``prettytable>=0.7.2``

Note
----

``ResultManager`` is developed by Python 3.5 and only tested on Python 3.5 and Python 2.7