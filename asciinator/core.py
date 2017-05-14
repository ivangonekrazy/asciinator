"""
    Loads image data and returns an ASCII art
    representation of the image.
"""

import numpy as np
from skimage import io, transform
from skimage.util.shape import view_as_blocks
from asciinator.exception import InvalidImageException
from asciinator.logger import core_logger as logger
from asciinator.mapper import get_mapper

# (Width, height) shape of a block.
# Each resulting ASCII character represents a block of this size in the image.
# This shape is non-square to compensate for most typefaces being tall
# in ascpect ratio.
BLOCK_SHAPE = (16, 8)

def generate_ascii_art(filename, mapper_name=None):
    """ Given a filename of an image,
        return a string of ASCII chars representing the image.
    """

    n_array = read_file(filename)
    blocks = build_blocks(n_array, BLOCK_SHAPE)
    txt = render_ascii(blocks, get_mapper(mapper_name))

    return txt


def read_file(filename):
    """ Returns grayscale image pixel data as a NumPy array
        with MxN shape.
    """

    try:
        logger.info('Loading image file: {}'.format(filename))
        return io.imread(filename, as_grey=True)
    except IOError:
        raise InvalidImageException()


def build_blocks(img_ndarr, block_shape):
    """ Transforms image into an array of non-overlapping
        blocks with shape of block_shape.

        The median grayscale value of each block is returned
        in a a new NumPy array.

        Reference:
        http://scikit-image.org/docs/dev/auto_examples/numpy_operations/plot_view_as_blocks.html
    """

    current_shape = img_ndarr.shape

    resized = transform.resize(
        img_ndarr, nearest_shape(current_shape, block_shape), mode='constant')

    block_view = view_as_blocks(resized, block_shape)
    view_shape = block_view.shape

    flattened_block_view = block_view.reshape(view_shape[0], view_shape[1], -1)
    median_blocks = np.median(flattened_block_view, axis=2)

    return median_blocks


def render_ascii(blocks, char_mapper):
    """ Maps grayscale values into
        ASCII characters.

        Returns a string.
    """

    blocks_mapper = np.vectorize(char_mapper)
    ascii_blocks = blocks_mapper(blocks)

    return '\n'.join([''.join(row) for row in ascii_blocks])


def nearest_shape(current_shape, block_shape, max_dim=3000):
    """ Given a shape tuple, return a new
        shape tuple that:

        - Has both dimensions smaller than the defined
          maximum.
        - Has dimensions that are modulos of the block
          size.
    """
    shape_width = current_shape[0]
    shape_height = current_shape[1]


    while (shape_width > max_dim) or (shape_height > max_dim):
        shape_width = shape_width // 2
        shape_height = shape_height // 2

    while shape_width % block_shape[0] != 0:
        shape_width += 1

    while shape_height % block_shape[1] != 0:
        shape_height += 1

    logger.info(
        'Reshape from {} to {} to accomodate {} block shape.'.format(
            current_shape, (shape_width, shape_height), block_shape)
    )

    return (shape_width, shape_height)
