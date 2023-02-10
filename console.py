#!/usr/bin/python3
""""""
import cmd
import models


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def parse(self, line):
        return line.strip().split(" ")

    def do_create(self, line):
        args = self.parse(line)
        if not args[0]:
            print("** class name missing **")
        elif args[0] not in models.model_factory.keys():
            print("** class doesn't exist **")
        else:
            b = models.model_factory.get(args[0])()
            b.save()
            print(b.id)

    def do_show(self, line):
        args = self.parse(line)
        if not args[0]:
            print("** class name missing **")
        elif len(args) <= 1:
            print("** instance id missing **")
        elif args[0] not in models.model_factory.keys():
            print("** class doesn't exist **")
        else:
            objs = models.storage.all()
            obj = objs.get(f"{args[0]}.{args[1]}")
            if obj:
                print(obj)
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        args = self.parse(line)
        if not args[0]:
            print("** class name missing **")
        elif len(args) <= 1:
            print("** instance id missing **")
        elif args[0] not in models.model_factory.keys():
            print("** class doesn't exist **")
        else:
            objs = models.storage.all()
            obj = objs.pop(f"{args[0]}.{args[1]}", None)
            if not obj:
                print("** no instance found **")
            else:
                models.storage.save()

    def do_all(self, line):
        args = self.parse(line)
        objs = models.storage.all()
        if args[0]:
            if args[0] == "BaseModel":
                print(
                    [
                        str(value)
                        for key, value in objs.items()
                        if args[0] == key.split(".")[0]
                    ]
                )
            else:
                print("** class doesn't exist **")
        else:
            print([str(obj) for obj in objs.values()])

    def do_update(self, line):
        args = self.parse(line)
        class_name = args[0]
        instance_id = args[1] if len(args) > 1 else None
        attribute = args[2] if len(args) > 2 else None
        value = args[3] if len(args) > 3 else None

        if not class_name:
            print("** class name missing **")
        elif not instance_id:
            print("** instance id missing **")
        elif not attribute:
            print("** attribute name missing **")
        elif not value:
            print("** value missing **")
        else:
            if class_name not in models.model_factory.keys():
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
