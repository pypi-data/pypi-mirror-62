Microsoft Azure Machine Learning Data Collection API for Python
===============================================================

This package has been tested with Python 2.7 and 3.5.

This is a preview release
=========================

The SDK is being released as a preview, for gathering feedback.

**Future releases are subject to breaking changes.**

.. :changelog:

Release History
===============

0.1.0a15 (2019-05-14)
^^^^^^^^^^^^^^^^^^^^^

* change 'identifier' keyword param to 'designation', Supported designations: 'inputs', 'predictions', 'labels', 'signals, 'general'
* add 'collection_name' paramter to intialization params
* collect method for 'inputs' designation now returns a dictionary with correlation data
* add_correlations method added. This method will take input data and correlation data, and augment input data with correlations

0.1.0a1 (2017-05-30)
^^^^^^^^^^^^^^^^^^^^

* Preview release.

