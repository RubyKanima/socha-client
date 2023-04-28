from socha import *
from tabulate import tabulate
from typing import List
import logging

def tabulate_moves(list: List[Move]):
    table = [["Team", "From Cart.", "To Cart."]]
    for each in list:
        if each.from_value:
            from_string = str(each.from_value.to_cartesian().x)+", "+str(each.from_value.to_cartesian().y)
        else:
            from_string = "None"
        to_string = str(each.to_value.to_cartesian().x)+", "+str(each.to_value.to_cartesian().y)
        table.append([str(each.team_enum.name),from_string, to_string])
    logging.info("\n" + tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

