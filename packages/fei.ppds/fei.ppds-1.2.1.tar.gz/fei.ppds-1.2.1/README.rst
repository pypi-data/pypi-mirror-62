fei.ppds
========

Customized synchronization objects. In addition to standard FIFO
``Semaphore``, it implements a LIFO version and a version with
randomized inserts into the waiter queue.

Developed for Parallel Programming and Distributed Systems course at Faculty of
Electrical Engineering and Information Technology STU in Bratislava.

Installation guide
------------------

The package is compatible with Python 3. It was tested under Python 3.8.

Using pip
~~~~~~~~~

.. code:: bash

   pip install --upgrade fei.ppds

Windows
~~~~~~~

.. code:: bash

   py -3 setup.py install

Linux
~~~~~

.. code:: bash

   python3 setup.py install
