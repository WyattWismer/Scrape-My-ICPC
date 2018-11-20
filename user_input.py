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
    def choose_options_from_list(li, item_name="option"):
        while True:
            # Display options
            out = ["(%d) %s" % (i, opt) for i,opt in enumerate(li)]
            print_columns(out,2)


            # User choice
            inp = raw_input("Please type the %s(s) you would like seperated by spaces.\n[[ PRESS ENTER FOR DEFAULT  ]]\n: " % item_name)
            if not inp: return

            inp = inp.strip().split()
            valid = for_all(is_int, inp) and for_all(lambda e: 0 <= int(e) < len(li), inp)

            if not valid:
                print "Your input must be some number of space seperated integers"
                continue
            
            return map(lambda i: li[int(i)], inp)

    @staticmethod
    def choose_lambda_function(flavor, example, default):
        while True:
            print "Please write a python expression to %s." % flavor
            print "Use the symbol % to represent the provided value."
            print "Example: %s" % example
            print "[[ PRESS ENTER FOR DEFAULT  %s  ]]" % default
            
            inp = raw_input()
            if not inp: return
            
            cnt = inp.count('%')
            if cnt == 0:
                print "Your input must be a valid python expression and contain %"
                continue

            inp = inp.strip().replace("%","%s")
            
            return eval("lambda __x__: " + inp % (("__x__",)*cnt))


def is_int(inp):
    pat = "^[0-9]+$"
    return (re.match(pat, inp) and True) or False


def for_all(p,li):
    """
        for-all e in li: p[e] = True 
    """
    func_and = lambda a,b: a and b 
    p_li = map(p, li)
    return reduce(func_and, p_li)  

        
def print_columns(out, ncols): 
    n = len(out)
    mx_len = max(map(lambda x: len(x), out))
    fm = "{:<"+str(mx_len)+"s}"

    for i,val in enumerate(out):
        if (i%3==0): print "\n",
        print fm.format(val),
    print 




        

