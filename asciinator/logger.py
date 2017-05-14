"""
    Logging configuration.
"""

import logging

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

service_logger = logging.getLogger('service')
service_logger.setLevel(logging.DEBUG)
service_logger.addHandler(console)

core_logger = logging.getLogger('core')
core_logger.setLevel(logging.DEBUG)
core_logger.addHandler(console)
