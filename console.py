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
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            b = models.BaseModel()
            b.save()
            print(b.id)

    def do_show(self, line):
        args = self.parse(line)
        if not args[0]:
            print("** class name missing **")
        elif len(args) <= 1:
            print("** instance id missing **")
        elif args[0] != "BaseModel":
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
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            objs = models.storage.all()
            obj = objs.pop(f"{args[0]}.{args[1]}", None)
            if not obj:
                print("** no instance found **")
            models.storage.save()

    def do_all(self):
        ...

    def do_update(self):
        ...

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
