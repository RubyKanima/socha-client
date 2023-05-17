from socha import *
from tabulate import tabulate
from typing import List
import logging

from extention.triangles import *

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
    table = [["hash", "root", "value", "inters", "oneway"]]
    for key in group.group:
        tile = group.group[key]
        enum = tile.penguin.team_enum.name if tile.penguin else None
        table.append([key, tile.root, enum or tile.fish, tile.inters, tile.oneway])
    logging.info("\n" + tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

def print_group_board(board:Board, group: Group, team: TeamEnum):
    print("- - - - - - - - - - - - - - - - -")
    for y in range(8):
        if y % 2 == 1:
            print("  ", end="")
        for x in range(8):
            coord = CartesianCoordinate(x,y).to_hex()
            if own_hash(coord) in group.group:
                num = len(group.group) - list(group.group.keys()).index(own_hash(coord))
                if num > 9: print(f" {num} ", end="")
                if num < 10: print(f" 0{num} ", end="")
            else:
                this_field = board.get_field(coord)
                if this_field.is_occupied():
                    if this_field.penguin.team_enum.name == team.name:
                        print(" ⛇  ", end="")
                    else:
                        print(" ඞ  ", end="")
                elif this_field.fish == 0:
                    print("    ", end="")
                else:
                    print(" -- ", end="")
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