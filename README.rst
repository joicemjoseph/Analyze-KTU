.. 

Analyzer
======================
KTU Result Analyser is final year ug project by gec wayanad. The project aims to visualize technological university's result, which is given in pdf format.
ultimately to replace yellow card.

Quickstart
----------

To bootstrap the project::

    virtualenv analyzer
    source analyzer/bin/activate
    cd path/to/analyzer/repository
    pip install -r requirements.pip
    pip install -e .
    cp analyzer/settings/local.py.example analyzer/settings/local.py
    manage.py syncdb --migrate

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.

Team Members
------------
- Akhil N
- Ismayil A
- Harsha Govindan
- Joice

