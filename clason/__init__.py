import time
import typing
from datetime import datetime
import json
from os import PathLike



def _convert_single(val, aType, for_json) -> any:
    origin = typing.get_origin(aType)
    if origin:
        args = typing.get_args(origin)
        if origin is list:
            if args is list:
                return [_convert_single(newVal, args[0], for_json) for newVal in val]
            if args is datetime:
                return [_convert_single(newVal, datetime, for_json) for newVal in val]
            else:
                return val
        elif origin is dict:
            return val
        raise TypeError("Unsupported type")
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
        args = typing.get_args(origin)
        if origin is list:
            if args is list:
                return [_load_single(newVal, args[0]) for newVal in val]
            if args is datetime:
                return [_load_single(newVal, datetime) for newVal in val]
            else:
                return val
        elif origin is dict:
            return val
        raise TypeError("Unsupported type")
    elif aType is datetime:
        return datetime.fromisoformat(val)
    elif aType is list:
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
        json.dump(self.clason_dump_d(for_json=True), open(path, mode='w'), indent=indent)

    @classmethod
    def clason_load_d(cls, dictionary: dict):
        if not cls.__dict__.__contains__("__annotations__"):
            raise KeyError("no annotations was found")
        if not isinstance(dictionary, dict):
            raise TypeError("The json is a list not an dict, use clason.loads_many for more than one")
        child = cls()
        for key in cls.__dict__["__annotations__"]:
            typeOfKey: type = cls.__dict__["__annotations__"][key]
            origin: any = typing.get_origin(typeOfKey)
            if not cls.__type_list__.__contains__(key):
                cls.__type_list__[key] = typeOfKey
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
        return child

    @classmethod
    def clason_loads(cls, string: str):
        return cls.clason_load_d(json.loads(string))

    @classmethod
    def clason_load(cls, path: str | PathLike):
        return cls.clason_load_d(json.load(open(path, mode="r")))
