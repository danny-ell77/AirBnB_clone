#!/usr/bin/python3
"""
Contains the FileStorage class
"""
import json

import models


class FileStorage:
    """
    The FileStorage engine that manages persisted data
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns all the saved objects
        """
        return self.__objects

    def new(self, obj):
        """
        Assigns a new record of an instance to the class
        Args:
        obj(BaseModel): An instance of BaseModel
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Persists the model's attributes to the file system in JSON
        """
        content = {k: obj.to_dict() for k, obj in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            f.write(json.dumps(content))

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists;
        otherwise, do nothing. If the file doesn't exist,
        no exception should be raised)
        """
        try:
            with open(self.__file_path, "r") as f:
                json_string = f.read()
                if json_string is not None and len(json_string) >= 1:
                    content = json.loads(json_string)
                    for key, value in content.items():
                        class_name, _ = key.strip().split(".")
                        class__ = models.mapper.get(class_name)
                        self.__objects[key] = class__(**value)
        except IOError:
            pass
