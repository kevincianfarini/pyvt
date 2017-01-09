# pyvt

[![Coverage Status](https://coveralls.io/repos/github/kevincianfarini/python-vt-api/badge.svg?branch=master)](https://coveralls.io/github/kevincianfarini/python-vt-api?branch=master)
[![Build Status](https://travis-ci.org/kevincianfarini/python-vt-api.svg?branch=master)](https://travis-ci.org/kevincianfarini/python-vt-api)

A Virginia Tech Timetable of Classes Python API

### Installation

```shell
pip install pyvt
```

### Usage

The API provides access to the Timetable through a Timetable object that is instanciated with a term year.

```python
timetable = Timetable('201701')  # Spring semester of 2017
```

Other term years follow a simple pattern: YYYYMM of start of semester

```python
termyears = {
    'Spring 2017': '201701',
    'Summer I 2017': '201706',
    'Summer II 2017': '201707',
    'Fall 2017': '201708',
    ...
}
```

The timetable object provides some useful methods for pulling data from the VT Timetable.

```python
timetable.crn_lookup('17583', open_only=False)
```

returns the class section object from the timetable with the crn 17583, regardless of whether or not the class is full to capacity. Alternatively if you would like to only find sections that are open:

```python
timetable.crn_lookup('17583')
```

All methods of the timetable provide a defualt argument of open_only=True when making timetable requests.

Some of the other most commonly used lookup methods are as follows:

```python
def class_lookup(self, subject_code, class_number, open_only=True):
    ...

def cle_lookup(self, cle_code, open_only=True):
    ...

def subject_lookup(self, subject_code, open_only=True):
    ...
```

More refined searches can be accomplished using the ```python refined_lookup(...)``` method

```python
def refined_lookup(self, crn_code=None, subject_code=None, class_number=None, cle_code=None, open_only=True):
```