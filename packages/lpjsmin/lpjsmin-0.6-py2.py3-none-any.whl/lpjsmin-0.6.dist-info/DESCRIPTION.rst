lpjsmin for minifying js files
===============================

We need to handle several minification goals within the Launchpad codebase.
This helps to create a single lib to help handle all of the cases and allow it
to be flexibly used in more projects.


Usage
-----

cmd line
~~~~~~~~~
You can pass the cmd line `lpjsmin` either a filename or a directory and it'll
process the file(s) adding a $fname-min.js next to the original file. This is
used for things like minifying files in the combo directory. You can just let
it know the root of the combo directory and it'll minify all files it finds in
there.

::

    $ lpjsmin -p static/js/
    $ lpjsmin -p static/js/myapp.js

python usage
~~~~~~~~~~~~
You can import the module and minify in your own build scripts either via just
filename and directory.

::

    import lpjsmin
    lpjsmin.minify('static/js')
    lpjsmin.minify('static/js/myapp.js')

If you need to be able to customize the name or location of the minified
files, wrap the lpjsmin script in your own build script and pass it the in/out
streams.

::

    import lpjsmin
    lpjsmin.minify_stream(
        open('static/js/myapp.js'),
        open('/tmp/myapp.minified.js', 'w')
    )

stdin
~~~~~~
You can also just pass text at the script via stdin and it'll minimze it back
out to you.

::

    $ cat file.js | lpjsmin


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



