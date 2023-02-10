#!/usr/bin/python3
""""""
import cmd
import models


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.action_mapper = {
            "all": self.do_all,
            "count": self.do_count,
            "save": self.do_create,
            "update": self.do_update,
            "destroy": self.do_destroy,
        }

    def parse_args(self, args):
        class_name = args[0]
        instance_id = args[1] if len(args) > 1 else None
        attribute = args[2] if len(args) > 2 else None
        value = args[3] if len(args) > 3 else None
        return class_name, instance_id, attribute, value

    def parse(self, line):
        return line.strip().split(" ")

    def default(self, line: str) -> None:
        args = line.strip().split(".", maxsplit=2)
        class_name = args[0]
        action = (
            args[1][:-2] if len(args) > 1 else None
        )  # use regex in case of parameters
        command = self.action_mapper.get(action)
        if command:
            command(class_name)
        else:
            print("** command doesn't exist **")

    def do_create(self, line):
        args = self.parse(line)
        class_name = self.parse_args(args)[0]
        if not class_name:
            print("** class name missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        else:
            b = models.model_factory(class_name)
            b.save()
            print(b.id)

    def do_show(self, line):
        args = self.parse(line)
        class_name, instance_id = self.parse_args(args)[:2]
        if not class_name:
            print("** class name missing **")
        elif not instance_id:
            print("** instance id missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        else:
            objs = models.storage.all()
            obj = objs.get(f"{class_name}.{instance_id}")
            if obj:
                print(obj)
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        args = self.parse(line)
        class_name, instance_id = self.parse_args(args)[:2]
        if not class_name:
            print("** class name missing **")
        elif not instance_id:
            print("** instance id missing **")
        elif class_name not in models.mapper.keys():
            print("** class doesn't exist **")
        else:
            objs = models.storage.all()
            obj = objs.pop(f"{class_name}.{instance_id}", None)
            if not obj:
                print("** no instance found **")
            else:
                models.storage.save()

    def do_all(self, line):
        args = self.parse(line)
        class_name = self.parse_args(args)[0]
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

    def do_count(self):
        ...

    def do_update(self, line):
        args = self.parse(line)
        class_name, instance_id, attribute, value = self.parse_args(args)

        if not class_name:
            print("** class name missing **")
        elif not instance_id:
            print("** instance id missing **")
        elif not attribute:
            print("** attribute name missing **")
        elif not value:
            print("** value missing **")
        else:
            if class_name not in models.mapper.keys():
                print("** class doesn't exist **")
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

    def emptyline(self) -> bool:
        pass

    def do_q(self, args):
        self.do_quit(args)

    def do_quit(self, args):
        """Quit the calculator"""
        return True

    def do_EOF(self, args):
        """exit after an End of FIle"""
        print("")
        return True

    def do_help(self, line):
        """Display custom help message"""
        print("Type 'hello' to say hello, 'quit' to quit")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
