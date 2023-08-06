# Py Random Words

## Installation

To install, simply:

```bash
$ pip3 install py_random_words
```

## Usage

```py
from py_random_words import RandomWords

rnd_word = RandomWords()

print(rnd_word.get_word()) # alpaca
print(rnd_word.get_word()) # cat
print(rnd_word.get_word()) # dog
```

## Release steps

```sh
# Make sure you have the latest versions of setuptools and wheel installed
$ python3 -m pip install --user --upgrade setuptools wheel

# Now run this command from the same directory where setup.py is located
$ python3 setup.py sdist bdist_wheel

# Uploading the distribution archives
$ python3 -m pip install --user --upgrade twine
$ python3 -m twine upload dist/*
```

Ref: https://packaging.python.org/tutorials/packaging-projects/#packaging-your-project