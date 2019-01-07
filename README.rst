============================
Experimental Results Manager
============================

This project helps you to handle your experimental results efficiently when doing your research. Basically it uses ``pickle`` and ``sqlite3`` to save, load and manage the data, now we provide you with some high-level interfaces so that you can get rid of pickle dumping and loading from disk all the time.

Since it is based on ``pickle``, in theory you can use it to manage all types of data in python, you can even save an object as shown in the following examples.

Usage
=====

Just start with ``from res_manager import ResultManager``, now you can create an object with ``rm = ResultManager(path)`` and then use it to save, load, delete and preview your data.

Install ResultManager with ``pip install res-manager``

::

    >>> from res_manager import ResultManager
    >>> rm = ResultManager('data')
    >>> rm.save([1, 2, 3], topic='test saving', name='data1', commit_comment='Test saving a list')
    >>> rm.save(65535, topic='test saving', commit_comment='Test saving a number without a name')
    >>> rm.save(rm, topic='topic 2', name="object of \"ResultManager\"" commit_comment='Saving an object')
    >>> rm.save({0:1,1:'string'}, name="hongshan's dict without topic")
    >>> rm.print_meta_info()
    ...
    >>> rm.load(3)
    <res_manager.manager.ResultManager object at 0x7f29c8587470>
    >>> rm.load(name='data1')
    [1, 2, 3]
    >>> rm.load(name="hongshan's dict without topic")
    {0: 1, 1: 'string'}
    >>> rm.delete_by_id(3)
    >>> rm.update_meta(5, comment="haha")

ResultManager
=============

This project mainly provides:

* A class named ``ResultManager`` that provides all functions.
* ``ResultManager.save``: Save your data.
* ``ResultManager.load``: Loading data by name or ID.
* ``ResultManager.print_meta_info``: Print all meta info of saved data, including name, path, topic, comments etc.
* ``ResultManager.delete_by_id``: Delete data from yor storage.
* ``ResultManager.update_meta``: Update meta information.
* ``ResultManager.print_names`` and ``ResultManager.print_comments``： Print names and comments.

Future Plan
===========

* Adding support to save and load figures for each piece of data
* Add more interfaces

Authors
=======

* Author and lead developer: `Hongshan Li`_

.. _`Hongshan Li`: https://www.hsli.top


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
* ``2.1.0`` Securely closing SQLite connections under any circumstances.
* ``2.2.0`` Add support to quotation marks, add ``update_meta`` interface, simplifier some interfaces.
