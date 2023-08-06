# Py Random Words

## Installation

To install, simply:

```bash
$ pip install py_random_words
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
$ python3 -m pip install --user --upgrade setuptools wheel twine

# Now run this command from the same directory where setup.py is located
$ make build

# Uploading the distribution archives
$ make release
```

Ref: https://packaging.python.org/tutorials/packaging-projects/#packaging-your-project