import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = '1.0.1'
setup(
    name='Clason',
    long_description=README,
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=['clason'],
    url='https://github.com/princessmiku/Clason',
    license='MIT',
    author='Miku',
    author_email='',
    description='Load your classes with json and save it with json or work with python dictionary\'s',
    keywords=['json', 'orm'],
    python_requires='>=3.10.0',
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
)
