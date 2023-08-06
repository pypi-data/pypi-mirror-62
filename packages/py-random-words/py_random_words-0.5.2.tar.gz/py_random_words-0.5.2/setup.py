from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='py_random_words',
      version='0.5.2',
      packages=find_packages(exclude=['tests*']),
      url='https://github.com/andreasonny83/py_random_words',
      license='MIT',
      author='andreasonny83',
      author_email='andreasonny83@gmail.com',
      description='Generate random names',
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['choice'],
      data_files=[('animals.json', ['py_random_words/animals.json'])],
      include_package_data=True,
      zip_safe=False,
)
