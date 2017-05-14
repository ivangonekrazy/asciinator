ASCIInator
==========
(c)2017 Ivan Tam.

A web service for generating grayscale density ASCII art.

Installation and Requirements
-----------------------------

You will to have the Python 2.7 and the `pip` package installed.

Please refer to documenation at:

https://pip.pypa.io/en/stable/installing/

I would also recommend running this service in a Python `virtualenv`.
To install `virtualenv`, please see the documentation at:

https://virtualenv.pypa.io/en/stable/installation/

Create and activate a `virtualenv` environment and install dependencies by
running the following commands in this repo's directory:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

This will install the following packages and their dependencies:

* `Flask`: A well-maintained web microframework. It is minimal and makes it
  easy to get small projects off the ground quickly. The included WSGI server
  `Werkzeug` also includes a very handy debugger.
* `scikit-image`: A high-quality well-known image processing library. I
  leveraged this library's resizing, image-loading, and array manipulation tools.

Running
-------

The included `Makefile` has tasks for running the service as well as
executing the test suite.

* `make start` will start the service at http://localhost:5000/
* `make test` will run the `unittest` suite.

Be sure your `virtualenv` environment is activated when running the above
commands. Otherwise, Python will not be able to locate the required
dependencies.

Usage
-----

Once the service is running, you can interact with it by pointing you browser
at:

http://localhost:5000

At at page, you can select an image file to upload as well an an ASCII art
style. Clicking on the submit button will convert the image to an ASCII art
image in the selected style.

Alternatively, you can use the service via the command-line `curl` utility:

```
curl -XPOST -F "file=@<some image file>" -F "style=<style-name>" http://localhost:5000
```

Where `style-name` is one of the following:
* `grayscale` (default if the `style` parameter is not set)
* `punct`
* `dashy`
* `and_or`
* `black_and_white`

Examples (run from the repo root directory):

```
curl -XPOST -F "file=@sample/sample.jpg" http://localhost:5000
curl -XPOST -F "file=@sample/sample.jpg" -F "style=black_and_white" http://localhost:5000
curl -XPOST -F "file=@sample/sample.jpg" -F "style=dashy" http://localhost:5000
```

Note that images with dimensions over 3000 pixels will be scaled down
before the ASCII art conversion.


Known Issues
------------

There is not upfront validation of the image file. A very large file could be
uploaded to this service and saved on disk before we can determine if we
were given a well-formed image file.

There is currently no limit on the size of the file uploaded.

There is currently no consideration given to how this service will run in a
multiprocess WSGI environment (though the UUIDv4 tempfiles would prevent
filename collisions)

A tempfile is created during the conversion process. There is currently little
error handling for cases like unexpected removal of the temporary file.

There is currently no authentication.
