from typing import Dict, Union

# The plan is to replace the 'blanket.scad' file
# it will have "use <tile.scad>"

# it can use x_dist_between_hexes for the hz translation multiplier
# it can use y_dist_between_hexes for the v  translation multiplier

#Val's thing is 170x184cm


##red   = "\"#c39390\""
##green = "\"#b6bf64\""
##blue  = "\"#9fb4c7\""
##white = "\"#e4dad0\""

## BLANKET PATTERN COLOURS
#red   = [0xc3, 0x93, 0x90]
#green = [0xb6, 0xbf, 0x64]
#blue  = [0x9f, 0xb4, 0xc7]
#white = [0xe4, 0xda, 0xd0]

## JAMES C BRETT SUPER SOFT BABY ARAN COLOURS
cream  = [0xEC, 0xE6, 0xDA]
purple = [0xE8, 0xE1, 0xF1]
blue   = [0xDE, 0xE6, 0xF3]
green  = [0xDD, 0xE7, 0xDE]
salmon = [0xEF, 0xDC, 0xE0]
yellow = [0xFA, 0xE4, 0xB2]

## JAMES C BRETT SUPER SOFT BABY ARAN COLOURS (dark patches)
cream  = [0xF1, 0xDC, 0xAF]
purple = [0xBA, 0xAB, 0xCC]
blue   = [0x8C, 0xB2, 0xD7]
green  = [0xBC, 0xD7, 0xC6]
salmon = [0xF4, 0xCA, 0xCB]
yellow = [0xFB, 0xD3, 0x61]

cols_linu0 = {
    "R": "\033[41m",
    "G": "\033[42m",
    "Y": "\033[43m",
    "B": "\033[44m",
    "W": "\033[47m",
    "Empty": "\033[0m" 
}
#cols_linux2 = {
#    "R": "\033[48;2;195;147;144m",
#    "G": "\033[48;2;182;191;100m",
#    "Y": "\033[48;2;160;160;20m",
#    "B": "\033[48;2;159;180;199m",
#    "W": "\033[48;2;200;200;200m",
#    "Empty": "\033[0m" 
#}
cols_linux2 = {
    "C": "\033[48;2;{};{};{}m".format(cream[0], cream[1], cream[2]),
    "P": "\033[48;2;{};{};{}m".format(purple[0], purple[1], purple[2]),
    "B": "\033[48;2;{};{};{}m".format(blue[0], blue[1], blue[2]),
    "G": "\033[48;2;{};{};{}m".format(green[0], green[1], green[2]),
    "S": "\033[48;2;{};{};{}m".format(salmon[0], salmon[1], salmon[2]),
    "Y": "\033[48;2;{};{};{}m".format(yellow[0], yellow[1], yellow[2]),
    "X": "\033[48;2;{};{};{}m".format(10,10,10),
    "Empty": "\033[0m" 
}
cols_scad = {
    "C": "\"#{:02X}{:02X}{:02X}\"".format(cream[0], cream[1], cream[2]),
    "P": "\"#{:02X}{:02X}{:02X}\"".format(purple[0], purple[1], purple[2]),
    "B": "\"#{:02X}{:02X}{:02X}\"".format(blue[0], blue[1], blue[2]),
    "G": "\"#{:02X}{:02X}{:02X}\"".format(green[0], green[1], green[2]),
    "S": "\"#{:02X}{:02X}{:02X}\"".format(salmon[0], salmon[1], salmon[2]),
    "Y": "\"#{:02X}{:02X}{:02X}\"".format(yellow[0], yellow[1], yellow[2]),
    "X": "\"#{:02X}{:02X}{:02X}\"".format(10,10,10),
    "Empty": ";\n"                        
}
cols_windows = {
    "R": "",
    "G": "",
    "Y": "",
    "B": "",
    "W": "",
    "Empty": "" 
}
cols = cols_linux2
key = {0: "X", 1: "C", 2: "P", 3: "B", 4: "G", 5: "S", 6: "Y", 9: "X"}


def print_hex(arr, a, b, rows):
    # arr is an array
    # a is the number of hexes in the first row
    # b is the number of hexes in the second row
    # rows is the total number of rows
    assert isinstance(arr, list) and isinstance(a, int) and isinstance(b, int) and isinstance(rows, int), "wrong types given"
    assert abs(a-b) <= 1, "a and b can only differ by one"
    assert rows >= 2, "there must be at least 2 rows"
    assert len(arr) >= (a*(rows//2)) + (b*(rows//2)), "there must be enough tiles for the rows (len(arr) = {})".format(len(arr))
    print("(len(arr) = {})".format(len(arr)))
    j=0 # WHERE IN THE ROW AM I?
    row_number = 0 # WHICH ROW AM I ON?
    row_a = True
    str_row = ""
    for i in range(len(arr)):
        if j == 0 and \
        (row_a == True and a <= b or \
        row_a == False and a > b):
            # print a blank
            str_row += " "
        my_char = str(arr[i])[0]
        if (my_char in cols):
            str_row += cols[my_char]
        str_row += my_char
        str_row += cols["Empty"]
        j += 1
        str_row += " "
        if row_a == True and j == a or \
        row_a == False and j == b:
            print(str_row)
            str_row = ""
            j = 0
            row_a = not row_a
            row_number += 1
            if row_number >= rows:
                break
    print(str_row)
    if (a == b):
        # a should have a blank before and b should have a blank after
        pass
    elif (a > b):
        # b should have a blank before and after
        pass
    else: # a < b
        # a should have a blank before and after
        pass


def scad_hex(arr, a, b, rows):
    # arr is an array
    # a is the number of hexes in the first row
    # b is the number of hexes in the second row
    # rows is the total number of rows
    assert isinstance(arr, list) and isinstance(a, int) and isinstance(b, int) and isinstance(rows, int), "wrong types given"
    assert abs(a-b) <= 1, "a and b can only differ by one"
    assert rows >= 2, "there must be at least 2 rows"
    assert len(arr) >= (a*(rows//2)) + (b*(rows//2)), "there must be enough tiles for the rows (len(arr) = {})".format(len(arr))
    j=0 # WHERE IN THE ROW AM I?
    row_number = 0 # WHICH ROW AM I ON?
    row_a = True
    str_total = ""
    str_row = ""
    for i in range(len(arr)):
        my_char = str(arr[i])[0]
        if (my_char in cols_scad):
            str_row += "translate([x_dist_between_hexes * {}, y_dist_between_hexes * {}, 0]) ".format(j, row_number) # translate to correct place
            if row_a and a < b:
                str_row += " translate([x_dist_between_hexes/2, 0, 0]) "
            elif not row_a and a >= b:
                str_row += " translate([x_dist_between_hexes/2, 0, 0]) "
            str_row += " hex_crochet(" + cols_scad[my_char] + ")" # put the hex
            str_row += cols_scad["Empty"]
        j += 1
        str_row += " "
        if row_a == True and j == a or \
        row_a == False and j == b:
            str_total += str_row
            str_row = ""
            j = 0
            row_a = not row_a
            row_number += 1
            if row_number >= rows:
                break
    str_total += str_row
    return str_total


def add_to_dict(x, d, ignore=None, _num=1):
    if type(x) != dict:
        if ignore is not None and x in ignore:
            return
        if x in d:
            d[x] = max(_num, d[x])  # d[x] + _num
        else:
            d[x] = _num
    else:
        for k, v in x.items():
            add_to_dict(k, d, ignore, v)


def weight_dict(d, weight=1):
    new_d = {}
    for k, v in d.items():
        d[k] = weight * v


def get_neighbours(arr, row_id, elem_id, ignore, look=None, n1=None) -> dict[int, int]:
    # if arr[row_id][elem_id] in ignore: return {}
    if look is None:
        look = []
    elif look == "all":
        look = ["L", "R", "UL", "UR", "BL", "BR"]
    neighbours = {}
    # Left side neighbour
    if elem_id > 0 and "L" in look:
        add_to_dict(ch_arr[row_id][elem_id - 1], neighbours, ignore)
    # Right side neighbour
    if elem_id + 1 < len(ch_arr[row_id]) and "R" in look:
        add_to_dict(ch_arr[row_id][elem_id + 1], neighbours, ignore)

    long_row = ((row_id > 0 and len(ch_arr[row_id]) > len(ch_arr[row_id - 1])) or
                (row_id == 0 and len(ch_arr[row_id]) > len(ch_arr[row_id + 1])))
    if row_id > 0:
        # Upper Left neighbour and Upper Right neighbour
        uln = 0
        urn = 0
        if long_row:
            uln = ch_arr[row_id - 1][elem_id - 1] if elem_id > 0 else 0
            urn = ch_arr[row_id - 1][elem_id]
        else:
            uln = ch_arr[row_id - 1][elem_id]
            urn = ch_arr[row_id - 1][elem_id + 1] if elem_id + 1 < len(ch_arr[row_id - 1]) else 0
        if "UL" in look:
            add_to_dict(uln, neighbours, ignore)
        if "UR" in look:
            add_to_dict(urn, neighbours, ignore)
    if row_id + 1 < len(ch_arr):
        # Bottom Left neighbour and Bottom Right neighbour
        bln = 0
        brn = 0
        if long_row:
            bln = ch_arr[row_id + 1][elem_id - 1] if elem_id > 0 else 0
            brn = ch_arr[row_id + 1][elem_id]
        else:
            bln = ch_arr[row_id + 1][elem_id]
            brn = ch_arr[row_id + 1][elem_id + 1] if elem_id + 1 < len(ch_arr[row_id + 1]) else 0
        if "BL" in look:
            add_to_dict(bln, neighbours, ignore)
        if "BR" in look:
            add_to_dict(brn, neighbours, ignore)
    if n1 is not None and n1 in neighbours.keys():
        # If an n3 of this n1 is the same as our n1... this n2 should be avoided
        add_to_dict(ch_arr[row_id][elem_id], neighbours, ignore, _num=8)
    return neighbours


def get_neighbours_neighbours(arr, row_id, elem_id, ignore, initial=True) -> dict[int, int]:
    this_elem = arr[row_id][elem_id]
    if this_elem in ignore:
        this_elem = None
    # if not initial and arr[row_id][elem_id] in ignore: return {}
    this_look = ["L", "R", "UL", "UR", "BL", "BR"]
    weights = [10, 5, 1]
    if type(initial) == list:
        this_look = initial
        initial = False
    if initial:
        neighbours = get_neighbours(arr, row_id, elem_id, ignore, "all")
        weight_dict(neighbours, weights[0])
    else:
        neighbours = get_neighbours(arr, row_id, elem_id, ignore, this_look)
        weight_dict(neighbours, weights[1])
    # Left side neighbour
    if elem_id > 0 and "L" in this_look:
        look = ["UL", "L", "BL"]
        if initial:
            ln_result = get_neighbours_neighbours(ch_arr, row_id, elem_id - 1, ignore, look)
        else:
            ln_result = get_neighbours(ch_arr, row_id, elem_id - 1, ignore, look, this_elem)
            weight_dict(ln_result, weights[2])
        add_to_dict(ln_result, neighbours)
    # Right side neighbour
    if elem_id + 1 < len(ch_arr[row_id]) and "R" in this_look:
        look = ["UR", "R", "BR"]
        if initial:
            rn_result = get_neighbours_neighbours(ch_arr, row_id, elem_id + 1, ignore, look)
        else:
            rn_result = get_neighbours(ch_arr, row_id, elem_id + 1, ignore, look, this_elem)
            weight_dict(rn_result, weights[2])
        add_to_dict(rn_result, neighbours)

    long_row = ((row_id > 0 and len(ch_arr[row_id]) > len(ch_arr[row_id - 1])) or
                (row_id == 0 and len(ch_arr[row_id]) > len(ch_arr[row_id + 1])))

    if row_id > 0:
        # Up Left neighbour and Up Right neighbour
        uln = 0
        urn = 0
        if long_row:
            uln = elem_id - 1
            urn = elem_id
        else:
            uln = elem_id
            urn = elem_id + 1 if elem_id + 1 < len(ch_arr[row_id - 1]) else -1
        if uln > -1 and "UL" in this_look:
            look = ["UL", "UR", "L"]
            if initial:
                uln_result = get_neighbours_neighbours(ch_arr, row_id - 1, uln, ignore, look)
            else:
                uln_result = get_neighbours(ch_arr, row_id - 1, uln, ignore, look, this_elem)
                weight_dict(uln_result, weights[2])
            add_to_dict(uln_result, neighbours)
        if urn > -1 and "UR" in this_look:
            look = ["UL", "UR", "R"]
            if initial:
                urn_result = get_neighbours_neighbours(ch_arr, row_id - 1, urn, ignore, look)
            else:
                urn_result = get_neighbours(ch_arr, row_id - 1, urn, ignore, look, this_elem)
                weight_dict(urn_result, weights[2])
            add_to_dict(urn_result, neighbours)

    if row_id + 1 < len(ch_arr):
        # Bottom Left neighbour and Bottom Right neighbour
        bln = 0
        brn = 0
        if long_row:
            bln = elem_id - 1
            brn = elem_id
        else:
            bln = elem_id
            brn = elem_id + 1 if elem_id + 1 < len(ch_arr[row_id + 1]) else -1
        if bln > -1 and "BL" in this_look:
            look = ["BL", "BR", "L"]
            if initial:
                bln_result = get_neighbours_neighbours(ch_arr, row_id + 1, bln, ignore, look)
            else:
                bln_result = get_neighbours(ch_arr, row_id + 1, bln, ignore, look, this_elem)
                weight_dict(bln_result, weights[2])
            add_to_dict(bln_result, neighbours)
        if brn > -1:
            look = ["BL", "BR", "R"]
            if initial:
                brn_result = get_neighbours_neighbours(ch_arr, row_id + 1, brn, ignore, look)
            else:
                brn_result = get_neighbours(ch_arr, row_id + 1, brn, ignore, look, this_elem)
                weight_dict(brn_result, weights[2])
            add_to_dict(brn_result, neighbours)
    return neighbours


def suggestion(n, weighted=False):
    key_weight_map = {}  # number to weight
    weight_key_map = {}  # weight to number
    for k in key:
        if k != 0 and k != 9:
            key_weight_map[k] = n[k] if k in n else 0
            if key_weight_map[k] in weight_key_map:  # if weight already listed..
                weight_key_map[key_weight_map[k]].append(k)
            else:
                weight_key_map[key_weight_map[k]] = [k]
    suggestion_string = "{"
    sorted_suggestion_string = list(weight_key_map.keys())
    sorted_suggestion_string.sort()
    for index in range(len(sorted_suggestion_string)):
        s = "{weight}: {nodes}, "
        if index == 0:
            s = "{weight}: {col}{nodes}{empty_col}, "
        suggestion_string += s.format(weight=sorted_suggestion_string[index], nodes=weight_key_map[sorted_suggestion_string[index]], col="\033[48;2;55;100;55m", empty_col="\033[0m")
    suggestion_string = suggestion_string[:-2] + "}"

    print("{}suggestion = {}".format(("weighted " if weighted else ""), str(suggestion_string)))


def get_suggestion():
    split_count: dict[str, int] = {}
    rev_keys: dict[str, int] = {k: v for v, k in key.items()}
    tot = 0
    for c in norm_flat:
        if c == "X": continue
        tot += 1
        if c in split_count:
            split_count[c] += 1
        else:
            split_count[c] = 1

    for row_id in range(len(ch_arr)):
        for elem_id in range(len(ch_arr[row_id])):
            if ch_arr[row_id][elem_id] == 9:
                print("element {} on row {} ({}):".format(elem_id, row_id, ch_arr[row_id]))
                n = get_neighbours_neighbours(ch_arr, row_id, elem_id, [0, 9])
                print("neighbours = {}".format(str(n)))
                suggestion(n)
                new_n = {}
                for k in n.keys():
                    new_n[k] = n[k] + split_count[key[k]]
                suggestion(new_n, True)

    min_split_count = min(split_count.values())
    max_split_count = max(split_count.values())
    # print("min_split_count {}, max_split_count {}. split_count {}".format(min_split_count, max_split_count, split_count))
    pretty_split_count = "{ "
    for k in rev_keys.keys():
        if k in split_count:  # REMOVES X/0
            col = ""
            if min_split_count != max_split_count:
                if split_count[k] == min_split_count:
                    col = "\033[48;2;0;100;0m"
                elif split_count[k] == max_split_count:
                    col = "\033[48;2;100;0;0m"
            pretty_split_count += "{name}({num}): {colour}{val}{done_col}, ".format(
                name=k, num=rev_keys[k], val=split_count[k], colour=col, done_col="\033[0m")
    pretty_split_count = pretty_split_count[:-2] + " }"
    print("Total: {}. Split: {}".format(str(tot), pretty_split_count))


##ch_arr = [ ["B", "R", "B", "R", "B", "R", "B", "R"], \
##          ["W", "G", "W", "G", "W", "G", "W", "G", "W"], \
##            ["B", "R", "B", "R", "B", "R", "B", "R"], \
##          ["W", "G", "W", "G", "W", "G", "W", "G", "W"], \
##            ["B", "R", "B", "R", "B", "R", "B", "R"], \
##          ["W", "G", "W", "G", "W", "G", "W", "G", "W"], \
##            ["B", "R", "B", "R", "B", "R", "B", "R"], \
##          ["W", "G", "W", "G", "W", "G", "W", "G", "W"], \
##            ["B", "R", "B", "R", "B", "R", "B", "R"], \
##          ["W", "G", "W", "G", "W", "G", "W", "G", "W"], \
##            ["B", "R", "B", "R", "B", "R", "B", "R"]]
##print_hex(ch_arr, 9, 8, 2)

num_a = 16; num_b = 15; num_row = 19; ch_arr = [ 
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "P", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"], \
            ["B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B", "S", "B"], \
          ["Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G", "Y", "G"] \
            ]
            
num_a = 16; num_b = 15; num_row = 19; ch_arr = [ 
          ["Y", "B", "P", "C", "P", "G", "S", "B", "Y", "C", "P", "B", "G", "Y", "C", "S"], \
            ["S", "C", "Y", "G", "S", "B", "Y", "C", "P", "B", "G", "S", "C", "B", "P"], \
          ["Y", "B", "S", "C", "B", "G", "P", "S", "Y", "C", "P", "B", "Y", "S", "G", "Y"], \
            ["S", "G", "Y", "S", "P", "B", "C", "G", "S", "Y", "C", "G", "C", "Y", "S"], \
          ["G", "B", "P", "C", "Y", "C", "P", "Y", "B", "G", "S", "P", "S", "P", "G", "Y"], \
            ["P", "G", "Y", "S", "G", "Y", "C", "P", "S", "B", "Y", "B", "Y", "B", "P"], \
          ["C", "B", "P", "G", "B", "P", "S", "Y", "G", "C", "G", "C", "G", "C", "G", "B"], \
            ["S", "G", "B", "S", "G", "B", "G", "S", "P", "B", "S", "P", "S", "P", "S"], \
          ["Y", "B", "P", "C", "B", "P", "C", "P", "B", "Y", "P", "Y", "B", "Y", "B", "Y"], \
            ["P", "C", "Y", "P", "C", "Y", "B", "C", "G", "C", "G", "C", "G", "C", "G"], \
          ["G", "Y", "S", "C", "Y", "S", "C", "Y", "S", "P", "S", "P", "S", "P", "S", "C"], \
            ["S", "G", "Y", "S", "G", "Y", "S", "G", "B", "Y", "B", "Y", "B", "Y", "P"], \
          ["C", "B", "S", "G", "B", "S", "G", "B", "P", "C", "G", "C", "G", "C", "B", "S"], \
            ["P", "C", "B", "P", "G", "B", "P", "C", "Y", "S", "P", "S", "P", "G", "Y"], \
          ["G", "Y", "P", "C", "B", "P", "C", "Y", "S", "G", "B", "Y", "B", "S", "C", "P"], \
            ["B", "S", "Y", "P", "C", "Y", "S", "G", "B", "P", "C", "G", "Y", "P", "B"], \
          ["G", "P", "G", "S", "Y", "S", "G", "B", "P", "C", "Y", "S", "C", "B", "C", "G"], \
            ["B", "C", "B", "G", "B", "P", "C", "Y", "S", "G", "B", "P", "G", "S", "P"], \
          ["C", "S", "G", "P", "C", "Y", "S", "G", "B", "P", "C", "Y", "S", "Y", "C", "B"] \
            ]
num_a = 13; num_b = 12; num_row = 15; ch_arr = [ 
          ["P", "B", "C", "B", "G", "P", "S", "Y", "C", "P", "B", "C", "Y"], \
            ["G", "Y", "S", "P", "B", "C", "G", "S", "Y", "C", "G", "P"], \
          ["S", "P", "C", "Y", "C", "P", "Y", "B", "G", "S", "P", "S", "G"], \
            ["G", "Y", "S", "G", "Y", "C", "P", "S", "B", "Y", "B", "Y"], \
          ["B", "P", "G", "B", "P", "S", "Y", "G", "C", "G", "C", "G", "C"], \
            ["G", "B", "S", "G", "B", "G", "S", "P", "B", "S", "P", "S"], \
          ["B", "P", "C", "B", "P", "C", "P", "B", "Y", "P", "Y", "B", "Y"], \
            ["C", "Y", "P", "C", "Y", "B", "C", "G", "C", "G", "C", "G"], \
          ["Y", "S", "C", "Y", "S", "C", "Y", "S", "P", "S", "P", "S", "P"], \
            ["G", "Y", "S", "G", "Y", "S", "G", "B", "Y", "B", "Y", "B"], \
          ["B", "S", "G", "B", "S", "G", "B", "P", "C", "G", "C", "G", "C"], \
            ["C", "B", "P", "G", "B", "P", "C", "Y", "S", "P", "S", "P"], \
          ["S", "P", "C", "B", "P", "C", "Y", "S", "G", "B", "Y", "B", "Y"], \
            ["G", "Y", "P", "C", "Y", "S", "G", "B", "P", "C", "G", "S"], \
          ["C", "B", "S", "Y", "S", "G", "B", "P", "C", "Y", "S", "C", "B"] \
            ]

num_a = 13; num_b = 12; num_row = 15; ch_arr = [ 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 3, 5, 2, 6, 0, 0, 0, 0], \
          [0, 0, 0, 1, 4, 2, 3, 4, 1, 0, 0, 0, 0], \
            [0, 0, 0, 5, 1, 6, 1, 3, 5, 0, 0, 0], \
          [0, 0, 0, 6, 4, 3, 4, 5, 6, 4, 0, 0, 0], \
            [0, 0, 1, 5, 2, 1, 2, 3, 2, 6, 0, 0], \
          [0, 0, 2, 3, 4, 6, 5, 4, 1, 5, 0, 0, 0], \
            [0, 0, 4, 2, 1, 4, 3, 5, 6, 0, 0, 0], \
          [0, 0, 0, 6, 3, 5, 6, 2, 1, 0, 0, 0, 0], \
            [0, 0, 0, 5, 1, 3, 5, 4, 0, 0, 0, 0], \
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
            ]
num_a = 13; num_b = 12; num_row = 15; 
ch_arr = [
[4, 3, 2, 5, 1, 6, 1, 5, 6, 5, 4, 3, 1],
[6, 1, 4, 2, 3, 4, 2, 1, 4, 2, 6, 4],
[1, 3, 2, 6, 1, 5, 3, 6, 2, 3, 1, 5, 6],
[2, 5, 3, 4, 6, 2, 1, 5, 4, 5, 2, 3],
[6, 4, 1, 2, 3, 5, 4, 2, 6, 1, 6, 4, 1],
[2, 3, 5, 6, 1, 6, 5, 3, 4, 3, 5, 2],
[1, 5, 6, 4, 2, 4, 3, 1, 2, 5, 1, 6, 3],
[4, 2, 3, 1, 5, 2, 6, 4, 6, 2, 4, 1],
[3, 1, 5, 4, 6, 3, 1, 5, 3, 1, 3, 5, 2],
[4, 3, 6, 2, 1, 4, 6, 2, 4, 6, 4, 6],
[5, 6, 2, 1, 5, 3, 2, 5, 1, 3, 2, 1, 3],
[1, 5, 3, 4, 6, 5, 1, 3, 2, 5, 4, 2],
[4, 2, 4, 1, 2, 1, 4, 6, 4, 6, 3, 6, 5],
[3, 5, 6, 5, 6, 3, 2, 5, 1, 2, 1, 4],
[6, 1, 2, 3, 4, 5, 1, 6, 3, 4, 5, 3, 2]
]
ch_arr = [  # This is the one we are making!
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

num_a = 13; num_b = 14; num_row = 15; 
ch_arr = [
[2, 4, 6, 2, 1, 2, 5, 3, 1, 5, 3, 5, 6],
[6, 3, 5, 3, 4, 6, 4, 2, 4, 6, 2, 4, 2, 5],
[1, 6, 2, 1, 2, 3, 1, 6, 1, 5, 3, 1, 4],
[2, 4, 5, 6, 3, 5, 4, 5, 3, 4, 6, 5, 3, 5],
[5, 6, 3, 4, 2, 6, 2, 1, 6, 2, 1, 2, 6],
[3, 1, 2, 5, 1, 4, 3, 4, 5, 4, 3, 4, 5, 1],
[6, 3, 1, 6, 3, 5, 1, 6, 3, 1, 6, 1, 4],
[4, 5, 4, 5, 2, 1, 6, 2, 5, 2, 4, 2, 3, 1],
[3, 2, 1, 3, 6, 4, 3, 4, 6, 3, 5, 6, 5],
[2, 4, 6, 4, 5, 1, 2, 5, 1, 2, 1, 4, 1, 3],
[1, 5, 3, 2, 6, 4, 6, 3, 5, 4, 3, 6, 2],
[5, 2, 6, 1, 5, 3, 5, 2, 4, 6, 2, 5, 3, 4],
[3, 4, 2, 4, 1, 2, 1, 3, 1, 3, 4, 1, 5],
[6, 1, 5, 1, 3, 6, 4, 6, 5, 6, 2, 6, 4, 1],
[2, 3, 6, 2, 5, 3, 1, 2, 4, 5, 1, 3, 2]
]
ch_arr = [
 [2, 4, 6, 2, 1, 2, 5, 3, 1, 5, 3, 5, 6],
[9, 3, 5, 3, 4, 6, 4, 2, 4, 6, 2, 4, 2, 9],
 [1, 6, 2, 1, 2, 3, 1, 6, 1, 5, 3, 1, 4],
[9, 4, 5, 6, 3, 5, 4, 5, 3, 4, 6, 5, 3, 5],
 [5, 6, 3, 4, 2, 6, 2, 1, 6, 2, 1, 2, 6],
[9, 1, 2, 5, 1, 4, 3, 4, 5, 4, 3, 4, 5, 9],
 [6, 3, 1, 6, 3, 5, 1, 6, 3, 1, 6, 1, 4],
[4, 5, 4, 5, 2, 1, 6, 2, 5, 2, 4, 2, 3, 1],
 [3, 2, 1, 3, 6, 4, 3, 4, 6, 3, 5, 6, 5],
[9, 4, 6, 4, 5, 1, 2, 5, 1, 2, 1, 4, 1, 9],
 [1, 5, 3, 2, 6, 4, 6, 3, 5, 4, 3, 6, 2],
[5, 2, 6, 1, 5, 3, 5, 2, 4, 6, 2, 5, 3, 4],
 [3, 4, 2, 4, 1, 2, 1, 3, 1, 3, 4, 1, 5],
[9, 1, 5, 1, 3, 6, 4, 6, 5, 6, 2, 6, 4, 1],
 [2, 3, 6, 2, 5, 3, 1, 2, 4, 5, 1, 3, 2]
]
    
if __name__ == "__main__":
    ch_arr_copy = ch_arr.copy()
    norm_flat = [(key[item] if item in key.keys() else item) for sublist in ch_arr_copy for item in sublist]  # FLATTEN
    ch_arr_copy.reverse()
    rev_flat  = [(key[item] if item in key.keys() else item) for sublist in ch_arr_copy for item in sublist]  # FLATTEN


    print_hex(norm_flat, num_a, num_b, num_row)

    do_translation = True
    do_cut_halves = True
    do_rotate = False

    with open("blanket.scad", "w") as file:
        file.write("include <tile.scad>\n")
        if do_rotate:
            file.write("centre_x = x_dist_between_hexes*{width}/2;\n".format(width=min(num_a, num_b), height=num_row))
            file.write("centre_y = y_dist_between_hexes*{height}/2 + hex_length/8;\n".format(width=min(num_a, num_b), height=num_row))
            
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
            
        #file.write("color(\"blue\")\n")
        
        file.write(scad_hex(rev_flat, num_a, num_b, num_row))
        
        
        if do_translation:
            if do_cut_halves:
                file.write("}\n")  # Close union
                file.write("translate([-x_dist_between_hexes, -y_dist_between_hexes, -1]) cube([x_dist_between_hexes, y_dist_between_hexes*{num_row}, 10]);\n".format(num_row=num_row))
                file.write("translate([x_dist_between_hexes*({num_b} - 1), -y_dist_between_hexes, -1]) cube([x_dist_between_hexes, y_dist_between_hexes*{num_row}, 10]);\n".format(num_b=num_b, num_row=num_row))
                file.write("}\n")  # Close difference
            file.write("}\n")  # Close translate
            
        if do_rotate:
            file.write("}\n")  # Close rotate
            

    # Don't get suggestion :)
    # get_suggestion()

