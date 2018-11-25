from os import listdir
from os import popen
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
        text = f(**kwargs)
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
        sm = staticmethod
        Choices.func[name] = sm(eval("lambda __x__: " + rfunc % (("__x__",)*cnt)))

    @staticmethod
    def save_choices(fname):
        """
        Saves current raw choices as json
        """
        if not exists(SAVED_PATH):
            os.mkdir(SAVED_PATH)

        location = join(SAVED_PATH,fname)
        with open(location, 'w') as out:
            json.dump(Choices.raw, out, sort_keys=True, indent=4)

    @staticmethod
    def load_choices(fname):
        """
        Loads raw choices from json and build lambdas
        """
        assert(exists(SAVED_PATH) and isdir(SAVED_PATH))
        location = join(SAVED_PATH, fname)
        assert(exists(location) and isfile(location))
        raw = json.load(location)
        for name in raw: build_choice(name)


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
    def choose_options_from_list(li, item_name="option"):
        # Sort schools
        li.sort()
        # Iterate until valid input
        while True:
            # Display options
            out = ["(%d) %s" % (i, opt) for i,opt in enumerate(li)]
            print_columns(out)
            
            # User choice
            inp = raw_input("Please type the %s(s) you would like seperated by spaces:\n"
                            "[[ PRESS ENTER FOR DEFAULT  ]]\n " % item_name)
            if not inp: return

            inp = inp.strip().split()
            valid = for_all(is_int, inp) and for_all(lambda e: 0 <= int(e) < len(li), inp)

            if not valid:
                print "Your input must be some number of space seperated integers"
                continue
            
            return map(lambda i: li[int(i)], inp)

    @staticmethod
    def choose_lambda_function(**kwargs):
        # Check for required keys
        assert('flavor' in kwargs)
        assert('example' in kwargs)
        assert('default' in kwargs)

        flavor = kwargs['flavor']
        example = kwargs['example']
        default = kwargs['default']

        while True:
            print "Please write a python expression to %s." % flavor
            print "Use the symbol % to represent the provided value."
            print "Example: %s" % example
            print "[[ PRESS ENTER FOR DEFAULT  %s  ]]" % default
            
            inp = raw_input()
            # Use default if no input is provided
            if not inp: return default
            
            cnt = inp.count('%')
            if cnt == 0:
                print "Your input must be a valid python expression and contain %"
                continue
            
            print #add spacing at end
            return inp


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




        

