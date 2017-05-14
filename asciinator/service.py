"""
    Web REST service.

    Takes POST requests at the root ('/') with the following params:
    - 'file': multipart/form encoded file contents
    - 'style': desired ASCII art style for the returned image

    An HTML web form is returned for rendering in a browser if
    a GET request is issued to the root endpoint.
"""

import os
import uuid
from contextlib import contextmanager
from flask import Flask, render_template, request
from asciinator.core import generate_ascii_art
from asciinator.exception import InvalidImageException
from asciinator.logger import service_logger as logger
from asciinator.mapper import MAPPERS

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask('AsciinatorService', template_folder=TEMPLATES_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', styles=MAPPERS.keys())

    if 'file' not in request.files:
        return render_template('index.html', error="No file selected?")

    mapper_name = request.form.get('style')

    try:
        with file_from_request(request) as temp_filename:
            ascii_art = generate_ascii_art(temp_filename, mapper_name)
    except InvalidImageException, iie:
        return iie.message, 422

    return ascii_art, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@contextmanager
def file_from_request(req):

    _file = req.files['file']
    filename = _file.filename
    _, ext = os.path.splitext(filename)

    tmp_filename = (str(uuid.uuid4()) + ext)

    _file.save(tmp_filename)
    file_size = os.stat(tmp_filename).st_size
    logger.info('Saved tempfile {} from request. {} bytes.'.format(tmp_filename, file_size))

    yield tmp_filename

    logger.info('Removing tempfile {}.'.format(tmp_filename))
    os.remove(tmp_filename)
