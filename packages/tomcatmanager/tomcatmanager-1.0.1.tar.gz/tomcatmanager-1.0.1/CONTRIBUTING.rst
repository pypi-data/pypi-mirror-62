Contributing
============

Get Source Code
---------------

Clone the repo from github::

  $ git clone git@github.com:tomcatmanager/tomcatmanager.git


Create Python Environments
--------------------------

tomcatamanger uses `tox <https://tox.readthedocs.io/en/latest/>`_ to run the
test suite against multiple python versions. I recommend using `pyenv
<https://github.com/pyenv/pyenv>`_ with the `pyenv-virtualenv
<https://github.com/pyenv/pyenv-virtualenv>`_ plugin to manage these various
versions. If you are a Windows user, ``pyenv`` won't work for you, you'll
probably have to use `conda <https://conda.io/>`_.

This distribution includes a shell script ``build-pyenvs.sh`` which
automates the creation of these environments.

If you prefer to create these virtual envs by hand, do the following::

  $ cd tomcatmanager
  $ pyenv install 3.8.0
  $ pyenv virtualenv -p python3.8 3.8.0 tomcatmanager-3.8
  $ pyenv install 3.7.5
  $ pyenv virtualenv -p python3.7 3.7.5 tomcatmanager-3.7
  $ pyenv install 3.6.9
  $ pyenv virtualenv -p python3.6 3.6.9 tomcatmanager-3.6
  $ pyenv install 3.5.8
  $ pyenv virtualenv -p python3.5 3.5.8 tomcatmanager-3.5


Now set pyenv to make all four of those available at the same time::

  $ pyenv local tomcatmanager-3.8 tomcatmanager-3.7 tomcatmanager-3.6 tomcatmanager-3.5

Whether you ran the script, or did it by hand, you now have isolated virtualenvs
for each of the minor python versions. This table shows various python commands,
the version of python which will be executed, and the virtualenv it will
utilize.

=============  ======  =================
Command        python   virtualenv
=============  ======  =================
``python``     3.8.0   tomcatmanager-3.8
``python3``    3.8.0   tomcatmanager-3.8
``python3.8``  3.8.0   tomcatmanager-3.8
``python3.7``  3.7.5   tomcatmanager-3.7
``python3.6``  3.6.9   tomcatmanager-3.6
``python3.5``  3.5.8   tomcatmanager-3.5
``pip``        3.8.0   tomcatmanager-3.8
``pip3``       3.8.0   tomcatmanager-3.8
``pip3.8``     3.8.0   tomcatmanager-3.8
``pip3.7``     3.7.5   tomcatmanager-3.7
``pip3.6``     3.6.9   tomcatmanager-3.6
``pip3.5``     3.5.8   tomcatmanager-3.5
=============  ======  =================


Install Dependencies
--------------------

Now install all the development dependencies::

  $ pip install -e .[dev]

This installs the tomcatmanager package "in-place", so the package points
to the source code instead of copying files to the python
``site-packages`` folder.

All the dependencies now have been installed in the ``tomcatmanager-3.8``
virtualenv. If you want to work in other virtualenvs, you'll need to manually
select it, and install again::

  $ pyenv shell tomcatmanager-3.6
  $ pip install -e .[dev]


Branches, Tags, and Versions
----------------------------

This project uses a simplified version of the `git flow branching
strategy <http://nvie.com/posts/a-successful-git-branching-model/>`_. We
don't use release branches, and we generally don't do hotfixes, so we
don't have any of those branches either. The master branch always
contains the latest release of the code uploaded to PyPI, with a tag for
the version number of that release.

The develop branch is where all the action occurs. Feature branches are
welcome. When it's time for a release, we merge develop into master.

This project uses `semantic versioning <https://semver.org/>`_.


Invoking Common Development Tasks
---------------------------------

This project uses many other python modules for various development tasks,
including testing, rendering documentation, and building and distributing
releases. These modules can be configured many different ways, which can
make it difficult to learn the specific incantations required for each
project you are familiar with.

This project uses `invoke <http://www.pyinvoke.org>`_ to provide a clean,
high level interface for these development tasks. To see the full list of
functions available::

  $ invoke -l

You can run multiple tasks in a single invocation, for example::

  $ invoke clean docs sdist wheel

That one command will remove all superflous cache, testing, and build
files, render the documentation, and build a source distribution and a
wheel distribution.

You probably won't need to read further in this document unless you
want more information about the specific tools used.


Testing
-------

To ensure the tests can run without an external dependencies,
``tests/mock_server80.py`` contains a HTTP server which emulates the behavior
of Tomcat Manager 8.0. There is a test fixture to start this server, and all
the tests run against this fixture. I created this fixture to speed up testing
time. It doesn't do everything a real Tomcat server does, but it's close enough for the tests to run, and it allows you to parallelize the test suite using ``python-xdist``.

You can run the tests against all the supported versions of python using tox::

  $ tox

tox expects that when it runs ``python3.4`` it will actually get a python from
the 3.4.x series. That's why we set up the various python environments earlier.

If you just want to run the tests in your current python environment, use
pytest::

  $ pytest

This runs all the test in ``tests/`` and also runs doctests in
``tomcatmanager/`` and ``docs/``.

You can speed up the test suite by using ``pytest-xdist`` to parallelize the
tests across the number of cores you have::

  $ pip install pytest-xdist
  $ pytest -n8

In many of the doctests you'll see something like:

>>> tomcat = getfixture('tomcat')

This ``getfixture()`` helper imports fixtures defined in ``conftest.py``,
which has several benefits:

- reduces the amount of redundant code in doctests which shows connecting
  to a tomcat server and handling exceptions
- allows doctests to execute against a mock tomcat server


Testing Against A Real Server
-----------------------------

If you wish, you can run the test suite against a real Tomcat Server instead of
against the mock server included in this distribution. Running the test suite
will deploy and undeploy an app hundreds of times, and will definitely trigger
garbage collection, so you might not want to run it against a production
server.

It's also slow (which is why the tests normally run against a mock server).
When I run the test suite against a stock Tomcat on a Linode with 2 cores and
4GB of memory it takes approximately 3 minutes to complete. I don't think
throwing more CPU at this would make it any faster: during the run of the test
suite the Tomcat Server never consumes more than a few percent of the CPU
capacity.

You must prepare some files on the server in order for the test suite to run
successfully. Some of the tests instruct the Tomcat Server to deploy an
application from a warfile stored on the server. I suggest you use the minimal
application included in this distribution at
``tomcatmanager/tests/war/sample.war``, but you can use any valid war file. Put
this file in some directory on the server; I typically put it in
``/tmp/sample.war``.

You must also construct a minimal context file on the server. You can see an
example of such a context file in ``tomcatmanager/tests/war/context.xml``:

.. code-block:: xml

  <?xml version="1.0" encoding="UTF-8"?>
  <!-- Context configuration file for my web application -->
  <Context path='/ignored' docBase='/tmp/sample.war'>
  </Context>

The ``docBase`` attribute must point to a valid war file or the tests will
fail. It can be the same minimal war file you already put on the server. The
``path`` attribute is ignored for context files that are not visible to Tomcat
when it starts up, so it doesn't matter what you have there. I typically put
this context file at ``/tmp/context.xml``.

You will also need:

- the url where the manager app of your Tomcat Server is available
- a user with the ``manager-script`` role
- the password for the aforementioned user

With all these prerequisites ready, you can feed them to ``pytest`` as shown:

.. code-block:: shell

  $ pytest --url=http://localhost:8080/manager --user=ace \
  --password=newenglandclamchowder --warfile=/tmp/sample.war \
  --contextfile=/tmp/context.xml

.. warning::

  If you test against a real Tomcat server, you should not use the
  ``pytest-xdist`` plugin to parallelize testing across multiple CPUs or
  many platforms. Many of the tests depend on deploying and undeploying an
  app at a specific path, and that path is shared across the entire test
  suite. It wouldn't help much anyway because the testing is constrained
  by the speed of the Tomcat server.

If you kill the test suite in the middle of a run, you may leave the test
application deployed in your tomcat server. If this happens, you must undeploy
it before rerunning the test suite or you will get lots of errors.

When the test suite deploys applications, it will be at the path returned by
the ``safe_path`` fixture in ``conftest.py``. You can modify that fixture if
for some reason you need to deploy at a different path.


Code Quality
------------

Use ``pylint`` to check code quality. There is a pylint config file for the
tests and for the main module::

  $ pylint --rcfile=tests/pylintrc tests
  $ pylint --rcfile=tomcatmanager/pylintrc tomcatmanager

You are welcome to use the pylint comment directives to disable certain
messages in the code, but pull requests containing these directives will be
carefully scrutinized.

As allowed by
`PEP 8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_
this project uses a nominal line length of 100 characters.


Documentation
-------------

The documentation is written in reStructured Test, and turned into HTML using
`Sphinx <http://www.sphinx-doc.org>`_::

  $ cd docs
  $ make html

The output will be in ``docs/build/html``.

If you are doing a lot of documentation work, the `sphinx-autobuild
<https://github.com/GaretJax/sphinx-autobuild>`_ module has been integrated.
Type::

  $ cd docs
  $ make livehtml

Then point your browser at `<http://localhost:8000>`_ to see the
documentation automatically rebuilt as you save your changes.

.. note::

  The ``sphinx-autobuild`` module has some limitations. Much of the
  documentation produced in this project is contained in the source code, and
  is incorporated via the Sphinx ``autodoc`` module. In order for ``autodoc``
  to work, it must import the source code, and it's not very good about
  noticing and reloading source code modules as they change. If you change
  the source code and want to make sure you are seeing the current changes
  in your browser, best to kill the webserver and start it back up again.

Use ``doc8`` to check documentation quality::

  $ invoke doc8


Make a Release
--------------

To make a release and deploy it to `PyPI
<https://pypi.python.org/pypi>`_, do the following:

1. Merge everything to be included in the release into the **develop** branch.

2. Run ``tox`` to make sure the tests pass in all the supported python versions.

3. Review and update ``CHANGELOG.rst``.

4. Update the milestone corresponding to the release at `https://github.com/tomcatmanager/tomcatmanager/milestones <https://github.com/tomcatmanager/tomcatmanager/milestones>`_

5. Push the **develop** branch to github.

6. Create a pull request on github to merge the **develop** branch into
   **master**. Wait for the checks to pass.

7. Merge the **develop** branch into the **master** branch and close the pull
   request.

8. Tag the **master** branch with the new version number, and push the tag.

9. Build source distribution, wheel distribution, and upload them to pypi staging::

     $ invoke pypi-test

10. Build source distribution, wheel distribution, and upload them to pypi::

      $ invoke pypi

11. Docs are automatically deployed to http://tomcatmanager.readthedocs.io/en/stable/.
    Make sure they look good. Add a "Version" in readthedocs which points to the tag
    you just created. Prune old versions as necessary.

12. Switch back to the **develop** branch. Add an **Unreleased** section to
    the top of ``CHANGELOG.rst``. Push the change to github.
