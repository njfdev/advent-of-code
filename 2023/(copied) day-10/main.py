P = "input.txt"
with open(P, "r") as f:
    R = f.read()
G = R.split("\n")
H = len(G)
W = len(G[0])

O = [[0] * W for _ in range(H)]  # part 2

ax = -1
ay = -1
for i in range(H):
    for j in range(W):
        if "S" in G[i]:
            ax = i
            ay = G[i].find("S")

# rightward downward leftward upward
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
happy = ["-7J", "|LJ", "-FL", "|F7"]
Sdirs = []
for i in range(4):
    pos = dirs[i]
    bx = ax + pos[0]
    by = ay + pos[1]
    if bx >= 0 and bx <= H and by >= 0 and by <= W and G[bx][by] in happy[i]:
        Sdirs.append(i)
Svalid = 3 in Sdirs  # part 2

# rightward downward leftward upward
transform = {
    (0, "-"): 0,
    (0, "7"): 1,
    (0, "J"): 3,
    (2, "-"): 2,
    (2, "F"): 1,
    (2, "L"): 3,
    (1, "|"): 1,
    (1, "L"): 0,
    (1, "J"): 2,
    (3, "|"): 3,
    (3, "F"): 0,
    (3, "7"): 2,
}

curdir = Sdirs[0]
cx = ax + dirs[curdir][0]
cy = ay + dirs[curdir][1]
ln = 1
O[ax][ay] = 1  # Part 2
while (cx, cy) != (ax, ay):
    O[cx][cy] = 1  # Part 2
    ln += 1
    curdir = transform[(curdir, G[cx][cy])]
    cx = cx + dirs[curdir][0]
    cy = cy + dirs[curdir][1]
print("(Part 1): " + str(ln // 2))

# End Part 1
# Begin Part 2

ct = 0
for i in range(H):
    inn = False
    for j in range(W):
        if O[i][j]:
            if G[i][j] in "|JL" or (G[i][j] == "S" and Svalid):
                inn = not inn
        else:
            ct += inn
print("(Part 2): " + str(ct))
