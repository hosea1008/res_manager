============================
Experimental Results Manager
============================

This project helps you to handle your experimental results efficiently when doing your research. Basically it uses ``pickle`` to save and load the data, now we provide you with some high-level interfaces so that you can get rid of pickle dumping and loading from disk all the time. Also, with a given ``topic`` parameter when saving data, it can automatically build different directories for different topic.

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