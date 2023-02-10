#!/usr/bin/python3
""""""
import json
import models


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        content = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            f.write(json.dumps(content))

    def reload(self):
        try:
            with open(self.__file_path, "r") as f:
                json_string = f.read()
                if json_string is not None and len(json_string) >= 1:
                    content = json.loads(json_string)
                    for key, value in content.items():
                        class_name, _ = key.strip().split(".")
                        class__ = models.model_factory.get(class_name)
                        self.__objects[key] = class__(**value)
        except IOError:
            pass
