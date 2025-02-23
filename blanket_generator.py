"""

Obvs there's the readme, but here's how to EDIT the program ;)

To make a new blanket:
- Create a ColSet object for the set of colours to be used
- Set num_a and num_b to the total hexes per row (max 1 different)
- Set num_row to the total rows
- Set ch_arr to the current state. Case 0 ignores the hex, any number outside the ColSet will be given a suggestion.
- Set `do_cut_halves` as desired

When running this script, blanket.scad is overwritten.
This scad file uses the tile.scad file, where the hex size is defined.

To view size reference overlays on the blanket.scad, use main.scad instead.

"""

from typing import Dict, Union

# The plan is to replace the 'blanket.scad' file
# it will have "use <tile.scad>"

# it can use x_dist_between_hexes for the hz translation multiplier
# it can use y_dist_between_hexes for the v  translation multiplier


class ColTuple:
    """ Data about the colour itself """
    col_name: str
    col_letter: str
    col_rgb: tuple[int, int, int]

    def __init__(self, letter: str, name: str, r: int, g: int, b: int):
        self.col_letter = letter
        self.col_name = name
        self.col_rgb = (r, g, b)


class ColSet:
    """ Data about a collection of colours.
    Colours are put into a dict for easy access, with 0 being a special non-set colour.
    """
    cols: dict[int, ColTuple]
    valid_col_letters: set[str]
    valid_col_indices: set[int]

    def __init__(self, cols: list[ColTuple]):
        self.cols = dict()
        self.valid_col_letters = set()
        self.valid_col_indices = set()
        self.cols[0] = ColTuple("X", "", 10, 10, 10)
        index = 1
        for col in cols:
            self.valid_col_letters.add(col.col_letter)
            self.valid_col_indices.add(index)
            self.cols[index] = col
            index += 1


# JAMES C BRETT SUPER SOFT BABY ARAN COLOURS
blanket1a: ColSet = ColSet(
    [
        ColTuple("C", "cream", 0xEC, 0xE6, 0xDA),
        ColTuple("P", "purple", 0xE8, 0xE1, 0xF1),
        ColTuple("B", "blue", 0xDE, 0xE6, 0xF3),
        ColTuple("G", "green", 0xDD, 0xE7, 0xDE),
        ColTuple("S", "salmon", 0xEF, 0xDC, 0xE0),
        ColTuple("Y", "yellow", 0xFA, 0xE4, 0xB2),
    ])

# JAMES C BRETT SUPER SOFT BABY ARAN COLOURS (dark patches)
blanket1b: ColSet = ColSet(
    [
        ColTuple("C", "cream", 0xF1, 0xDC, 0xAF),
        ColTuple("P", "purple", 0xBA, 0xAB, 0xCC),
        ColTuple("B", "blue", 0x8C, 0xB2, 0xD7),
        ColTuple("G", "green", 0xBC, 0xD7, 0xC6),
        ColTuple("S", "salmon", 0xF4, 0xCA, 0xCB),
        ColTuple("Y", "yellow", 0xFB, 0xD3, 0x61),
    ])

# Merino DK COLOURS
blanket2: ColSet = ColSet(
    [
        ColTuple("DP", "Dark Purple", 0x54, 0x1E, 0x3D),
        ColTuple("LP", "Light Purple", 0x91, 0x76, 0x95),
        ColTuple("LR", "Light Rose", 0xB7, 0x83, 0x6E),
        ColTuple("DR", "Dark Rose", 0xB9, 0x6A, 0x5C),
        ColTuple("La", "Lavender", 0xA4, 0x75, 0x85),
    ])

# Example blanket 3 DK COLOURS
blanket3: ColSet = ColSet(
    [
        ColTuple("DP", "Dark Purple", 0x54, 0x1E, 0x3D),
        ColTuple("LP", "Light Purple", 0x91, 0x76, 0x95),
        ColTuple("LR", "Light Rose", 0xB7, 0x83, 0x6E),
        ColTuple("DR", "Dark Rose", 0xB9, 0x6A, 0x5C),
        ColTuple("La", "Lavender", 0xA4, 0x75, 0x85),
        ColTuple("Wh", "White", 0xEE, 0xEE, 0xEE),
        ColTuple("Gr", "Grey", 0xCC, 0xCC, 0xCC),
    ])

col_formatted_linux_empty = "\033[0m"
col_formatted_scad_empty = ";\n"


def col_formatted_linux(rgb_tuple: tuple[int, int, int]):
    return "\033[48;2;{};{};{}m".format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])


def col_formatted_scad(rgb_tuple: tuple[int, int, int]):
    return "\"#{:02X}{:02X}{:02X}\"".format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])


def print_hex(arr: list[int], a: int, b: int, rows: int, col_set: ColSet) -> None:
    """ Prints to the terminal the hexagon array

    :param arr: is an array of hexagon colour numbers (flattened)
    :param a: is the number of hexes in the first row
    :param b: is the number of hexes in the second row
    :param rows: is the total number of rows
    :param col_set: is the set of colours to translate the hexagons to
    """
    assert isinstance(arr, list) and isinstance(a, int) and isinstance(b, int) and isinstance(rows,
                                                                                              int), "wrong types given"
    assert abs(a - b) <= 1, "a and b can only differ by one"
    assert rows >= 2, "there must be at least 2 rows"
    assert len(arr) >= (a * (rows // 2)) + (
            b * (rows // 2)), "there must be enough tiles for the rows (len(arr) = {})".format(len(arr))
    print("(len(arr) = {})".format(len(arr)))
    j = 0  # WHERE IN THE ROW AM I?
    row_number = 0  # WHICH ROW AM I ON?
    row_a = True
    str_row = ""
    for i in range(len(arr)):
        # If start of Row and this row is smaller than the other row, indent row
        # Also indents if they are the same - there should always be 1 row indented
        if j == 0 and \
                (row_a is True and a <= b or
                 row_a is False and a > b):
            str_row += " "

        my_col = arr[i]
        if my_col in col_set.cols.keys():
            str_row += col_formatted_linux(col_set.cols[my_col].col_rgb)
            str_row += col_set.cols[my_col].col_letter
        else:
            str_row += col_set.cols[0].col_letter
            pass
        str_row += col_formatted_linux_empty
        j += 1
        str_row += " "
        if (row_a is True and j == a or
                row_a is False and j == b):
            print(str_row)
            str_row = ""
            j = 0
            row_a = not row_a
            row_number += 1
            if row_number >= rows:
                break
    print(str_row)


def scad_hex(arr: list[int], a: int, b: int, rows: int, col_set: ColSet) -> str:
    """ Returns the hexagon array as formatted for scad - ready to write to file

    :param arr: is an array of hexagon colour numbers (flattened)
    :param a: is the number of hexes in the first row
    :param b: is the number of hexes in the second row
    :param rows: is the total number of rows
    :param col_set: is the set of colours to translate the hexagons to
    :returns total rows appended together
    """
    assert isinstance(arr, list) and isinstance(a, int) and isinstance(b, int) and isinstance(rows,
                                                                                              int), "wrong types given"
    assert abs(a - b) <= 1, "a and b can only differ by one"
    assert rows >= 2, "there must be at least 2 rows"
    assert len(arr) >= (a * (rows // 2)) + (
            b * (rows // 2)), "there must be enough tiles for the rows (len(arr) = {})".format(len(arr))
    j = 0  # WHERE IN THE ROW AM I?
    row_number = 0  # WHICH ROW AM I ON?
    row_a = True
    str_total = ""
    str_row = ""
    for i in range(len(arr)):
        my_col = arr[i]
        if my_col in col_set.cols.keys():
            str_row += "translate([x_dist_between_hexes * {}, y_dist_between_hexes * {}, 0]) ".format(j, row_number)
            if row_a and a < b:
                str_row += " translate([x_dist_between_hexes/2, 0, 0]) "
            elif not row_a and a >= b:
                str_row += " translate([x_dist_between_hexes/2, 0, 0]) "
            str_row += " hex_crochet(" + col_formatted_scad(col_set.cols[my_col].col_rgb) + ")"  # put the hex
            str_row += col_formatted_scad_empty
        j += 1
        str_row += " "
        if (row_a is True and j == a or
                row_a is False and j == b):
            str_total += str_row
            str_row = ""
            j = 0
            row_a = not row_a
            row_number += 1
            if row_number >= rows:
                break
    str_total += str_row
    return str_total


def add_to_dict(x, d, valid, _num=1):
    """ Adds to the dictionary a count of 'x'.
    If x is already a key, its count is unchanged? # its count is incremented.
    If x is not a key, it is added and count is set to 1
    If x is a dictionary, this function is called for each kvp in x (v is num)

    :param x: thing to add to the dictionary
    :param d: dictionary to add to...
    :param valid: what integers are valid to be added to the dictionary
    :param _num: fixed count to set to regardless of x
    """
    if type(x) != dict:
        if x not in valid:
            return
        if x in d:
            d[x] = max(_num, d[x])  # d[x] + _num
        else:
            d[x] = _num
    else:
        for k, v in x.items():
            add_to_dict(k, d, valid, v)


def weight_dict(d, weight=1):
    new_d = {}
    for k, v in d.items():
        d[k] = weight * v


def get_neighbours(arr: list[list[int]], row_id: int, elem_id: int, valid: set[int], look=None, n1=None) -> dict[int, int]:
    """

    :param arr: full hexagon array
    :param row_id: current row
    :param elem_id: current element in row
    :param valid: valid indices in the col set
    :param look: directions to look for neighbours
    :param n1:
    :returns: dictionary of neighbour index to count of neighbours with that index
    """
    if look is None:
        look = []
    elif look == "all":
        look = ["L", "R", "UL", "UR", "BL", "BR"]
    neighbours = {}
    # Left side neighbour
    if elem_id > 0 and "L" in look:
        add_to_dict(arr[row_id][elem_id - 1], neighbours, valid)
    # Right side neighbour
    if elem_id + 1 < len(arr[row_id]) and "R" in look:
        add_to_dict(arr[row_id][elem_id + 1], neighbours, valid)

    long_row = ((row_id > 0 and len(arr[row_id]) > len(arr[row_id - 1])) or
                (row_id == 0 and len(arr[row_id]) > len(arr[row_id + 1])))
    if row_id > 0:
        # Upper Left neighbour and Upper Right neighbour
        uln = 0
        urn = 0
        if long_row:
            uln = arr[row_id - 1][elem_id - 1] if elem_id > 0 else 0
            urn = arr[row_id - 1][elem_id]
        else:
            uln = arr[row_id - 1][elem_id]
            urn = arr[row_id - 1][elem_id + 1] if elem_id + 1 < len(arr[row_id - 1]) else 0
        if "UL" in look:
            add_to_dict(uln, neighbours, valid)
        if "UR" in look:
            add_to_dict(urn, neighbours, valid)
    if row_id + 1 < len(arr):
        # Bottom Left neighbour and Bottom Right neighbour
        bln = 0
        brn = 0
        if long_row:
            bln = arr[row_id + 1][elem_id - 1] if elem_id > 0 else 0
            brn = arr[row_id + 1][elem_id]
        else:
            bln = arr[row_id + 1][elem_id]
            brn = arr[row_id + 1][elem_id + 1] if elem_id + 1 < len(arr[row_id + 1]) else 0
        if "BL" in look:
            add_to_dict(bln, neighbours, valid)
        if "BR" in look:
            add_to_dict(brn, neighbours, valid)
    if n1 is not None and n1 in neighbours.keys():
        # If an n3 of this n1 is the same as our n1... this n2 should be avoided
        add_to_dict(arr[row_id][elem_id], neighbours, valid, _num=8)
    return neighbours


def get_neighbours_neighbours(arr: list[list[int]], row_id: int, elem_id: int, valid: set[int], initial=True) -> dict[int, int]:
    """

    :param arr: full hexagon array
    :param row_id: current row
    :param elem_id: current element in row
    :param valid: valid indices in the col set
    :param initial: True OR list of directions to look for neighbours
    :returns: dictionary of neighbour- and next-neighbour- indices, to count of neighbour-s with that index (weighted)
    """
    this_elem = arr[row_id][elem_id]
    if this_elem not in valid:
        this_elem = None
    this_look = ["L", "R", "UL", "UR", "BL", "BR"]
    weights = [10, 5, 1]
    if type(initial) == list:
        this_look = initial
        initial = False
    if initial:
        neighbours = get_neighbours(arr, row_id, elem_id, valid, "all")
        weight_dict(neighbours, weights[0])
    else:
        neighbours = get_neighbours(arr, row_id, elem_id, valid, this_look)
        weight_dict(neighbours, weights[1])
    # Left side neighbour
    if elem_id > 0 and "L" in this_look:
        look = ["UL", "L", "BL"]
        if initial:
            ln_result = get_neighbours_neighbours(arr, row_id, elem_id - 1, valid, look)
        else:
            ln_result = get_neighbours(arr, row_id, elem_id - 1, valid, look, this_elem)
            weight_dict(ln_result, weights[2])
        add_to_dict(ln_result, neighbours, valid)
    # Right side neighbour
    if elem_id + 1 < len(arr[row_id]) and "R" in this_look:
        look = ["UR", "R", "BR"]
        if initial:
            rn_result = get_neighbours_neighbours(arr, row_id, elem_id + 1, valid, look)
        else:
            rn_result = get_neighbours(arr, row_id, elem_id + 1, valid, look, this_elem)
            weight_dict(rn_result, weights[2])
        add_to_dict(rn_result, neighbours, valid)

    long_row = ((row_id > 0 and len(arr[row_id]) > len(arr[row_id - 1])) or
                (row_id == 0 and len(arr[row_id]) > len(arr[row_id + 1])))

    if row_id > 0:
        # Up Left neighbour and Up Right neighbour
        uln = 0
        urn = 0
        if long_row:
            uln = elem_id - 1
            urn = elem_id
        else:
            uln = elem_id
            urn = elem_id + 1 if elem_id + 1 < len(arr[row_id - 1]) else -1
        if uln > -1 and "UL" in this_look:
            look = ["UL", "UR", "L"]
            if initial:
                uln_result = get_neighbours_neighbours(arr, row_id - 1, uln, valid, look)
            else:
                uln_result = get_neighbours(arr, row_id - 1, uln, valid, look, this_elem)
                weight_dict(uln_result, weights[2])
            add_to_dict(uln_result, neighbours, valid)
        if urn > -1 and "UR" in this_look:
            look = ["UL", "UR", "R"]
            if initial:
                urn_result = get_neighbours_neighbours(arr, row_id - 1, urn, valid, look)
            else:
                urn_result = get_neighbours(arr, row_id - 1, urn, valid, look, this_elem)
                weight_dict(urn_result, weights[2])
            add_to_dict(urn_result, neighbours, valid)

    if row_id + 1 < len(arr):
        # Bottom Left neighbour and Bottom Right neighbour
        bln = 0
        brn = 0
        if long_row:
            bln = elem_id - 1
            brn = elem_id
        else:
            bln = elem_id
            brn = elem_id + 1 if elem_id + 1 < len(arr[row_id + 1]) else -1
        if bln > -1 and "BL" in this_look:
            look = ["BL", "BR", "L"]
            if initial:
                bln_result = get_neighbours_neighbours(arr, row_id + 1, bln, valid, look)
            else:
                bln_result = get_neighbours(arr, row_id + 1, bln, valid, look, this_elem)
                weight_dict(bln_result, weights[2])
            add_to_dict(bln_result, neighbours, valid)
        if brn > -1:
            look = ["BL", "BR", "R"]
            if initial:
                brn_result = get_neighbours_neighbours(arr, row_id + 1, brn, valid, look)
            else:
                brn_result = get_neighbours(arr, row_id + 1, brn, valid, look, this_elem)
                weight_dict(brn_result, weights[2])
            add_to_dict(brn_result, neighbours, valid)
    return neighbours


def suggestion(n, valid, weighted=False, cached_print=None):
    key_weight_map = {}  # number to weight
    weight_key_map = {}  # weight to number
    for k in valid:
        key_weight_map[k] = n[k] if k in n else 0
        if key_weight_map[k] in weight_key_map:  # if weight already listed..
            weight_key_map[key_weight_map[k]].append(k)
        else:
            weight_key_map[key_weight_map[k]] = [k]
    suggestion_string = "{"
    sorted_suggestion_string = list(weight_key_map.keys())
    sorted_suggestion_string.sort()
    min_weight = 99999
    unique_weights = set()
    for index in range(len(sorted_suggestion_string)):
        this_weight = sorted_suggestion_string[index]
        s = "{weight}: {nodes}, "
        if index == 0:
            s = "{weight}: {col}{nodes}{empty_col}, "
        suggestion_string += s.format(weight=this_weight,
                                      nodes=weight_key_map[sorted_suggestion_string[index]], col="\033[48;2;55;100;55m",
                                      empty_col="\033[0m")
        min_weight = min(min_weight, this_weight)
        unique_weights.add(this_weight)
    suggestion_string = suggestion_string[:-2] + "}"

    if len(unique_weights) != 1 or min_weight != 0:  # All weights are 0 if there is no data
        if cached_print is not None:
            print(cached_print)
        print("{}suggestion = {}".format(("weighted " if weighted else ""), str(suggestion_string)))


def get_suggestion(arr: list[list[int]], col_set: ColSet) -> None:
    total_set_hexes_per_colour: dict[int, int] = {k: 0 for k in col_set.valid_col_indices}
    total_set_hexes = 0
    for row in arr:
        for col in row:
            if col in col_set.valid_col_indices:
                total_set_hexes += 1
                if col in total_set_hexes_per_colour:
                    total_set_hexes_per_colour[col] += 1
                else:
                    total_set_hexes_per_colour[col] = 1

    for row_id in range(len(arr)):
        for elem_id in range(len(arr[row_id])):
            if arr[row_id][elem_id] != 0 and arr[row_id][elem_id] not in col_set.valid_col_indices:
                cached_print = "element {} on row {} ({}):".format(elem_id, row_id, arr[row_id])
                neighbour_count_dict = get_neighbours_neighbours(arr, row_id, elem_id, col_set.valid_col_indices)
                # print("neighbours = {}".format(str(n)))

                # Update for total count - try to make to number of each colour even
                new_neighbour_count_dict = {}
                for neighbour_index in neighbour_count_dict.keys():
                    new_neighbour_count_dict[neighbour_index] = neighbour_count_dict[neighbour_index] \
                                                                + total_set_hexes_per_colour[neighbour_index]
                suggestion(new_neighbour_count_dict, col_set.valid_col_indices, True, cached_print)

    min_total_col_count = min(total_set_hexes_per_colour.values())
    max_total_col_count = max(total_set_hexes_per_colour.values())
    # print("min_split_count {}, max_split_count {}. split_count {}".format(min_split_count, max_split_count, split_count))
    pretty_split_count = "{ "
    for colour_index in col_set.valid_col_indices:
        col = ""
        if min_total_col_count != max_total_col_count:
            if total_set_hexes_per_colour[colour_index] == min_total_col_count:
                col = "\033[48;2;0;100;0m"
            elif total_set_hexes_per_colour[colour_index] == max_total_col_count:
                col = "\033[48;2;100;0;0m"
        pretty_split_count += "{name}({num}): {colour}{val}{done_col}, ".format(
            name=col_set.cols[colour_index].col_name, num=colour_index, val=total_set_hexes_per_colour[colour_index],
            colour=col, done_col="\033[0m")
    pretty_split_count = pretty_split_count[:-2] + " }"
    print("Total: {}. Split: {}".format(str(total_set_hexes), pretty_split_count))


# This is Blanket1!
colour_set = blanket1b
num_a = 13
num_b = 12
num_row = 15
ch_arr = [
    [2, 4, 6, 2, 1, 2, 5, 3, 1, 5, 3, 5, 6],
    [3, 5, 3, 4, 6, 4, 2, 4, 6, 2, 4, 2],
    [1, 6, 2, 1, 2, 3, 1, 6, 1, 5, 3, 1, 4],
    [4, 5, 6, 3, 5, 4, 5, 3, 4, 6, 5, 3],
    [5, 6, 3, 4, 2, 6, 2, 1, 6, 2, 1, 2, 6],
    [1, 2, 5, 1, 4, 3, 4, 5, 4, 3, 4, 5],
    [6, 3, 1, 6, 3, 5, 1, 6, 3, 1, 6, 1, 4],
    [5, 4, 5, 2, 1, 6, 2, 5, 2, 4, 2, 3],
    [3, 2, 1, 3, 6, 4, 3, 4, 6, 3, 5, 6, 5],
    [4, 6, 4, 5, 1, 2, 5, 1, 2, 1, 4, 1],
    [1, 5, 3, 2, 6, 4, 6, 3, 5, 4, 3, 6, 2],
    [2, 6, 1, 5, 3, 5, 2, 4, 6, 2, 5, 3],
    [3, 4, 2, 4, 1, 2, 1, 3, 1, 3, 4, 1, 5],
    [1, 5, 1, 3, 6, 4, 6, 5, 6, 2, 6, 4],
    [2, 3, 6, 2, 5, 3, 1, 2, 4, 5, 1, 3, 2]
]

# This is Blanket2 - Pinks!
colour_set = blanket2
num_a = 14
num_b = 14
num_row = 10
ch_arr = [
    [1, 3, 5, 1, 2, 3, 2, 1, 5, 3, 4, 2, 1, 5],
    [5, 2, 4, 3, 4, 1, 5, 4, 2, 4, 2, 5, 3, 4],
    [4, 5, 1, 2, 5, 4, 2, 5, 3, 1, 3, 2, 5, 1],
    [2, 1, 3, 5, 1, 2, 1, 4, 2, 5, 2, 4, 1, 2],
    [3, 4, 2, 3, 4, 5, 3, 1, 4, 3, 1, 2, 4, 3],
    [4, 2, 3, 5, 1, 2, 1, 5, 2, 1, 4, 3, 5, 1],
    [5, 4, 2, 3, 5, 4, 3, 4, 3, 5, 2, 1, 3, 4],
    [2, 1, 3, 4, 1, 2, 5, 1, 2, 4, 1, 5, 4, 5],
    [5, 4, 1, 3, 4, 3, 4, 3, 1, 5, 2, 3, 2, 1],
    [3, 1, 3, 5, 2, 1, 5, 2, 5, 4, 3, 1, 5, 4]
]  # (14,14)*10 = 140 hexes (some are half hexes)

# num_a = 12; num_b = 12; num_row = 9; ch_arr = [
#     [1, 2, 3, 4, 1, 6, 3, 5, 9, 9, 9, 9],
#     [4, 5, 6, 5, 2, 4, 1, 6, 9, 9, 9, 9],
#     [9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
#     [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
#   # (12,12)*9 = 108 hexes
colour_set = blanket3
num_a = 10
num_b = 10
num_row = 10
ch_arr = [
    [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
    [4, 5, 6, 7, 1, 2, 3, 4, 5, 6],
    [7, 1, 2, 3, 4, 5, 6, 7, 1, 2],
    [3, 4, 5, 6, 7, 1, 2, 3, 4, 5],
    [6, 7, 1, 2, 3, 4, 5, 6, 7, 1],
    [2, 3, 4, 5, 6, 7, 1, 2, 3, 4],
    [5, 6, 7, 1, 2, 3, 4, 5, 6, 7],
    [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
    [4, 5, 6, 7, 1, 2, 3, 4, 5, 6],
    [7, 1, 2, 3, 4, 5, 6, 7, 1, 2]
]

if __name__ == "__main__":
    ch_arr_copy = ch_arr.copy()
    norm_flat: list[int] = [item for sublist in ch_arr_copy for item in sublist]  # FLATTEN
    ch_arr_copy.reverse()
    rev_flat: list[int] = [item for sublist in ch_arr_copy for item in sublist]  # FLATTEN

    print_hex(norm_flat, num_a, num_b, num_row, colour_set)

    do_translation = True
    do_cut_halves = True
    do_rotate = False

    with open("blanket.scad", "w") as file:
        file.write("include <tile.scad>\n")
        if do_rotate:
            file.write("centre_x = x_dist_between_hexes*{width}/2;\n".format(width=min(num_a, num_b), height=num_row))
            file.write("centre_y = y_dist_between_hexes*{height}/2 + hex_length/8;\n".format(width=min(num_a, num_b),
                                                                                             height=num_row))

            # These are for a centre dot & half-way lines
            # file.write("translate([centre_x, centre_y, 0]) color(\"red\") cylinder(h=50,d=20);\n")
            # file.write("translate([centre_x, centre_y, 0] - [10,centre_y,0]) color(\"yellow\") cube([10,centre_y, 20]);\n")
            # file.write("translate([centre_x, centre_y, 0]) color(\"green\") cube([10,centre_y, 20]);\n")

            file.write("translate([centre_y, centre_x, 0]) ")
            file.write("rotate([0,0,90]) ")
            file.write("translate(-[centre_x, centre_y, 0]) ")
            file.write("\n{\n")

        if do_translation:
            if do_cut_halves:
                file.write("translate([0, hex_length/2, 0])\n{\n")
                file.write("difference()\n{\n")
                file.write("union()\n{\n")
            else:
                file.write("translate([x_dist_between_hexes/2, hex_length/2, 0])\n{\n")

        # file.write("color(\"blue\")\n")

        file.write(scad_hex(rev_flat, num_a, num_b, num_row, colour_set))

        if do_translation:
            if do_cut_halves:
                file.write("}\n")  # Close union
                file.write(
                    "translate([-x_dist_between_hexes, -y_dist_between_hexes, -1]) cube([x_dist_between_hexes, y_dist_between_hexes*{num_row}, 10]);\n".format(
                        num_row=num_row))
                file.write(
                    "translate([x_dist_between_hexes*({num} - 0.5), -y_dist_between_hexes, -1]) cube([x_dist_between_hexes, y_dist_between_hexes*{num_row}, 10]);\n".format(
                        num=min(num_a, num_b), num_row=num_row + 1))
                file.write("}\n")  # Close difference
            file.write("}\n")  # Close translate

        if do_rotate:
            file.write("}\n")  # Close rotate

    get_suggestion(ch_arr, colour_set)
