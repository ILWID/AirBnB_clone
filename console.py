#!/usr/bin/python3
"""
    This module contains the entry point of the command interpreter
    for this project
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ The command interpreter """

    prompt = "(hbnb) "
    models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        """ Executes when the line is empty """

        pass

    def complete_create(self, text, line, begidx, endidx):
        """ helps to complete class names """

        if not text:
            complete_list = self.models.keys()[:]
        else:
            complete_list = [i for i in self.models.keys()
                             if i.startswith(text)]

        return complete_list

    def do_create(self, line):
        """
            Creates a new instance of class name given
            Usage: create <model>
        """

        try:
            name, __ = line.split(" ")
        except ValueError:
            name = line

        if not name:
            print("** class name missing **")
        elif name not in HBNBCommand.models:
            print("** class doesn't exist **")
        else:
            cls = HBNBCommand.models[name]
            new = cls()
            new.save()

            print(new.id)

    def count(self, line):
        """
            Counts instances and print result
            Usage: count <model>
        """

        try:
            name, __ = line.split(" ")
        except ValueError:
            name = line

        if not name:
            print("** class name missing **")
        elif name not in HBNBCommand.models:
            print("** class doesn't exist **")
        else:
            count = 0
            all_objs = storage.all()

            for key, val in all_objs.items():
                if val.__class__.__name__ == name:
                    count += 1

            print(count)

    def do_show(self, line):
        """
            Prints the string representation of an instance based
            on the class name and id
            Usage: show <model> <id>
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        for i in range(1, len(args)):
            if args[i]:
                id = args[i]
                break
        else:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                print(obj)
                return
        print("** no instance found **")

    def do_destroy(self, line):
        """
            Deletes an instance based on the class name and id
            Usage: destroy <model> <id>
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        for i in range(1, len(args)):
            if args[i]:
                id = args[i]
                break
        else:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                del obj
                del storage._FileStorage__objects[obj_id]
                storage.save()
                return

        print("** no instance found **")

    def do_all(self, line):
        """
            Prints all string representation of all instances
            based or not on the class name
        """

        all_objs = storage.all()
        all_objs_ptr = []

        try:
            name, __ = line.split(" ")
        except ValueError:
            name = line

        if name:
            if name not in HBNBCommand.models:
                print("** class doesn't exist **")
                return

            for obj_id, obj in all_objs.items():
                if obj.__class__.__name__ == name:
                    all_objs_ptr.append(obj.__str__())
        else:
            for obj_id, obj in all_objs.items():
                all_objs_ptr.append(obj.__str__())

        print(all_objs_ptr)

    def do_update(self, line):
        """
            Updates an instance based on class name and id by
            adding or updating attributes
            Usage: update <model> <id> <attribute> "<value>"
        """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        model = args[0]
        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        i = 1
        while i < len(args):
            if args[i]:
                id = args[i]
                break
            i += 1
        else:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        id_exist = False
        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                id_exist = True

        if not id_exist:
            print("** no instance found **")
            return

        i += 1
        while i < len(args):
            if args[i]:
                attr_name = args[i]
                break
            i += 1
        else:
            print("** attribute name missing **")
            return

        attr_vals = []
        i += 1
        while i < len(args):
            if args[i]:
                attr_vals.append(args[i])
                break
            i += 1
        else:
            print("** value missing **")
            return

        if attr_vals[0][-1] != '"':
            i += 1
            while i < len(args):
                attr_vals.append(args[i])
                if args[i][-1] == '"':
                    break
                i += 1

        attr_val = " ".join(attr_vals)

        for obj_id, obj in all_objs.items():
            if id == obj.id and obj.__class__.__name__ == model:
                value = "".join(attr_val.split('"'))
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                setattr(obj, attr_name, value)
                obj.save()
                break

    def update_dict(self, line, dict_):
        """ Updates from dictionary representation """

        args = line.split(" ")
        model = args[0]

        if model not in HBNBCommand.models:
            print("** class doesn't exist **")
            return

        i = 1
        while i < len(args):
            if args[i]:
                id = args[i]
                break
            i += 1
        else:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        for obj_id, obj in all_objs.items():
            if obj.id == id and obj.__class__.__name__ == model:
                for key, val in dict_.items():
                    setattr(obj, key, val)
                return

        print("** no instance found **")

    def update(self, line):
        """ implements the update command """

        attr = ""
        command = ""

        # check for seperator "," and add all chars after to attr
        # attr will be used to check the type of update called
        # ie string or update with dict
        found_sep = False
        for ch in line:
            if not found_sep and ch == "{":
                break
            if found_sep:
                attr += ch
            else:
                if ch == '"' or ch == ",":
                    pass
                else:
                    command += ch
            if ch == ",":
                found_sep = True

        if attr:
            attr = eval(attr)

        if type(attr) is dict:
            self.update_dict(command, attr)
        else:
            com_str = "{}".format(command)
            if type(attr) is tuple:
                i = 0
                while i < 2:
                    com_str += " "
                    if i == 1:
                        com_str += '"'
                    com_str += attr[i]
                    i += 1
                com_str += '"'
            elif type(attr) is str:
                com_str += " {}".format(attr)
            self.do_update(com_str)

    def default(self, line):
        """ Use default to implement function-like commands"""

        command_dict = {
            "all": self.do_all,
            "count": self.count,
            "show": self.do_show,
            "destroy": self.do_destroy,
        }

        if line[-1] != ")":
            print("*** Unknown syntax: {}".format(line))
            return

        try:
            model, command = line.split(".", 1)
        except ValueError:
            print("*** Unknown syntax: {}".format(line))
            return

        com_str = "{} ".format(model)
        try:
            comm, command = command.split("(", 1)
        except ValueError:
            print("*** Unknown syntax: {}".format(line))
            return

        command = command[:-1]

        # calls a different function for update command and return
        if comm == "update":
            self.update(com_str + command)
            return

        for ch in command:
            if ch == '"' or ch == ",":
                continue
            com_str += ch

        if comm in command_dict:
            command_func = command_dict[comm]
            command_func(com_str)
        else:
            print("*** Unknown syntax: {}".format(line))

    def do_quit(self, line):
        """ Quit command to exit the program """

        return True

    do_EOF = do_quit
    complete_destroy = complete_create
    complete_show = complete_create
    complete_all = complete_create
    complete_update = complete_create


if __name__ == "__main__":
    HBNBCommand().cmdloop()
