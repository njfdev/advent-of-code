import os

grid = []
tree_line = []

with open("tree-heights.txt") as f:
    for line in f:
        grid.append([int(x) for x in line.strip()])

# ~~~~~~~~~Part 2


def tree_view(xpos, ypos):
    tree_limit_top = 0
    tree_limit_bottom = 0
    tree_limit_right = 0
    tree_limit_left = 0

    # Checking Top
    for x in range(xpos - 1, -1, -1):
        if grid[x][ypos] < grid[xpos][ypos]:
            tree_limit_top += 1
        elif grid[x][ypos] >= grid[xpos][ypos]:
            tree_limit_top += 1
            break
    # Checking Left
    for y in range(ypos - 1, -1, -1):
        if grid[xpos][y] < grid[xpos][ypos]:
            tree_limit_left += 1
        elif grid[xpos][y] >= grid[xpos][ypos]:
            tree_limit_left += 1
            break
    # Checking Right
    for i in range(ypos + 1, len(grid[xpos])):
        if grid[xpos][i] < grid[xpos][ypos]:
            tree_limit_right += 1
        elif grid[xpos][i] >= grid[xpos][ypos]:
            tree_limit_right += 1
            break
    # Checking Bottom
    for j in range(xpos + 1, len(grid)):
        if grid[j][ypos] < grid[xpos][ypos]:
            tree_limit_bottom += 1
        elif grid[j][ypos] >= grid[xpos][ypos]:
            tree_limit_bottom += 1
            break

    return tree_limit_top * tree_limit_left * tree_limit_bottom * tree_limit_right


for x in range(len(grid)):
    for y in range(len(grid[x])):
        if x != 0 and y != 0 and x != (len(grid) - 1) and y != (len(grid[x]) - 1):
            tree_line.append(tree_view(x, y))


print(max(tree_line))
