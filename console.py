#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re

import models


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "

    def __init__(self, *args, **kwargs) -> None:
        """Initializer for HBNBCommand"""
        super().__init__(*args, **kwargs)

        self.action_mapper = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "save": self.do_create,
            "update": self.do_update,
            "destroy": self.do_destroy,
        }

    def _parse_args(self, args):
        """parse the args list into arguments"""
        class_name = args[0]
        instance_id = args[1] if len(args) > 1 else None
        attribute = args[2] if len(args) > 2 else None
        value = args[3] if len(args) > 3 else None
        return class_name, instance_id, attribute, value

    def _parse(self, line):
        """split the line by spaces"""
        return line.strip().split(" ")

    def _handle_update(self, line, command, class_name, identifier, attrs):
        try:
            attrs_parsed = eval(attrs)
            if type(attrs_parsed) is not dict:
                raise Exception()
            for key, value in attrs_parsed.items():
                self._call_command(
                    line,
                    command,
                    class_name,
                    identifier,
                    attrs=f"{key} {value}"
                )
        except Exception:
            print(f"*** Unknown syntax: {line}")

    def _call_command(self, line, command, class_name, identifier, attrs):
        new_line = f"{class_name} {identifier} {attrs}"
        if command := self.action_mapper.get(command):
            command(new_line)
        else:
            print(f"*** Unknown syntax: {line}")

    def default(self, line: str) -> None:
        """Default behavior for cmd module when input is invalid"""
        identifier = ""
        attrs = ""

        class_name, *action = line.strip().split(".", maxsplit=2)
        action = "".join(action)
        command, *args = action.split("(")
        args = "".join(args)

        # Match pattern 1: (<id>)
        pattern1 = re.compile(r"\s*\"*(\w+-\w+-\w+-\w+-\w+)\"*\s*\)$")
        # Match pattern 2: (<id>, <attribute name>, <attribute value>)
        pattern2 = re.compile(
            r"\s*\"*(\w+-\w+-\w+-\w+-\w+)\"*\s*,\s*\"(\w+)\",\s*\"*(\w+)\"*\)$"
        )
        # Match pattern 3: (<id>, <dictionary representation>)
        pattern3 = re.compile(r"\s*\"*(\w+-\w+-\w+-\w+-\w+)\"*,\s*(\{.*\})\)$")
        match = (
            re.match(pattern1, args)
            or re.match(pattern2, args)
            or re.match(pattern3, args)
        )
        if match:
            identifier = match.group(1)
            attrs = " ".join(match.groups()[1:]) if match.lastindex > 1 else ""
            if len(attrs) > 0 and attrs[0] == "{":
                return self._handle_update(
                    line, command, class_name, identifier, attrs
                )
        elif args != ")":
            print(f"*** Unknown syntax: {line}")
            return
        self._call_command(line, command, class_name, identifier, attrs)

    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args = self._parse(line)
        class_name = self._parse_args(args)[0]
        if not class_name:
            print("** class name missing **")
        elif class__ := models.mapper.get(class_name):
            b = class__()
            b.save()
            print(b.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = self._parse(line)
        class_name, instance_id, _, _ = self._parse_args(args)
        if not class_name:
            print("** class name missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")
        else:
            objs = models.storage.all()
            obj = objs.get(f"{class_name}.{instance_id}")
            if obj:
                print(obj)
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        args = self._parse(line)
        class_name, instance_id, _, _ = self._parse_args(args)
        if not class_name:
            print("** class name missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")

        else:
            objs = models.storage.all()
            obj = objs.pop(f"{class_name}.{instance_id}", None)
            if not obj:
                print("** no instance found **")
            else:
                models.storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""

        args = self._parse(line)
        class_name = self._parse_args(args)[0]
        objs = models.storage.all()
        if class_name:
            if class_name in models.mapper.keys():
                print(
                    [
                        str(value)
                        for key, value in objs.items()
                        if class_name == key.split(".")[0]
                    ]
                )
            else:
                print("** class doesn't exist **")
        else:
            print([str(obj) for obj in objs.values()])

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = self._parse(line)
        class_name = self._parse_args(args)[0]
        objs = models.storage.all()
        if not class_name:
            print("** class name missing **")
        elif class_name not in models.mapper.keys():
            print(0)
        else:
            count = len(
                [
                    str(value)
                    for key, value in objs.items()
                    if class_name == key.split(".")[0]
                ]
            )
            print(count)

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args = self._parse(line)
        class_name, instance_id, attribute, value = self._parse_args(args)

        if not class_name:
            print("** class name missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")
        elif not attribute:
            print("** attribute name missing **")
        elif not value:
            print("** value missing **")
        else:
            objs = models.storage.all()
            obj = objs.get(f"{class_name}.{instance_id}")
            if obj:
                attr_type = type(getattr(obj, attribute, None))
                if attr_type in {int, str, float}:
                    setattr(obj, attribute, attr_type(value))
                obj.save()
            else:
                print("** no instance found **")

    def do_help(self, arg):
        '''
        Documented
        commands(type help < topic >):
        == == == == == == == == == == == == == == == == == == == ==
        EOF help quit save show all destroy update count
        '''
        super().do_help(arg)

    def emptyline(self) -> bool:
        """Do nothing upon receiving an empty line."""
        pass

    def do_quit(self, args):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, args):
        """EOF signal to exit the program."""
        print("")
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()


# def default(self, line: str) -> None:
#     """Default behavior for cmd module when input is invalid"""
#     identifier = ""
#     attrs = ""
#     value = ""

#     class_name, *action = line.strip().split(".", maxsplit=2)
#     action = "".join(action)
#     command, *args = action.split("(")
#     args = "".join(args)

#     # Match pattern 1: (<id>)
#     pattern1 = re.compile(r"\s*\"(\w+-\w+-\w+-\w+-\w+)\"\s*\)$")
#     # Match pattern 2: (<id>, <attribute name>, <attribute value>)
#     pattern2 = re.compile(
#         r"\s*\"(\w+-\w+-\w+-\w+-\w+)\"\s*,\s*\"(\w+)\",\s*\"(\w+)\"\)$"
#     )
#     # Match pattern 3: (<id>, <dictionary representation>)
#     pattern3 = re.compile(r"\s*\"(\w+-\w+-\w+-\w+-\w+)\",\s*(\{.*\})\)$")
#     match = (
#         re.match(pattern1, args)
#         or re.match(pattern2, args)
#         or re.match(pattern3, args)
#     )
#     if match:
#         identifier = match.group(1)
#         attrs = " ".join(match.groups()[1:]) if match.lastindex > 1 else ""
#         print(type(attrs))

#         if attrs[0] == "{":
#             try:
#                 attrs_type = eval(attrs)
#                 if type(attrs_type) is not dict:
#                     raise Exception()
#                 for key, value in attrs_type.items():
#                     self._call_command(
#                         line, command, class_name, identifier, key, value
#                     )
#             except Exception:
#                 print(f"*** Unknown syntax: {line}")
#                 return

#     elif args != ")":
#         print(f"*** Unknown syntax: {line}")
#     self._call_command(line, command, class_name, identifier, attrs, value)
