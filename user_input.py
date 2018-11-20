import re

class Choices: pass

class Inputter:
    """
    Used to request input from the user
    """
    @staticmethod
    def choose_option_from_dict(to_full_opt):
        while True:
            # Display options
            for option in to_full_opt:
                full_option = to_full_opt[option]
                print "(%s) %s" % (option, full_option) 
            # User choice
            inp = raw_input("Please type the option you would like: ")
            inp = inp.strip()
            if inp in to_full_opt: return to_full_opt[option]
            print "This is not a valid option"

    @staticmethod
    def choose_option_from_list(li):
        while True:
            # Display options
            for i,option in enumerate(li):
                print "(%d) %s" % (i, option) 

            # User choice
            inp = raw_input("Please type the option you would like: ")
            inp = inp.strip()

            if is_int(inp):
                choice = int(inp)
                if 0<= choice < len(li):
                    return li[int(inp)]
            print "This is not a valid option"

    @staticmethod
    def get_lambda_function(flavor, example, default):
        while True:
            print "Please write a python expression to %s." % flavor
            print "Use the symbol % to represent your value."
            print "Example: %s" % example
            print "[[ PRESS ENTER FOR DEFAULT  %s  ]]" % default
            
            inp = raw_input()
            if not inp: return

            if "%" not in inp:
                print "Your input must be a valid python expression and contain %"
                continue

            inp = inp.strip().replace("%","%s")
            
            return eval("lambda __x__: " + inp % "__x__")


def is_int(inp):
    pat = "^[0-9]+$"
    return re.match(pat, inp)

        





        

