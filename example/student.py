import datetime

from clason import Clason, load_many, dump_many


# define a clason class
class Address(Clason):
    # define a str value
    street: str
    # define a int value
    number: int
    city: str
    # define a default str value
    country: str = "Germany"

    def __init__(self, street, number, city, country=country):
        self.street = street
        self.number = number
        self.city = city
        self.country = country


# define a clason class
class Subject(Clason):
    name: str
    # define a default int list
    # if you not define a default value, do not forget to define it on init
    grades: list[int] = []

    def __init__(self, name, grades=None):
        if grades is None:
            grades = grades
        self.name = name
        self.grades = grades


# define a clason class
class Student(Clason):
    # define a str value
    name: str
    # define a int value
    age: int
    # define a sub class
    address: Address
    # define a default value
    # example str, but the other types are possible
    email: str = None
    # define a datetime with a default datetime
    registered: datetime.datetime = datetime.datetime.now()
    # define a list, in this example with a clason class as subtype
    # but other types are possible
    # if you not define a default value, do not forget to define it on init
    subjects: list[Subject] = []
    # define a dictionary, an "any" dictionary do not support clason and datetimes and more,
    # its only support default json types (str, int, float, bool)
    # if you set a specific type, its support clason and datetime.
    # if you not define a default value, do not forget to define it on init
    data: dict[str, any] = {}

    def __init__(self, name, age, address, email=email):
        self.name = name
        self.age = age
        self.address = address
        self.email = email


# example for create a class
anna = Student("Anna", 21, Address('Europaplatz', 1, 'Berlin'))
anna.subjects.append(Subject("Math", [3, 4, 2, 2, 1, 4, 3, 3]))
# Random address with https://www.randomlists.com/texas-addresses
rene = Student("Rene", 25, Address('North Argyle Ave.', 81, 'Humble - TX 77339', 'United States'))
rene.subjects.append(Subject("Math", [4, 5, 5, 2, 3, 3, 1, 6]))

# example save a class
anna.clason_dump('./anna.json')
rene.clason_dump('./rene.json')
# example save a list with classes
# indent is optional
dump_many('students.json', [anna, rene], indent=3)


# example load of a json list
# set the path and the default class structure
students = load_many('students.json', Student)
for student in students:
    # Print the names of the students
    print(student.name)

# this is one example, more functions (dump/load) listed in the readme.md
