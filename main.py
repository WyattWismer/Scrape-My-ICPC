import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np
from os.path import exists 
from os import listdir


def main():
    # Load data
    dh.load_data(2015,2018)

    # load save build new
    saves = get_saves()
    did_load_save = load_save(saves)
    if not did_load_save:
        build_new_config()

    # Plot data
    pw.add_target_schools(CH.func['target_schools']())


def get_saves():
    """
    Finds name of all saves under choices/
    """
    saves = []
    if exists(CH.SAVED_PATH):
        saves = listdir(CH.SAVED_PATH) 
        saves = filter(lambda s: s.endswith('.json'), saves)
    return saves 

def load_save(saves):
    """
    Loads a particular choices configuration
    """
    save_name = None
    if not saves: return
    save_name = Inp.choose_option_from_list(options=saves,
                                            item_name="save",
                                            help_text=("Enter the # associated with a save to load it. \n"
                                                       "The default option will continue without a save."),
                                            default=None)
    if not save_name == None:
        CH.load_choices(save_name)
        return True
    return False

def build_new_config():
    """
    Builds a choices configuration from user input
    """
    # From ranks of a schools teams for a given year choose the points you would like to graph.
    CH.add_choice(
    'rank_point_chooser',
    Inp.choose_lambda_function,
    flavor="select points to draw",
    help_text=("You are given a list with a schools yearly performance named %.\n\n"
               "For example in a given year you might have % = [3,11,27] for a given school.\n"
               "This would indicate that the school teams had places 3rd, 11th, and 27th.\n"
               "This list is always given in sorted order.\n\n"
               "Write an expression to create the sublist of points you are interested in graphing.\n"
               "For example, to select the best team from % you could write %[0:1]\n"
               "The default option will select all points."),
    default="%[:]")

    # Select which data point you would like to use from a schools performance for a particular year
    CH.add_choice(
    'trend_point_chooser',
    Inp.choose_lambda_function,
    flavor="select point for trend",
    help_text=("You are given a list with a schools yearly performance named %.\n\n"
               "For example in a given year you might have % = [3,11,27] for a given school\n"
               "This would indicate that the school teams had places 3rd, 11th, and 27th.\n"
               "This list is always given in sorted order.\n\n"
               "Write an expression to select the point to use in the trend line.\n"
               "For example, to select the worst team from % you could write %[-1]\n"
               "The default option will select the best team."),
    default="%[0]")

    # Let user choose schools
    all_schools = list(dh.data)
    default_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

    CH.add_choice(
    'target_schools',
    Inp.choose_options_from_list,
    options=all_schools,
    item_name="school",
    help_text=("Ensure the numbers you enter are space seperated.\n"
               "To select the first three schools shown you could enter:\n"
               "0 1 2\n"
               "The default options will select %s" % ', '.join(default_schools)),
    default=default_schools,
    plural=True)

    save_name = raw_input("Name for configuration: ")
    save_name = save_name.strip()

    if save_name:
        if not save_name.endswith(".json"): save_name += ".json"
        CH.save_choices(save_name)


if __name__ == "__main__":
    main()
