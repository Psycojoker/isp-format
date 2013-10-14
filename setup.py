import os
from setuptools import setup


PKG_NAME = 'ispformat'
VERSION = __import__(PKG_NAME).__version__

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'isp-format',
    version = VERSION,
    packages = ['ispformat.validator', 'ispformat.schema', 'ispformat.specs'],
    include_package_data = True,
    scripts = ['ispformat/bin/isp-format-validator'],
    license = '2-clause BSD License',
    description = 'Tools and specification related to FFDN\'s ISP format',
    long_description = README,
    url = 'http://www.ffdn.org/',
    author = 'Gu1',
    author_email = 'gu1@cafai.fr',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'jsonschema',
    ],
    zip_safe = False,
)
