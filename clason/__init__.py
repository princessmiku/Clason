import time
import typing
from datetime import datetime
import json
from os import PathLike



def _convert_single(val, aType, for_json) -> any:
    origin = typing.get_origin(aType)
    if origin:
        args = typing.get_args(aType)
        if origin is list:
            if args is list:
                return [_convert_single(newVal, args[0], for_json) for newVal in val]
            if args is datetime:
                return [_convert_single(newVal, datetime, for_json) for newVal in val]
            if issubclass(args[0], Clason):
                return [newVal.clason_dump_d(for_json) for newVal in val]
            else:
                return val
        elif origin is dict:
            return val
        raise TypeError("Unsupported type")
    elif issubclass(aType, Clason):
        return val.clason_dump_d(for_json)
    elif aType is datetime:
        if for_json:
            return val.isoformat()
        else:
            return val
    elif aType is list:
        return val
    else:
        return val


def _load_single(val, aType) -> any:
    origin = typing.get_origin(aType)
    if origin:
        args = typing.get_args(aType)
        if origin is list:
            if isinstance(val, str):
                val = json.loads(val)
            if args is list:
                return [_load_single(newVal, args[0]) for newVal in val]
            if args is datetime:
                return [_load_single(newVal, datetime) for newVal in val]
            if issubclass(args[0], Clason):
                return [args[0].clason_load_d(newVal) for newVal in val]
            else:
                return val
        elif origin is dict:
            return val
        raise TypeError("Unsupported type")
    elif issubclass(aType, Clason):
        return aType.clason_load_d(val)
    elif aType is datetime:
        return datetime.fromisoformat(val)
    elif aType is list:
        if isinstance(val, str): return json.loads(val)
        return val
    else:
        return aType(val)


class Clason:
    __type_checking__: bool = True
    __type_list__: dict[str, type] = {}

    def clason_dump_d(self, for_json: bool = False) -> dict:
        """
        Dump the class in a python dictionary
        :param for_json: should it optimize for json?
        :return:
        """
        dictionary = {}
        for key, value in self.__dict__.items():
            allowedType = self.__type_list__[key]
            try:
                dictionary[key] = _convert_single(value, allowedType, for_json)
            except TypeError as e:
                if self.__type_checking__:
                    print(e)
                    raise TypeError(
                        f"Error in key '{key}' current type is {type(value).__name__}, "
                        f"the default type is {allowedType.__name__}"
                    ) from None
                else:
                    dictionary[key] = value

        return dictionary

    def clason_dumps(self, indent: None | int | str = None) -> str:
        return json.dumps(self.clason_dump_d(for_json=True), indent=indent)

    def clason_dump(self, path: str | PathLike, indent: None | int | str = None):
        jsonData = self.clason_dumps(indent)
        with open(path, mode='w') as f:
            f.write(jsonData)
            f.close()

    @classmethod
    def clason_load_d(cls, dictionary: dict):
        if not cls.__dict__.__contains__("__annotations__"):
            raise KeyError("no annotations was found")
        if not isinstance(dictionary, dict):
            raise TypeError(
                "The json is a list not an dict, use clason.load_many / clason.loads_many for more than one object"
            )
        child = cls.__new__(cls)
        child.clason_on_init_start()

        for key in cls.__dict__["__annotations__"]:
            typeOfKey: type = cls.__dict__["__annotations__"][key]
            origin: any = typing.get_origin(typeOfKey)
            if dictionary.__contains__(key):
                child.__dict__[key] = _load_single(dictionary[key], typeOfKey)
            else:
                try:
                    cls.__dict__[key]
                except KeyError as e:
                    raise KeyError(f"Key '{key}' has no default value, and no value data was found") from None
                else:
                    value = cls.__dict__[key]
                    try:
                        if not isinstance(value, typeOfKey) and cls.__type_checking__:
                            raise TypeError(
                                f"The default value from key '{key}' must be a {typeOfKey.__name__} "
                                f"not an {type(value).__name__}"
                            )
                    except TypeError as e:
                        if origin: pass
                        elif cls.__type_checking__:
                            raise e
                    child.__dict__[key] = value
        child.clason_on_init_end()
        return child

    @classmethod
    def clason_loads(cls, string: str):
        return cls.clason_load_d(json.loads(string))

    @classmethod
    def clason_load(cls, path: str | PathLike):
        return cls.clason_load_d(json.load(open(path, mode="r")))

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        for key in cls.__dict__["__annotations__"]:
            if cls.__dict__.__contains__(key):
                obj.__dict__[key] = cls.__dict__[key]
            if not cls.__type_list__.__contains__(key):
                cls.__type_list__[key] = cls.__dict__["__annotations__"][key]
        return obj

    def clason_on_init_start(self):
        """
        this function starts at the beginning of the init (no variables are assigned from clason)
        an init function if clason load the class.
        the normal __init__ function is not working, but if you need it use this
        - no function variables allowed -
        """
        pass

    def clason_on_init_end(self):
        """
        this function starts at the end of the init (the variables are assigned from clason)
        an init function if clason load the class.
        the normal __init__ function is not working, but if you need it use this
        - no function variables allowed -
        """
        pass


def load_many_d(listOfClass: list, targetClass) -> list[any]:
    if not issubclass(targetClass, Clason): raise TypeError('Target class is not extend Clason')
    return [targetClass.clason_load_d(c) for c in listOfClass]


def loads_many(jsonStr: str, targetClass) -> list[any]:
    if not issubclass(targetClass, Clason): raise TypeError('Target class is not extend Clason')
    return load_many_d(json.loads(jsonStr), targetClass)


def load_many(path: str | PathLike, targetClass) -> list[any]:
    if not issubclass(targetClass, Clason): raise TypeError('Target class is not extend Clason')
    return load_many_d(json.load(open(path, mode='r')), targetClass)


def dump_many_d(listOfClass) -> list[any]:
    return [c.clason_dump_d(True) for c in listOfClass]


def dumps_many(listOfClass, indent: None | int | str = None) -> str:
    return json.dumps(dump_many_d(listOfClass), indent=indent)


def dump_many(path: str | PathLike, listOfClass, indent: None | int | str = None):
    jsonData = dumps_many(listOfClass, indent)
    with open(path, mode='w') as f:
        f.write(jsonData)
        f.close()
