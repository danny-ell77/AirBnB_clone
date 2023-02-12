#!/usr/bin/python3
""" A module that contains the BaseModel Class
"""
import copy
from datetime import datetime
from uuid import uuid4

import models


class BaseModel:
    """The Base Model that manages all the attributes for other models
    Instance Attributes:
        id (str) : an identifier for the model using uuid
        assigned when an instance is created
        updated_at (datetime) : The date/time the model is updated
        created_at (datetime) : The date/time the model is created
    """

    def __init__(self, *args, **kwargs):
        """Initializes the instance attributes
        Args:
            id (str) :
            updated_at (datetime) : The date/time the model is updated
            created_at (datetime) : The date/time the model is created
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "updated_at" or key == "created_at":
                    setattr(
                        self, key, datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    )
                elif key != "__class__":
                    setattr(self, key, value)

        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self) -> str:
        """A unique string representation for the class"""
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
