# Clason

----
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python - ^3.10](https://img.shields.io/badge/Python-^3.10-blue)](https://www.python.org/)
[![Downloads](https://pepy.tech/badge/clason)](https://pepy.tech/project/clason)


Load your classes with json and save it with json or work with python dictionary's

For an example usage look in the folder ``example``


# Install
________

Install the package with pip ``pip install clason``

Install with pip + github ``pip install git+https://github.com/princessmiku/Clason``


# Basic Setup
________

```python
from clason import Clason

class Student(Clason):
    ...
```

### Example Class

```python
class Student(Clason):
    name: str
    age: int
    address: Address
    email: str = None
```

# How to use?
________

### Set a variable with type

``name: str``, `age: int`

Supported Types: ``str``, ``int``, ``list``, ``dict``, ``datetime``, ``float``, ``Clason class``

Note: time is a float, ``current_time: float = time.time()``

_Values without type are not possible_

### Set a variable with default value
``name: str = "Anna"``, `age: int = 22`, `date: datetime.datetime = datetime.datetime.now()`

if you set a default value, you need only to define a normale variable


### Work with List
``list: list``, `list: list[str]`, `list: list[class]`

if you set a list, you can define a subtype, as subtype you can use alle regular supported types.

Note: If you not define a subtype, it could be make problems with datetime and a clason classes because they are handled differently 

### Work with Dictionary
``dict: dict[str, any]``, `dict[str, str]`

if you set a list, you can define a subtype, as subtype you can use alle regular supported types.
if you not want to define a subtype you need to write ``any``, else it could make problems

### Work with a Clason class
``myClass: ClassWithClasson``

It's possible to set a type as a Clason class, if you have another class that extends Clason, for example a Address class.
Clason.

Clason will then initalize these in the same way as all other clason classes. This is also possible to inherit more often

# Functions
________

### On Class initialization

It is possible to write your own __init__ method during the initialization of a class, before and after. 

#### Setup
````python
from clason import Clason
class Student(Clason):
    name: str

    def clason_on_init_start(self):
        # starts before the loading process
        ... # your code
    def clason_on_init_end(self):
        # starts at the end of the loading process
        ... # your code
````

## Class loading

If you want to load your json file or a python dictionary do this

### Load - Single
Load a single json/python dictionary
````python
from clason import Clason
class Student(Clason):
    name: str

anna = Student.clason_load("anna.json") # load from a json file

anna = Student.clason_loads("...") # load from a json string

anna = Student.clason_load_d({...}) # load from a python dictionary
````

### Load - Multi
Load a list of data from a json/python dictionary

A multi load function need a target class

Its return a list with the loaded target class
````python
from clason import Clason, load_many, loads_many, load_many_d

class Student(Clason):
    name: str

students = load_many('students.json', Student)  # load from a json file

students = loads_many("...", Student)  # load from a json string

students = load_many_d([{},...], Student) # load from a python dictionary
````


## Class saving

If you want to save your class in a json file or a python dictionary do this

``Indent`` is optional, try it out what it does, it's except an integer

### Save - Single
Save a single class in a json/python dictionary
````python
from clason import Clason
class Student(Clason):
    name: str
    
    def __init__(self, name):
        self.name = name
anna = Student("Anna")
anna.clason_dump("anna.json", indent=2) # save in a json file
anna_str = anna.clason_dumps(indent=2) # save in a json string, it return a string

anna_dict = anna.clason_dump_d() # save in a python dictionary, it returns a python dictionary
````

### Save - Multi
Save a list of classes in a json/python dictionary

A multi save need a list with the classes

````python
from clason import Clason, dump_many, dumps_many, dump_many_d


dump_many('students.json', [anna, ...], indent=2) # save in a json file

students_str = dumps_many([anna, ...], indent=2)  # save in a json string, it return a string

students_dict = dump_many_d([anna, ...]) # save in a python dictionary, it returns a list with python dictionarys
````
