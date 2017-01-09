# pyvt

[![Coverage Status](https://coveralls.io/repos/github/kevincianfarini/pyvt/badge.svg?branch=master)](https://coveralls.io/github/kevincianfarini/pyvt?branch=master)
[![Build Status](https://travis-ci.org/kevincianfarini/pyvt.svg?branch=master)](https://travis-ci.org/kevincianfarini/pyvt)


A Virginia Tech Timetable of Classes Python API

### Installation

```shell
pip install py-vt
```

### Usage

Import the Timetable
```python
from pyvt.timetable import Timetable
```

The API provides access to the Timetable through a Timetable object that is instantiated with a term year.

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

returns the class section object from the timetable with the CRN 17583, regardless of whether or not the class is full to capacity. Alternatively if you would like to only find sections that are open:

```python
timetable.crn_lookup('17583')
```

All methods of the timetable provide a defualt argument of ```open_only=True``` when making timetable requests.

Some of the other most commonly used lookup methods are as follows:

```python

def crn_lookup(self, crn_code, open_only=True):
    ...
```
```crn_lookup(...)``` will return either a single ```Section(...)``` object or ```None``` depending on the success of the query. None is returned if there were no available class sections based of the arguments.

The following methods return either a list of ```Section(...)``` objects or ```None``` depending on the success of the query.

```python
def class_lookup(self, subject_code, class_number, open_only=True):
    ...

def cle_lookup(self, cle_code, open_only=True):
    ...

def subject_lookup(self, subject_code, open_only=True):
    ...
```

More refined searches can be accomplished using the ```refined_lookup(...)``` method

```python
def refined_lookup(self, crn_code=None, subject_code=None, class_number=None, cle_code=None, open_only=True):
```

### Usage Codes

Some of the codes that need to be used with this API are solely to satisfy the needs of the VT Timetable posts. Some helpful codes are as follows.

```python
len(crn_code) >= 3

subj_codes = [
    'STAT',
    'MATH',
    'CS',
    'ECE',
    ...
]

len(class_number) == 4

cle_codes = {
    'AR%': 'All Curriculums',
    'AR01': 'Area 1 Classes',
    'AR02': 'Area 2 Classes',
    ...
    'AR07': 'Area 7 Classes'
}
```

### The Section Object

Class sections returned from the timetable come in the form of a ```Section()``` object. All Section objects have the follows properties:

```python
section_attrs = ['crn', 'code', 'name', 'lecture_type', 'credits', 'capacity', 'instructor', 'days', 'start_time', 'end_time', 'location', 'exam_type']
```

Either a single section object or a list of section objects will be returned to you upon a successful query to the VT Timetable. You can access information about class sections from the above attributes.

### The TimetableError

A Timetable error is thrown when either a bad request is made or the VT Timetable is down. In effect, when the status code of the request is not 200. The thrown error can be used to try and gracefully fail to an extent. The TimetableError provides a ```sleep_time``` attribute to allow for a runtime pause.

```python
try:
    timetable.crn_lookup(...)
except TimetableError as e:
    time.sleep(e.sleep_time)
```

The idea behind this is that if the request was bad, your program will sleep for a short amount of time. However if the VT Timetable is down, and multiple successive ```TimetableErrors``` are raised, then ```sleep_time``` grows exponentially to avoid overwhelming the server.