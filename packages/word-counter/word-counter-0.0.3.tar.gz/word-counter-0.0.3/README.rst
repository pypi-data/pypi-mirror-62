.. image:: https://img.shields.io/pypi/v/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/pypi/l/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/pypi/pyversions/word-counter.svg
 :target: https://pypi.org/project/word-counter/
.. image:: https://img.shields.io/github/contributors/sig9org/word-counter.svg
 :target: https://github.com/sig9org/word-counter/graphs/contributors

word-counter
==================================================

Count the number of words on the specified URL(s).

Requirements
==================================================

- python 3.4+
- libicu-devel

Installation
==================================================

In case of CentOS8, execute as follows:

.. code-block:: bash

    # dnf -y install libicu-devel
    # pip install word-counter

Usage (CLI)
==================================================

Count words.
--------------------------------------------------

.. code-block:: bash

    $ word-counter --klass 'site-content' https://blogs.cisco.com/developer
    {
      "count": 226,
      "count_duplicates": 377,
      "words": {
        ",": 18,
        "2020": 11,
        ".": 11,
        .
        .
        .
        "DevNetAPIsnetwork": 1,
        "monitoringStealthwatch": 1,
        "1234": 1
      }
    }


Count words in multiple URLs.
--------------------------------------------------

.. code-block:: bash

    $ word-counter \
    >     https://blogs.cisco.com/developer/node-red-webinar \
    >     https://blogs.cisco.com/developer/meraki-python-sdk-webinar \
    >     https://blogs.cisco.com/developer/understanding-meraki-apis
    {
      "count": 404,
      "count_duplicates": 1018,
      "words": {
        ",": 51,
        "the": 36,
        "and": 30,
        .
        .
        .
        "Related": 1,
        "Resources": 1,
        "certifications": 1
      }
    }
