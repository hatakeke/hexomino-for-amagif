import numpy as np
from itertools import permutations, product

arrays = np.array([
    [
        [1, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ], [
        [1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ], [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], [
        [0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
])

colors = [
    "181818",  
    "f94144",  
    "f3722c",  
    "f9c74f",  
    "92d050",  
    "00b050",  
    "00b0f0",  
    "0070ff",  
    "673AB7",  
    "ff70a6",  
    "ffb3c1",  
    "e438d4"   
]


ROW_MAX = 6
COL_MAX = 11
NUM_PIECE = arrays.shape[0]
NUM_ROWS = arrays.shape[1]
NUM_COLUMNS = arrays.shape[2]

def paint_outputs(color_str):
    r, g, b = int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m■\033[0m"

# 最も左上の 1 or 0 を検出して座標を返す
def upper_left(array, boolen):
    for col in range(array.shape[1]):
        for row in range(array.shape[0]):
            if array[row][col] == boolen:
                return row, col
    return -1, -1

def put_check(frame, array):
    at_row, at_col = upper_left(frame, 0)
    upper_row, left_col = upper_left(array, 1)
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):
            if array[row][col]:
                if (row - upper_row + at_row < 0) or (row - upper_row + at_row >= ROW_MAX) or (col - left_col + at_col >= COL_MAX):
                    return False
                elif frame[row - upper_row + at_row][col - left_col + at_col] > 0:
                    return False
    return True

def put_brock(frame, array, sequencal):
    at_row, at_col = upper_left(frame, 0)
    upper_row, left_col = upper_left(array, 1)
    new_frame = np.copy(frame)
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS):
            if array[row][col]:
                new_frame[row - upper_row + at_row][col - left_col + at_col] = sequencal + 1
    return new_frame

def draw_broks(frame):
    print("\033[2J\033[H", end="")
    for row in range(ROW_MAX):
        for col in range(COL_MAX):
            print(paint_outputs(colors[frame[row][col]]), end=" ")
        print("")

def enumerate_brocks(i_list, frame, seq, rot):
    pass_list_new = []
    for i in i_list:
        for k in range(4):
            rot_array = np.rot90(arrays[i], k)
            if put_check(frame, rot_array):
                pass_list_new.append((seq + [i], rot + [k]))
    if pass_list_new == []:
        return False
    else:
        return make_sequence(pass_list_new)

def make_sequence(pass_list):
    for seq, rot in pass_list:
        frame = np.zeros((ROW_MAX, COL_MAX), dtype=int)
        i_list = list(range(NUM_PIECE))
        for i, k in zip(seq, rot):
            rot_array = np.rot90(arrays[i], k)
            frame = put_brock(frame, rot_array, i)
            i_list.remove(i)
            draw_broks(frame)
        if len(i_list) == 0:
            return True
        else:
            if enumerate_brocks(i_list, frame, seq, rot):
                return True
    return False

def main():
    frame = np.zeros((ROW_MAX, COL_MAX), dtype=int)
    i_list = list(range(NUM_PIECE))
    if enumerate_brocks(i_list, frame, [], []):
        print("")
        print(">>> Result <<<")
        print("Amakawa gift get!")
    else:
        print("")
        print(">>> Result <<<")
        print("You lose.")

    print("")
    print(">>> Brocks <<<")
    for row in range(NUM_ROWS):
        for i in range(NUM_PIECE):
            for col in range(NUM_COLUMNS):
                if arrays[i][row][col]:
                    print(paint_outputs(colors[i+1]), end=" ")
                else:
                    print(" ", end=" ")
            print(" ", end=" ")
        print("")

# 実行
main()