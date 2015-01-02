===============
dif-cpp-judger
===============

**Note: This project currently is under development and has some security issue.Use it at your own risk.**

This is a django project for cpp education.
We can write down some cpp question.
Let user upload their codes to compile and execute at server side.

Any pull requests are wellcome.

==============
Requirements
==============
* python 2.7
* Django 1.7 or later
* Celery 3.1 + and one of `celery  <http://www.celeryproject.org/>`_ supported broker
* AngularJs 1.x

============
Installation
============
First, ``git clone`` and ``cd`` to this repo

::

 pip install -r requirements.txt
 cp _/settings.py.sample _/settings.py

Configuration
=============
There is some vars need to be configure in ``_/settings.py``.

* ``SECRET_KEY``: please see https://gist.github.com/ndarville/3452907
* We use facebook oauth to auth user, please refere the `python-social-auth <https://github.com/omab/python-social-auth>`_
* ``JUDGE_DIR``: The tmp dir for compiling code.
* ``JUDGE_ITEM_PER_LIST``: Currently no function.
* ``JUDGE_CPP_COMPILER``: The cpp compiler.

Run server
===========
Besides running your favor web server you also need to start the celery worker using ``./celery.sh``.


========
License
========
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE Version 2

