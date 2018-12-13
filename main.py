import plot_wrapper as pw
import data_handler as dh
from user_input import Inputter as Inp
from user_input import Choices as CH
import numpy as np
from os.path import exists 
from os import listdir


# get list of saves
saves = None
if exists(CH.SAVED_PATH):
    saves = listdir(CH.SAVED_PATH) 
    saves = filter(lambda s: s.endswith('.json'), saves)

# continue or load save 
save_name = None
if saves:
    save_name = Inp.choose_option_from_list(options=saves,
                                            item_name="save",
                                            default=None)
    if not save_name == None:
        CH.load_choices(save_name)

# Load data
dh.load_data(2015,2018)


if not save_name:
    # From the ranks of a schools teams for a given year choose the points you would like to graph.
    CH.add_choice(
    'rank_point_chooser',
    Inp.choose_lambda_function,
    flavor=("choose the points you would like to graph given the "
    "ranks of all of a school's teams for a given year"),
    example="%[0:1] would select only the first point.",
    default="%[:]"             
    )

    # Select which data points you would like to use from a schools performance for a particular year
    CH.add_choice(
    'trend_point_chooser',
    Inp.choose_lambda_function,
    flavor="select which data point you would like to use in the trend",
    example="%[-1] would select only the last point.",
    default="%[0]"
    )

    # Let user choose schools
    all_schools = list(dh.data)
    default_schools = ['McMaster University', 'University of Waterloo', 'University of Toronto']

    CH.add_choice(
    'target_schools',
    Inp.choose_options_from_list,
    options=all_schools,
    item_name="school",
    default=default_schools,
    plural=True
    )

    save_name = raw_input("Please enter a name for this configuration: ")
    save_name = save_name.strip()

    if save_name:
        if not save_name.endswith(".json"): save_name += ".json"
        CH.save_choices(save_name)



# Plot data
pw.add_target_schools(CH.func['target_schools']())


