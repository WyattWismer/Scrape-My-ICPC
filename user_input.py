from os import popen, mkdir
from os.path import join, exists, isfile, isdir
import re
import json


class Choices:
    """
    Storage of user choices both as text and as functions.
    By treating everything as a function the interface can be greatly simplified.
    Constant values will become constant functions and this makes it easy to 
    serialize eveyrthing in a human readable (and human editable) format.
    Functions are exposed through the [] operator.
    """
    SAVED_PATH = './choices' 
    raw = {}
    func = {}

    @staticmethod
    def add_choice(name, f, **kwargs):
        """
        Takes in a function to obtain a user choice.
        Runs this function and stores the result.
        """
        text = str(f(**kwargs))
        Choices.raw[name] = text
        Choices.build_choice(name)

    @staticmethod
    def build_choice(name):
        """
        From plain-text at raw[name],
        Constructs lambda func at func[name]
        """
        rfunc = Choices.raw[name]
        rfunc = rfunc.strip().replace("%","%s")
        cnt = rfunc.count('%')
        Choices.func[name] = eval("lambda "+"__x__"*(cnt>0)+": " + rfunc % (("__x__",)*cnt))

    @staticmethod
    def save_choices(fname):
        """
        Saves current raw choices as json
        """
        if not exists(Choices.SAVED_PATH):
            mkdir(Choices.SAVED_PATH)

        location = join(Choices.SAVED_PATH,fname)
        with open(location, 'w') as out:
            json.dump(Choices.raw, out, sort_keys=True, indent=4)

    @staticmethod
    def load_choices(fname):
        """
        Loads raw choices from json and build lambdas
        """
        assert(exists(Choices.SAVED_PATH) and isdir(Choices.SAVED_PATH))
        location = join(Choices.SAVED_PATH, fname)
        assert(exists(location) and isfile(location))
        fp = open(location, 'r')
        Choices.raw = json.load(fp)
        for name in Choices.raw:
            Choices.build_choice(name)


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
    def choose_options_from_list(**kwargs):
        li        = kwargs['options']
        item_name = kwargs['item_name']
        default   = kwargs['default']
        help_text = helpify(kwargs['help_text'])

        if 'plural' in kwargs: plural = kwargs['plural']
        else:                  plural = False 

        # Sort schools
        li.sort()
        # Iterate until valid input
        while True:
            # Display options
            out = ["(%d) %s" % (i, opt) for i,opt in enumerate(li)]
            print_columns(out)
            
            # User choice
            inp = raw_input(
                "#'s of %s" % item_name+
                "(s)"*plural+
                " you would like"+
                " seperated by spaces"*plural+
                ":\n"+
                "DEFAULT: %s\n" % str(default)
            )

            if not inp:
                return default

            inp = inp.strip().split()
            valid = for_all(is_int, inp) and for_all(lambda e: 0 <= int(e) < len(li), inp)

            if is_help(inp) or not valid:
                print help_text
                continue
            
            res = map(lambda i: li[int(i)], inp)

            if plural: return res
            else: return res[0]

    @staticmethod
    def choose_option_from_list(**kwargs):
        return Inputter.choose_options_from_list(plural=False, **kwargs)

    @staticmethod
    def choose_lambda_function(**kwargs):
        flavor    = kwargs['flavor']
        default   = kwargs['default']
        help_text = helpify(kwargs['help_text'])

        while True:
            print "Expression to %s" % flavor
            print "DEFAULT: %s" % default
            
            inp = raw_input()
            # Use default if no input is provided
            if not inp: return default
            
            cnt = inp.count('%')
            if cnt == 0:
                print help_text 
                continue
            
            print #add spacing at end
            return inp

#Helper Methods
def is_help(inp):
    help_cmd="help"
    return (inp == help_cmd
            or inp == help_cmd.upper())

def helpify(help_text):
    longest_line_width = max(map(len, help_text.split('\n')))
    border = '-'*longest_line_width+'\n'
    advice = "\nPress enter for default.\n"
    return "\n%s%s%s%s\n" % (border,help_text,advice,border)
    

def is_int(inp):
    pat = "^[0-9]+$"
    return (re.match(pat, inp) and True) or False


def for_all(p,li):
    """
        return for-all e in li: p[e] = True 
    """
    func_and = lambda a,b: a and b 
    p_li = map(p, li)
    return reduce(func_and, p_li)  


def print_columns(out): 
    n = len(out)
    mx_len = max(map(len, out))
    console_width = get_console_width()
    ncols = console_width/(mx_len+1)
    buf = 2
    fm = "{:<"+str(mx_len+buf)+"s}"

    for i,val in enumerate(out):
        if (i%ncols==0): print "\n",
        print fm.format(val),
    print "\n"


def get_console_width():
    w = 80 #DEFAULT
    try:
        #Currently only support linux
        _,c = popen('stty size').read().split()
        return int(c)
    except:
        pass
    return w




        

