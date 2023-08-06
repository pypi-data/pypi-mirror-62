.. fluidfoam documentation master file, created by
   sphinx-quickstart on Thu Jan 11 12:22:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FluidFoam documentation
=======================


The fluidfoam package provides Python classes useful to perform some plot with OpenFoam data.

What is this repository for?
----------------------------

* Openfoam Tools
* Version : 0.2.1
* Supported OpenFoam Versions : 2.4.0, 4.1 to 7, v1712plus to v1912plus
* Supported Python Versions : 2.7.x, >= 3.4


Deployment instructions
-----------------------

The simplest way to install fluidfoam is by using pip::

  pip install fluidfoam --user

You can get the source code from `github
<https://github.com/fluiddyn/fluidfoam>`_ or from `the Python Package Index
<https://pypi.python.org/pypi/fluidfoam/>`_.

The development mode is often useful. From the root directory, run::

  python setup.py develop --user


Committing instructions (in development mode)
---------------------------------------------

A good starting point is to follow this `forking tutorial <https://guides.github.com/activities/forking/>`_.

To clone your fork of fluidfoam repository::

  git clone https://github.com/your_username/fluidfoam
  
To get the status of the repository::

  git status

In case of new/modified file(s)::

  git add new_file

To commit a revision on the local repository::

  git commit -m "comment on the revision"

To push the revision on your github fluidfoam repository::

  git push

To propose your changes into the main fluidfoam project, follow again the `forking tutorial <https://guides.github.com/activities/forking/>`_.

Example Usage
-------------

* http://servforge.legi.grenoble-inp.fr/pub/soft-sedfoam/

Core Developers
---------------

* Cyrille.Bonamy@legi.cnrs.fr
* Julien.Chauchat@grenoble-inp.fr
* Antoine.Mathieu@univ-grenoble-alpes.fr

Emeritus Core Developers
------------------------

* Pierre.Augier@legi.cnrs.fr

Emeritus Developers
------------------------

* Guillaume.Maurice@univ-grenoble-alpes.fr
* Tim.Nagel@legi.cnrs.fr

License
-------

fluidfoam is distributed under the GNU General Public License v2 (GPLv2).

.. _GPLv2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html


.. User Guide
.. ----------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

..   overview
..   install
..   tutorial
..   examples


Modules Reference
-----------------

Here is presented the general organization of the package
and the documentation of the modules, classes and
functions.

.. autosummary::
   :toctree: generated/

   fluidfoam.readof
   fluidfoam.processing1d
   fluidfoam.readpostpro
   fluidfoam.meshdesign

.. toctree::
   :maxdepth: 2
   :caption: Example galleries:

   auto_examples/index


More
----

.. |release| image:: https://img.shields.io/pypi/v/fluidfoam.svg
   :target: https://pypi.python.org/pypi/fluidfoam/
   :alt: Latest version

.. |docs| image:: https://readthedocs.org/projects/fluidfoam/badge/?version=latest
   :target: http://fluidfoam.readthedocs.org
   :alt: Documentation status

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/ipwdnr1an8su429q?svg=true
.. _AppVeyor: https://ci.appveyor.com/project/CyrilleBonamy/fluidfoam/history

.. |coverage| image:: https://codecov.io/gh/fluiddyn/fluidfoam/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/fluiddyn/fluidfoam/branch/master/
   :alt: Code coverage




- `FluidFoam forge on github <https://github.com/fluiddyn/fluidfoam>`_
- FluidFoam in PyPI |release|
- Unittest coverage |coverage|

.. toctree::
   :maxdepth: 1

..   changes
..   to_do

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
