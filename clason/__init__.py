import time
import typing
from datetime import datetime
import json
from os import PathLike



def _convert_single(val, aType, for_json) -> any:
    valueType = type(val)
    if valueType is int and aType is int \
            or valueType is str and aType is str \
            or valueType is float and aType is float \
            or valueType is list and aType is list \
            or valueType is any and aType is any:
        return val
    elif valueType is datetime and aType is datetime:
        if for_json:
            return val.isoformat()
        else:
            return val
    elif valueType is dict:
        new = {}
        for key, value in val.items():
            dictValType = type(value)
            new[key] = _convert_single(value, dictValType, for_json) if dictValType != list else _convert_list_for_dict(value, dictValType, for_json)
        return new
    raise TypeError(f"Type {valueType.__name__} is not the allowed type {aType.__name__} for this value")


def _convert_list_for_dict(cList, aType, for_json) -> any:
    origin = typing.get_origin(aType)
    if origin:
        newType = typing.get_args(aType)[0]
        if origin is list:
            return [_convert_list_for_dict(newList, newType, for_json) for newList in cList]
        return [_convert_single(val, origin, for_json) for val in cList]
    if aType is list:
        return _convert_list_for_dict(cList, aType, for_json)
    else:
        try:
            return [_convert_single(val, aType, for_json) for val in cList]
        except TypeError as e:
            raise TypeError(f"A type from a value in the list is a different as the default type") from None


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
            origin = typing.get_origin(allowedType)
            if origin:
                args = typing.get_args(allowedType)
                if not len(args):
                    raise TypeError("Something is append")
                if origin is list:
                    dictionary[key] = _convert_list_for_dict(value, args[0], for_json)
                elif origin is dict:
                    dictionary[key] = _convert_single(value, args[0], for_json)
                else:
                    if self.__type_checking__:
                        raise TypeError(
                            f"Error in key '{key}', "
                            f"the type of the key is a list but the sup type {args[0].__name__} is not supported"
                        )
            else:
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
                if not isinstance(dictionary[key], typeOfKey) and cls.__type_checking__:
                    raise TypeError(f"Key '{key}' must be a {typeOfKey.__name__} not an {type(dictionary[key]).__name__}")
                if typeOfKey == datetime:
                    child.__dict__[key] = datetime.fromisoformat(dictionary[key])
                if typing.get_origin(typeOfKey):
                    print(origin)
                else:
                    child.__dict__[key] = dictionary[key]
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
