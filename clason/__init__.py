import json
from os import PathLike


class Clason:

    def clason_dump(self, path: str | PathLike):
        pass

    def clason_dumps(self) -> str:
        pass

    @classmethod
    def clason_loads(cls, string: str):
        if not cls.__dict__.__contains__("__annotations__"):
            raise KeyError("no annotations was found")
        data = json.loads(string)
        if not isinstance(data, dict):
            raise TypeError("The json is a list not an dict, use clason.loads_many for more than one")
        child = cls()
        for key in cls.__dict__["__annotations__"]:
            typeOfKey: type = cls.__dict__["__annotations__"][key]
            if data.__contains__(key):
                if not isinstance(data[key], typeOfKey):
                    raise TypeError(f"Key '{key}' must be a {typeOfKey.__name__} not an {type(data[key]).__name__}")
                child.__dict__[key] = data[key]
            else:
                try:
                    cls.__dict__[key]
                except KeyError as e:
                    raise KeyError(f"Key '{key}' has no default value, and no value data was found") from None
                else:
                    value = cls.__dict__[key]
                    if not isinstance(value, typeOfKey):
                        raise TypeError(
                            f"The default value from key '{key}' must be a {typeOfKey.__name__} "
                            f"not an {type(value).__name__}"
                        )
                    child.__dict__[key] = value
        return child

    @classmethod
    def clason_load(cls, path: str | PathLike):
        pass

    #https://stackoverflow.com/questions/13402847/how-to-watch-for-a-variable-change-in-python-without-dunder-setattr-or-pdb
