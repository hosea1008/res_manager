============================
Experimental Results Manager
============================

This project helps you to handle your experimental results efficiently when doing your research. Basically it uses ``pickle`` and ``sqlite3`` to save, load and manage the data, now we provide you with some high-level interfaces so that you can get rid of pickle dumping and loading from disk all the time.

Since it is based on ``pickle``, in theory you can use it to manage all types of data in python, you can even save an object as shown in the following examples.

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
    ...
    >>> rm.load_data_by_id(5)
    <res_manager.manager.ResultManager object at 0x7f29c8587470>
    >>> rm.load_data_by_name('data1')
    [1, 2, 3]
    >>> rm.load_data_by_name('dict_without_topic')
    {0: 1, 1: 'string'}
    >>> rm.delete_data_by_id(3)

ResultManager
=============

This project mainly provides:

* A class named ``ResultManager`` that provides functions to save, load, clear and preview data.
* ``ResultManager.save_data``: Save your data.
* ``ResultManager.load_data_by_name`` and ``ResultManager.load_data_by_id``: Loading data by name or ID.
* ``ResultManager.print_meta_info`` Print all meta info of saved data, including name, path, topic, comments etc.
* ``ResultManager.delete_data_by_id`` Delete data from yor storage.

Future Plan
===========

* Adding support to save and load figures for each piece of data
* Add more interfaces

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


Key release notes
-----------------

* ``1.0.3`` Save data to pickle files, initial version.
* ``2.0.0`` Introduce SQLite to save and manage data.
* ``2.1.1`` Securely closing SQLite connections under any circumstances.
