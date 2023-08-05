Introduction
============

Installing
==========

If you have `pip <https://pip.pypa.io/>`_ on your system, you can simply install or upgrade the Python bindings::

	pip install --upgrade ibmBluepages
	
Example 1
==========

from ibmBluepages import ibmBluepages

ibmBluepages = ibmBluepages()
personInfo = ibmBluepages.getPersonInfoByIntranetID("intrenetID")
print(personInfo)

Supported Python Version
==========

Tested on: Python 3.5+.