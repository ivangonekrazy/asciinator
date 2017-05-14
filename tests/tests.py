import base64
import logging
import unittest
import numpy
from cStringIO import StringIO
from asciinator.core import build_blocks, nearest_shape
from asciinator.logger import core_logger, service_logger
from asciinator.service import app

class CoreTests(unittest.TestCase):

    def setUp(self):
        core_logger.setLevel(logging.CRITICAL)

    def test_build_blocks(self):
        rand_array = numpy.random.rand(300, 451)

        blocks = build_blocks(rand_array, (8,8))

        self.assertEquals(
            (38, 57),
            blocks.shape,
            'Should sample blocks from the image array.'
       )

    def test_nearest_shape(self):

        self.assertEquals(
            (304, 456),
            nearest_shape((300, 451), (8,8)),
            "Should round to nearest modulo of block shape."
        )

        self.assertEquals(
            (2000, 2000),
            nearest_shape((8000, 8000), (8,8)),
            "Should down scale oversized shapes."
        )

        self.assertEquals(
            (2008, 2016),
            nearest_shape((8020, 8040), (8,8)),
            "Should down scale and round oversized shapes."
        )

        self.assertEquals(
            (2010, 2016),
            nearest_shape((8020, 8040), (10,8)),
            "Should round shapes to non-square block shapes."
        )

class ServiceTests(unittest.TestCase):
    b64_image = """
    /9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a
    HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIy
    MjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAyADIDASIA
    AhEBAxEB/8QAHAAAAgIDAQEAAAAAAAAAAAAAAAcFBgIDBAgB/8QANxAAAQMDAgMECAUEAwAAAAAA
    AQIDBAAFERIhBjFRE0FhgQcUFSJCcaHRIzIzkrFSYoORs8Hw/8QAGQEAAwEBAQAAAAAAAAAAAAAA
    AgQFAwEG/8QAKBEAAQMDAwMDBQAAAAAAAAAAAQACAwQRURITIQUxQRQicTJCUmGx/9oADAMBAAIR
    AxEAPwBTXaEpD65Kk4ClaXfBfP6/euQtqZ1kN6NAIUTv/wC5gZ86bCuD4pZdTLkqd14StOyQrHnV
    qtSXLlZFiVYnEiOtltTTiwPwwCC57ycYTjlvv8qGpnlgcxgaDq/dllC0Stc4HgLz2l4Bag2PhONJ
    3wRy8ee/yrpbafXkqjuDCQAC2Vf9edP+bEtNqZck3W3eqsCQY6U9gEhZCc60adynY8+vdyqDRbLb
    clLetUlv1VoKK1rCjuNz3Z686CHqOqbZlBac9wikhe2PcaLhKQsPDSgNOjBKisIVjPUbbCtDqHWy
    UKacbQDga0FOee58d6eNktse6x1+z5EaSGF4WvBAyc7cq+xeFDbktie8248AMBGFalEnBOrBIyAN
    snKhVB1SALNddYR6nvDXNsqIx6NnHo7bq5yEqWkKKUoyASOQOd6KbnsmH8d5iNL+JtxsBST0Pv8A
    MUVP36nKubdDj+qalwYMC2yVNMtMktlIKUgZJGKVki9cRP3+eFRJKmAlxqOns9LbauSVknbx38PC
    rNMbTcHXoijIS+nUpt1Ky+9kEBJ93YHcqwOlVi4z+LrJJcRHemT4iAE+sOwiU5HMZIPI7c6ntpJK
    SBvnfNLwtEcpke4c4N1uZDMdLBZuFV+BJMGTaJUifPkMzzJcBW0vT2gAGMbEZ+tY8RuXN2CfUy+4
    +VAFxSgdKPHr5DrUMxMRZeJbTwuHnEsIZck4c93W4onAx+76dKthcQEFZUNI5qzsKckNzfKpUcEb
    Lnyl6JXEIGPXxt/cn7UVyS/Sypqa+2xBbcZQ4pLa8/mSDsfMUV3akW/q6VN++Tr4bXp4XSzGfbWF
    hHZJCXB/TlQ7+oHnUbd3brY7REdjwFzW2yA+ywpRcSDzKOZO5J7vtomy7nHS0faEpae1ShxtAaCl
    BWwwrSnG+O/rWXaD4lXcK6esPH+FYrQdOqXWD3DhQNxo7Kdg2dAgIacTlaxlxatlKJ3OTz8K7o1r
    hwmnEsBRU4rUrBJ3xjy5VXI8u4tOAx3ZOgckywlxH86/rVgYv7Rs7s59ktqYWW3GWjqJXkABJ2zn
    Kccue+KTmoHw8u8ohICld6VeEZN6mM3G2JJnRWwhbedJWnJUMeIz558KUk+4cRtpVbrhJuSAPdUw
    +tY8iDzr0hKfluzPW3y1E1b5baLpT3bqJwDjv0j51rcuLjSAtNziyQTgJLHaLUeg0EfwaYidJGwN
    03sgkqYSRoJGUjmvRfxE6yhzRGRrSFaVO4Iz3HbnRTeMi75Oi0q0934p5ftoo96XCZ1UP5rrun6f
    +aN/zCpGiivQeUgsXNkKx0NaIpzwC8s/nLzyirvyHzg/MYH+qKKmdU+hvyib2KlBUdPSn2lal6Rq
    7Ze+N/0l0UUmpa3tIQWkEpSSUjJIooorNYr/2Q==
    """

    def setUp(self):
        self.client = app.test_client()
        service_logger.setLevel(logging.CRITICAL)

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def test_post_with_invalid_image(self):
        response = self.client.post('/',
            data=dict(file=(StringIO('not-a-pic'), 'some_non_image.png'))
        )
        self.assertEquals(422, response.status_code,
            'Should not process invalid images.')

    def test_post_with_image(self):

        response = self.client.post('/',
            data=dict(file=(StringIO(base64.b64decode(self.b64_image)), 'image.jpg'))
        )
        self.assertEquals(200, response.status_code,
                'Valid images should be successfully processed.')
        self.assertIn('text/plain', response.content_type,
                'Valid images should be turned into ASCII art.')

    def test_ascii_art_style(self):

        response = self.client.post('/',
            data=dict(
                file=(StringIO(base64.b64decode(self.b64_image)), 'image.jpg'),
                style='punct'
            )
        )

        punct_mapper_char_set = set('?!;:., ')
        response_char_set = set(response.data) - set('\n')
        self.assertTrue(response_char_set.issubset(punct_mapper_char_set),
                'ASCII art style should be configurable.')
