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
