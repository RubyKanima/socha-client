from socha import *
from tabulate import tabulate
from typing import List
import logging

from extention.triangles import *


colors = {
    "reset": "\033[00m",
    "spots": {
        "white":    "\033[37m",
        "red":      "\033[31m",
        "black":    "\033[30m",
        "yellow":      "\033[93m",
    }
}

def print_common(board: Board, team: str):
    if team == 'ONE':
        own_pretty_print_custom(board," ", "⛇", "ඞ")
    else:
        own_pretty_print_custom(board," ", "ඞ", "⛇")

def tabulate_moves(move_list: List[Move]):
    table = [["Team", "From Cart.", "To Cart."]]
    for each in move_list:
        if each.from_value:
            from_string = str(each.from_value.to_cartesian().x)+", "+str(each.from_value.to_cartesian().y)
        else:
            from_string = "None"
        to_string = str(each.to_value.to_cartesian().x)+", "+str(each.to_value.to_cartesian().y)
        table.append([str(each.team_enum.name),from_string, to_string])
    logging.info("\n" + tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

def tabulate_group(group: Group):
    table = [["hash", "root", "fish", "inters", "spot", "group"]]
    for key in group.group:
        tile = group.group[key]
        enum = tile.penguin.team_enum.name if tile.penguin else None
        table.append([key, tile.root, enum or tile.fish, tile.inters, tile.spot, tile.group])
    logging.info("\n" + tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

def print_group_board(board: Board, group: Group, team: str):
    print("- - - - - - - - - - - - - - - - -")
    for y in range(8):
        if y % 2 == 1:
            print("  ", end="")
        for x in range(8):
            coord = CartesianCoordinate(x, y).to_hex()
            hashed = own_hash(coord)
            if hashed in group.group:
                num = len(group.group) - list(group.group.keys()).index(hashed)
                if num > 9: print(f" {num} ", end="")
                if num < 10: print(f" 0{num} ", end="")
            else:
                this_field = board.get_field(coord)
                if this_field.is_occupied():
                    if this_field.penguin.team_enum.name == team:
                        print(" ⛇  ", end="")
                    else:
                        print(" ඞ  ", end="")
                elif this_field.fish == 0:
                    print("    ", end="")
                else:
                    print(" -- ", end="")
        print()
    print("- - - - - - - - - - - - - - - - -")

def print_group_board_color(board: Board, group: Group, team: str):
    print("- - - - - - - - - - - - - - - - -")
    for y in range(8):
        if y % 2 == 1:
            print("  ", end="")
        for x in range(8):
            coord = CartesianCoordinate(x, y).to_hex()
            hashed = own_hash(coord)
            if hashed in group.group:
                color = colors["spots"][group.group[hashed].spot]
                print(color + f" {group.group[hashed].fish} ", end=" ")
                print(colors["reset"], end="")
            else:
                this_field = board.get_field(coord)
                if this_field.is_occupied(): 
                    if this_field.penguin.team_enum.name == team:
                        print(" ⛇ ", end=" ")
                    else:
                        print(" ඞ ", end=" ")
                elif this_field.fish == 0:
                    print("   ", end=" ")
                else:
                    print(" - ", end=" ")
        print()
    print("- - - - - - - - - - - - - - - - -")

def print_moves_board_custom(board: Board, move_list: List[Move], empty_char = " ", char = "-", one_char = None, two_char = None):
    print("- - - - - - - - - - - - - - - - -")
    move_list_to = [each.to_value for each in move_list]
    for i, row in enumerate(board.board):
        if (i + 1) % 2 == 0:
            print("  ", end="")
        for field in row:
            if field.coordinate in move_list_to:
                print(f" {field.fish} ", end=" ")
            elif field.is_occupied():
                if one_char and field.get_team().value == "ONE":
                    print(f" {one_char[0]} ", end=" ")
                elif two_char and field.get_team().value == "TWO":
                    print(f" {two_char[0]} ", end=" ")
                else:
                    print(field.get_team().value, end= " ")
            elif field.is_empty():
                print(f" {empty_char[0]} ", end=" ")
            else:
                print(f" {char[0]} ", end=" ")
        print()
    print("- - - - - - - - - - - - - - - - -")

def print_moves_board(board: Board, move_list: List[Move]):
    print("- - - - - - - - - - - - - - - - -")
    move_list_to = [each.to_value for each in move_list]
    for i, row in enumerate(board.board):
        if (i + 1) % 2 == 0:
            print("  ", end="")
        for field in row:
            if field.coordinate in move_list_to:
                print(f" {field.fish} ", end=" ")
            elif field.is_occupied():
                print(field.get_team().value, end= " ")
            elif field.is_empty():
                print("   ", end=" ")
            else:
                print(" - ", end=" ")
        print()
    print("- - - - - - - - - - - - - - - - -")

def own_pretty_print_custom(board: Board, empty_char = " ", one_char = None, two_char = None):
    print("- - - - - - - - - - - - - - - - -")
    for i, row in enumerate(board.board):
        if (i + 1) % 2 == 0:
            print("  ", end="")
        for field in row:
            if field.is_empty():
                print(f" {empty_char[0]} ", end=" ")
            elif field.is_occupied():
                if one_char and field.get_team().value == "ONE":
                    print(f" {one_char[0]} ", end=" ")
                elif two_char and field.get_team().value == "TWO":
                    print(f" {two_char[0]} ", end=" ")
                else:
                    print(field.get_team().value, end= " ")
            else:
                print(f" {field.fish} ", end=" ")
        print()
    print("- - - - - - - - - - - - - - - - -")

def own_pretty_print(board: Board):
    print("- - - - - - - - - - - - - - - - -")
    for i, row in enumerate(board.board):
        if (i + 1) % 2 == 0:
            print("  ", end="")
        for field in row:
            if field.is_empty():
                print(f"   ", end=" ")
            elif field.is_occupied():
                print(field.get_team().value, end=" ")
            else:
                print(f" {field.fish} ", end=" ")
        print()
    print("- - - - - - - - - - - - - - - - -")