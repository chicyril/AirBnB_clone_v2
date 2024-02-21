#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models import storage


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = storage.cls_ref()
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)', end=" ")

    def precmd(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in self.__class__.dot_cmds:
                raise Exception
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, line):
        """Exits the command interpreter."""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("\nquit:\t quit")
        print("\tExit the command interpreter.\n")

    def do_EOF(self, line):
        """Exit the program. same as quit.
        Usage: ctr D
        """
        print()
        return True

    def emptyline(self):
        """Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        _cls = arg_list[0]
        if _cls not in self.__class__.classes:
            print("** class doesn't exist **")
            return
        kwargs = {}
        for kwarg in arg_list[1:]:
            kwrd, kval = kwarg.split('=')
            kval = eval(kval)
            if type(kval) is str:
                kval = kval.replace('_', ' ').replace('"', '\\"')
            kwargs[kwrd] = kval
        new_instance = self.__class__.classes[_cls](**kwargs)
        print(new_instance.id)
        new_instance.save()

    def help_create(self):
        """Display help for `create` command"""
        print('\ncreate:\t create <class name>')
        print('\tCreate new instance of specified class.\n')

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        _cls = new[0]
        _id = new[2]

        if _id and ' ' in _id:
            _id = _id.partition(' ')[0]

        if not _cls:
            print("** class name missing **")
            return

        if _cls not in self.__class__.classes:
            print("** class doesn't exist **")
            return

        if not _id:
            print("** instance id missing **")
            return

        key = _cls + "." + _id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Display help for `show` command"""
        print("\nshow:\t show <class name> <instance id>")
        print("\tPrint the string representation of instance with the "
              "provided class name and id\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        _cls = new[0]
        _id = new[2]
        if _id and ' ' in _id:
            _id = _id.partition(' ')[0]

        if not _cls:
            print("** class name missing **")
            return

        if _cls not in self.__class__.classes:
            print("** class doesn't exist **")
            return

        if not _id:
            print("** instance id missing **")
            return

        key = _cls + "." + _id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Display help for `destroy` command."""
        print('\ndestroy: destroy <class name> <instance id>')
        print('\tDelete instance with the specified class name and id.\n')

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]
            if args not in self.__class__.classes:
                print("** class doesn't exist **")
                return
            clss = self.__class__.classes[args]
            for k, v in storage.all(clss).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """Display help for `all` command."""
        print('\nall:\t all [<class name>]')
        print('\tPrint string representation of all created instance(s), '
              'or instance(s) of a specified class\n')

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Help doccumment for count command."""
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:
            print("** class name missing **")
            return
        if c_name not in self.__class__.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        if key not in storage.all():
            print("** no instance found **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            if not att_name and args[0] != ' ':
                att_name = args[0]

            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        _obj = storage.all()[key]

        for i, att_name in enumerate(args):
            if (i % 2 == 0):
                att_val = args[i + 1]
                if not att_name:
                    print("** attribute name missing **")
                    return

                if not att_val:
                    print("** value missing **")
                    return

                if att_name in self.__class__.types:
                    att_val = self.__class__.types[att_name](att_val)

                _obj.__dict__.update({att_name: att_val})

        _obj.save()

    def help_update(self):
        """Diplay help for `update` command."""
        print("\nupdate:\t update <class name> <id> <attr name> <attr val>")
        print("\tUpdate an attribute of a specified instance of a class "
              "or set the attribute, with the provided val.\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
