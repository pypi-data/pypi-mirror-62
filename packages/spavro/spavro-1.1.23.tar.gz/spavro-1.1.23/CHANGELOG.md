Spavro Changelog
-----------------

1.1.23 - Feb 21, 2020
=====================

- Fix bug with buffer in datafile output via a ([pull request](https://github.com/pluralsight/spavro/pull/10))

1.1.22 - Apr 9, 2019
====================

- Added support for xz codec via a ([pull request](https://github.com/pluralsight/spavro/pull/7))
- Improved the error reporting / validation for integers, calling out overflows as a separate case from non-integers.
- Add union test for integer/float case

1.1.21 - Jan 19, 2019
=====================

- Add fix for case when int values are presented to a union containing a 'float' schema. Allow the int to be stored using the float schema.

1.1.20 - Oct 6, 2018
=====================

- Add better handling for appending avro records when the file obejct isn't opened using the right mode.

1.1.18, 1.1.19 - Aug 20, 2018
=====================

- Fixed bug with the schema resolver where named schemas were not being handled properly

1.1.17 - May 4, 2018
=====================

- Version bump to try and fix the docs again

1.1.16 - May 4, 2018
=====================

- Deploy Bug: Bug with new pypi deploy led to extension code not being in the package. This release has the extension code in it.

1.1.12, 1.1.13, 1.1.14, 1.1.15 - May 3, 2018
============================================

- Pypi requires a full version to update the description, attempting to add the
markdown version of the description to pypi

1.1.11 - Apr 30, 2018
=====================

- Fix bug with namespace handling where names with 'dots' in them were still
being concatenated with the namespace leading to bogus names
- The array data 'check' function also had a bug where it was not verifying that
the datum was a list before attempting to check that all items conformed to the schema

1.1.8, 1.1.9, 1.1.10 - Mar 19, 2018
===================================

- Fix bug with C implementation of zig zag decoder. Additional unnecessary cast was clipping during the bit shifting for larger numbers.
- Skipping 1.1.8 and 1.1.9 was missing C cythonized code and created incompatibilities with python 2.7

1.1.7 - Mar 6, 2018
===================

- Fix bug with 'bytes' type in union schemas failing to parse

1.1.6 - Jan 17, 2018
====================

- Fix bug with reference types (named references) inside unions

1.1.5 - Jan 4, 2018
===================

- Remove accidental debug loglevel logging directive

1.1.4 - Dec 22, 2017
====================

- Add more helpful exception messages (mainly for Python 3 with chained exceptions) that will describe which field in a record datum failed and when ints and strings mismatch, show the datum and the schema.
- Fix some old non-py3 incompatible utility code to be py2/py3

1.1.3 - Dec 4, 2017
===================

- Fix source distribution Cython file inclusion ([pull request](https://github.com/pluralsight/spavro/pull/2))

1.1.2 - Nov 14, 2017
====================

- Add more type checking in the serializer. Some fast data types were leading to spavro not rejecting bad data.
- Add tests to verify that invalid (no schema conforming data) is rejected

1.1.1 - Oct 31, 2017
====================

- Fix bug with Enum adding it to the named types that can be namespaced.
- Fix bug with 32bit systems that could potentially trucate long data at 2^31 bits

1.1.0 - June 20, 2017
=====================

- Add code to support pickling spavro records. This allows the use of spavro in contexts like Spark that need to serialize the data to be shipped around.

1.0.0 - June 7, 2017
====================

- First release of spavro, speedier avro for python!
