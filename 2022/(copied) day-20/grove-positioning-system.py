from collections import defaultdict

InputList = []
with open("encrypted-coords.txt", "r") as data:
    for t in data:
        Line = t.strip()
        Line = int(Line)
        InputList.append(Line)

# this confirms that the values are not unique
InputSet = set(InputList)
# print(len(InputList), len(InputSet))

Len = len(InputList)
InputDict = defaultdict()
for n, v in enumerate(InputList):
    InputDict[n] = v
    if v == 0:
        ZeroIndex = n

NeighborDict = defaultdict()
for v in range(Len):
    NewNeighbors = ((v - 1) % Len, (v + 1) % Len)
    NeighborDict[v] = NewNeighbors

for v in range(Len):
    # Discovering this minus 1 took some doing
    Movement = InputDict[v] % (Len - 1)
    if Movement == 0:
        continue
    StartBackNeighbor, StartForwardNeighbor = NeighborDict[v]
    CurrentSpot = v
    NextSpot = StartForwardNeighbor

    for f in range(Movement):
        _, MidFN = NeighborDict[NextSpot]
        CurrentSpot = NextSpot
        NextSpot = MidFN
    EndSpot = CurrentSpot

    SBNB, _ = NeighborDict[StartBackNeighbor]
    NeighborDict[StartBackNeighbor] = (SBNB, StartForwardNeighbor)

    _, SFNF = NeighborDict[StartForwardNeighbor]
    NeighborDict[StartForwardNeighbor] = (StartBackNeighbor, SFNF)

    EndSpotBack, EndSpotForward = NeighborDict[EndSpot]
    NeighborDict[EndSpot] = (EndSpotBack, v)

    NeighborDict[v] = (EndSpot, EndSpotForward)

    _, ESFF = NeighborDict[EndSpotForward]
    NeighborDict[EndSpotForward] = (v, ESFF)

Part1Answer = 0
CurrentSpot = ZeroIndex
_, NextSpot = NeighborDict[CurrentSpot]
for t in range(3):
    for f in range(1000):
        _, MidFN = NeighborDict[NextSpot]
        CurrentSpot = NextSpot
        NextSpot = MidFN
    Part1Answer += InputDict[CurrentSpot]

########Part 2
DecryptionKey = 811589153
for v in range(Len):
    Rea = InputDict[v]
    InputDict[v] = Rea * DecryptionKey

for v in range(Len):
    NewNeighbors = ((v - 1) % Len, (v + 1) % Len)
    NeighborDict[v] = NewNeighbors

for t in range(10):
    print(t)
    for v in range(Len):
        Movement = InputDict[v] % (Len - 1)
        if Movement == 0:
            continue
        StartBackNeighbor, StartForwardNeighbor = NeighborDict[v]
        CurrentSpot = v
        NextSpot = StartForwardNeighbor

        for f in range(Movement):
            _, MidFN = NeighborDict[NextSpot]
            CurrentSpot = NextSpot
            NextSpot = MidFN
        EndSpot = CurrentSpot

        SBNB, _ = NeighborDict[StartBackNeighbor]
        NeighborDict[StartBackNeighbor] = (SBNB, StartForwardNeighbor)

        _, SFNF = NeighborDict[StartForwardNeighbor]
        NeighborDict[StartForwardNeighbor] = (StartBackNeighbor, SFNF)

        EndSpotBack, EndSpotForward = NeighborDict[EndSpot]
        NeighborDict[EndSpot] = (EndSpotBack, v)

        NeighborDict[v] = (EndSpot, EndSpotForward)

        _, ESFF = NeighborDict[EndSpotForward]
        NeighborDict[EndSpotForward] = (v, ESFF)


Part2Answer = 0
CurrentSpot = ZeroIndex
_, NextSpot = NeighborDict[CurrentSpot]
for t in range(3):
    for f in range(1000):
        _, MidFN = NeighborDict[NextSpot]
        CurrentSpot = NextSpot
        NextSpot = MidFN
    Part2Answer += InputDict[CurrentSpot]
    print(InputDict[CurrentSpot])


print(f"{Part1Answer = }")
print(f"{Part2Answer = }")
