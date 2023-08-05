.. image:: https://img.shields.io/pypi/v/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/pypi/l/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/pypi/pyversions/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/github/contributors/sig9org/word-counter.svg
 :target: https://github.com/sig9org/word-counter/graphs/contributors

word-counter
========================================

Count the number of words on the specified URL(s).

Requirements
========================================

- python 3.4+
- libicu-devel

Installation
========================================

In case of CentOS8, execute as follows:

.. code-block:: bash

    # dnf -y install libicu-devel
    # pip install word-counter

Usage (CLI)
========================================

Count words, list results.
----------------------------------------

.. code-block:: bash

    $ word-counter --klass 'site-content' https://blogs.cisco.com/developer
    {
      ",": 18,
      "2020": 11,
        .
        .
        .
      "monitoringStealthwatch": 1,
      "1234": 1
    }


Just count words
----------------------------------------

.. code-block:: bash

    $ word-counter --count-only --klass 'site-content' https://blogs.cisco.com/developer
    377
