from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='s3kv',
    version='0.1.5',
    author='Balaji Bal',
    description='A Python library for interacting with S3 key-value store',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BalLab/s3kv',
    packages=['s3kv'],
    install_requires=[
        'boto3', 'elasticsearch'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)