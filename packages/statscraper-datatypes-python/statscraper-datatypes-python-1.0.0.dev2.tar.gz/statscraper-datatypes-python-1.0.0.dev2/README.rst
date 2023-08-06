Python bindings for ``statscraper-datatypes``. Requires Python 3.7
(because it uses dataclasses).

For developers
--------------

These instructions are for developers working on this packages

Downloading
~~~~~~~~~~~

.. code:: sh

     git clone https://gitlab.com/jplusplus/statscraper
     pip install -r requirements.txt

This repo includes ``statscraper-datatypes`` as a subtree. To update
this, do:

.. code:: sh

     git subtree pull --prefix datatypes/datatypes git@github.com:jplusplus/statscraper-datatypes.git master --squash

Publishing
~~~~~~~~~~

Remember to change the version number in setup.py before tagging a new
version!

.. code:: sh

   git push
   git tag X-Y-X
   git push --tags
   python3 setup.py sdist bdist_wheel
   python3 -m twine upload dist/statscraper-datatypes-python-X-Y-X*
