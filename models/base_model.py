#!/usr/bin/python3
"""
"""
import copy
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["updated_at", "created_at"]:
                        setattr(
                            self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                        )
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self) -> str:
        """ """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """ """
        models.storage.save()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """ """
        attrs = copy.deepcopy(self.__dict__)
        attrs["created_at"] = self.created_at.isoformat()
        attrs["updated_at"] = self.updated_at.isoformat()
        attrs["__class__"] = self.__class__.__name__

        return attrs
