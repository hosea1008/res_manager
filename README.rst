============================
Experimental Results Manager
============================

|PyPI| |Travis build| |License| |Last commit| |Status|

.. |PyPI| image:: https://img.shields.io/pypi/v/res-manager.svg
   :target: https://pypi.org/project/res-manager/

.. |Travis build| image:: https://travis-ci.com/hosea1008/res_manager.svg?branch=master
    :target: https://travis-ci.com/hosea1008/res_manager

.. |License| image:: https://img.shields.io/github/license/hosea1008/res_manager.svg
   :target: https://github.com/hosea1008/res_manager/blob/master/LICENSE

.. |Last commit| image:: https://img.shields.io/github/last-commit/hosea1008/res_manager.svg

.. |Status| image:: https://img.shields.io/pypi/status/res-manager.svg



This project helps you to handle your experimental results efficiently when doing your research. Basically it uses ``pickle`` and ``sqlite3`` to save, load and manage the data, now we provide you with some high-level interfaces so that you can get rid of pickle dumping and loading from disk all the time.

Since it is based on ``pickle``, in theory you can use it to manage all types of data in python, you can even save an object as shown in the following examples.

Installation
============

``pip install res-manager``

Usage
=====

Just start with ``from res_manager import ResultManager``, now you can create an object with ``rm = ResultManager(path)`` and then use it to save, load, delete and preview your data.


::

    >>> from res_manager import ResultManager
    >>> rm = ResultManager('data')
    >>> rm.save([1, 2, 3], topic='test saving', name='data1', comment='Test saving a list')
    >>> rm.save(65535, topic='test saving', comment='Test saving a number without a name')
    >>> rm.save(rm, topic='topic 2', name="object of \"ResultManager\"", comment='Saving an object')
    >>> rm.save({0:1,1:'string'}, name="hongshan's dict without topic")
    >>> rm.print_meta_info()
        ...
    >>> rm.load(3)
        <res_manager.manager.ResultManager object at 0x7f29c8587470>
    >>> rm.load(3, version='first')
        [1, 2, 3]
    >>> rm.delete_by_id(3, version='latest')
    >>> rm.update_meta(1, name='b', topic='topic 5')

ResultManager
=============

This project mainly provides:

* A class named ``ResultManager`` that provides all functions.
* ``ResultManager.save``: Save your data.
* ``ResultManager.load``: Loading data by ID.
* ``ResultManager.print_meta_info``: Print all meta info of saved data, including data id, name, topic.
* ``ResultManager.delete_by_id``: Delete data from yor storage.
* ``ResultManager.update_meta``: Update meta information.
* ``ResultManager.print_names`` and ``ResultManager.print_comments``： Print names and comments.
* ``ResultManager.print_data_info``: Print details of the requested data.

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

``ResultManager`` is developed by Python 3.5 and tested on python 2.6, 2.7, 3.4-3.7


Key release notes
-----------------

* ``1.0.3`` Save data to pickle files, initial version.
* ``2.0.0`` Introduce SQLite to save and manage data.
* ``2.1.0`` Securely closing SQLite connections under any circumstances.
* ``2.2.0`` Add support to quotation marks, add ``update_meta`` interface, simplifier some interfaces.
* ``3.0.0`` Add version control to manage data at different versions with the same name.