import os

grid = []

with open("tree-heights.txt") as f:
    for line in f:
        grid.append([int(x) for x in line.strip()])

counter = 0
grid_line_counter = 0

# ~~~~~~~~Part 1


def is_visible(xpos, ypos):
    visible_top = False
    visible_bottom = False
    visible_right = False
    visible_left = False

    # Checking Top
    if grid[xpos - 1][ypos] < grid[xpos][ypos]:
        visible_top = True
        for x in range(xpos - 1, -1, -1):
            if grid[x][ypos] >= grid[xpos][ypos]:
                visible_top = False
                break
    # Checking Left
    if grid[xpos][ypos - 1] < grid[xpos][ypos]:
        visible_left = True
        for y in range(ypos - 1, -1, -1):
            if grid[xpos][y] >= grid[xpos][ypos]:
                visible_left = False
                break
    # Checking Right
    if grid[xpos][ypos + 1] < grid[xpos][ypos]:
        visible_right = True
        for i in range(ypos + 1, len(grid[xpos])):
            if grid[xpos][i] >= grid[xpos][ypos]:
                visible_right = False
                break
    # Checking Bottom
    if grid[xpos + 1][ypos] < grid[xpos][ypos]:
        visible_bottom = True
        for j in range(xpos + 1, len(grid)):
            if grid[j][ypos] >= grid[xpos][ypos]:
                visible_bottom = False
                break

    if (
        visible_top == True
        or visible_bottom == True
        or visible_left == True
        or visible_right == True
    ):
        return True
    else:
        return False


for x in range(len(grid)):
    for y in range(len(grid[x])):
        # print(grid[x][y])
        if x != 0 and y != 0 and x != (len(grid) - 1) and y != (len(grid[x]) - 1):
            # if top is greater than current val, add one to counter. Else: loop through until you find lower value or until end of index.
            check_pos = is_visible(x, y)
            if check_pos == True:
                counter += 1
        else:
            grid_line_counter += 1

print(counter + grid_line_counter)
