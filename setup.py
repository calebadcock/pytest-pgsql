from setuptools import setup
import sys
import os

# Check the Python version manually because pip < 9.0 doesn't check it for us.
if sys.version_info < (3, 4):
    raise RuntimeError('Unsupported version of Python: ' + sys.version)

old_pbr_version = os.getenv('PBR_VERSION') or ''
os.environ['PBR_VERSION'] = '1.1.1'

setup(
    setup_requires=['pbr'],
    pbr=True,
)

os.environ['PBR_VERSION'] = old_pbr_version
