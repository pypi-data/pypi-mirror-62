.. This is your project NEWS file which will contain the release notes.
.. Example: http://www.python.org/download/releases/2.6/NEWS.txt
.. The content of this file, along with README.rst, will appear in your
.. project's PyPI page.

News
====

0.6
---

* Add tox testing support and drop buildout.
* Add Python 3 support.
* Use PEP 508 environment markers.


0.5
---
*Release date: 11-June-2012*

* Ignore any files that don't end in .js
* Fix broken logic detecting if this file was already minified or not that
  allowed multiple nested minifications (filename-min-min-min.js)


0.4
---
*Release date: 21-Feb-2012*

* Fix typo in the setup.py


0.3
----
*Release date: 21-Feb-2012*

* Add argparse as a conditional dep for older Python versions.


0.2
----
*Release date: 21-Feb-2012*

* Move the file/directory based minifying to the -p/--path cmd line flag.
* Support minifying off of stdin and sending to stdout if no path is
  specified.
* Fix the ipdb dependency that should not have been there.

0.1
---

*Release date: 17-Feb-2012*

* Initial pulling out of the Launchpad utils directory.

