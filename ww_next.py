import copy


def adjcheck(x, y, array, rowsno, colsno):
    total = 0
    if y - 1 >= 0:  # y-1 won't be out of bounds
        if x - 1 >= 0:  # x-1 won't be out of bounds
            if array[y - 1][x - 1] == 1:  # top left
                total += 1
        if array[y - 1][x] == 1:  # top middle
            total += 1
        if x + 1 <= (colsno - 1):  # x+1 won't be out of bounds
            if array[y - 1][x + 1] == 1:  # top right
                total += 1

    if x - 1 >= 0:  # x-1 won't be out of bounds
        if array[y][x - 1] == 1:  # middle left
            total += 1

    if x + 1 <= (colsno - 1):  # x+1 won't be out of bounds
        if array[y][x + 1] == 1:  # middle right
            total += 1

    if y + 1 <= (rowsno - 1):  # y+1 won't be out of bounds
        if x - 1 >= 0:  # x-1 won't be out of bounds
            if array[y + 1][x - 1] == 1:  # bottom left
                total += 1
        if array[y + 1][x] == 1:  # bottom middle
            total += 1
        if x + 1 <= (colsno - 1):  # x+1 won't be out of bounds
            if array[y + 1][x + 1] == 1:  # bottom right
                total += 1

    if 0 < total < 3:
        return True
    else:
        return False


def main(array):
    rowsno = (len(array))  # y coord
    colsno = (len(array[0]))  # x coord

    changed = copy.deepcopy(array)

    for y in range(rowsno):
        for x in range(colsno):
            if (array[y][x] == 1) or (array[y][x] == 2):
                changed[y][x] += 1
            if array[y][x] == 3:
                if adjcheck(x, y, array, rowsno, colsno):
                    changed[y][x] = 1
                else:
                    changed[y][x] = 3

    return changed
