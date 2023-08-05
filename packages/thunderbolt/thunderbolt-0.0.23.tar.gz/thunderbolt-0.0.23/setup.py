from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = ['boto3', 'pandas', 'gokart>=0.2.4', 'tqdm']

setup(
    name='thunderbolt',
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description='gokart file downloader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='6syun9',
    author_email='6syun9@gmail.com',
    url='https://vaaaaanquish.jp',
    install_requires=install_requires,
    packages=find_packages(),
    platforms='any',
    tests_require=['moto==1.3.6'],
    test_suite='test',
    classifiers=['Programming Language :: Python :: 3.6'],
)
