import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = 'Thumbor mongodb storage adapters'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="thumbor_mongodb_storage_webp",
    version="6.0.5",
    author="Bertrand THILL",
    description=("Thumbor thumbor storage adapters - France.tv Release"),
    license="MIT",
    keywords="thumbor mongodb mongo",
    url="https://github.com/francetv/thumbor_mongodb_storage_webp",
    packages=[
        'thumbor_mongodb_storage_webp',
        'thumbor_mongodb_storage_webp.storages',
        'thumbor_mongodb_storage_webp.result_storages'
    ],
    long_description=long_description,
    classifiers=[
        'Development Status ::4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'thumbor>=6.7.0',
        'pymongo>=3.4.0'
    ]
)
