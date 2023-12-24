# read input.txt
input = open("input.txt", "r").read().strip().splitlines()

import math
# import matrix math library
import numpy as np
from tqdm import tqdm

def parse_input(input_data):
    data = []
    for line in input_data:
        data.append([[int(num.strip()) for num in v.split(", ")] for v in line.split(" @ ")])

    return data


def hailstone_to_slope_intercept(hailstone):
    # convert to slope intercept form
    # y = mx + b
    # m = y_velocity / x_velocity
    # b = y_pos - m * x_pos

    # returns (m, b)
    return hailstone[1][1] / hailstone[1][0], hailstone[0][1] - (hailstone[1][1] / hailstone[1][0]) * hailstone[0][0]


def slope_intercept_to_standard_form(slope_intercept):
    # convert to standard form
    # ax + by = c
    # a = -m
    # b = 1
    # c = -b

    # returns (a, b, c)
    return -slope_intercept[0], 1, -slope_intercept[1]


def get_hailstone_intersection(hailstone_a_, hailstone_b_):
    hailstone_a = hailstone_a_.copy()
    hailstone_b = hailstone_b_.copy()
    # solve the linear equation system
    # for each hailstone, [0][0] is the x pos, [0][1] is the y pos, [1][0] is the x velocity, [1][1] is the y velocity
    
    # if the velocities are the same, check if y_intercept is the same
    hailstone_a_slope_intercept = hailstone_to_slope_intercept(hailstone_a)
    hailstone_b_slope_intercept = hailstone_to_slope_intercept(hailstone_b)
    if hailstone_a_slope_intercept[0] == hailstone_b_slope_intercept[0]:
        if hailstone_a_slope_intercept[1] == hailstone_b_slope_intercept[1]:
            return math.inf
        return None
    
    # convert to standard form
    hailstone_a_standard_form = slope_intercept_to_standard_form(hailstone_a_slope_intercept)
    hailstone_b_standard_form = slope_intercept_to_standard_form(hailstone_b_slope_intercept)

    # solve the linear equation system using cramer's rule
    # ax + by = e
    # cx + dy = f
    # x = (ed - bf) / (ad - bc)
    # y = (af - ec) / (ad - bc)

    a = hailstone_a_standard_form[0]
    b = hailstone_a_standard_form[1]
    e = hailstone_a_standard_form[2]
    c = hailstone_b_standard_form[0]
    d = hailstone_b_standard_form[1]
    f = hailstone_b_standard_form[2]

    try:
        x = np.linalg.det([[e, b], [f, d]]) / np.linalg.det([[a, b], [c, d]])
        y = np.linalg.det([[a, e], [c, f]]) / np.linalg.det([[a, b], [c, d]])
        return (-x, -y)
    except ZeroDivisionError:
        return None



def get_intersections_within_test_area(data, min_val, max_val):
    intersections = []
    already_tested_pairs = []
    for hailstone_a in tqdm(data):
        for hailstone_b in data:
            if hailstone_a == hailstone_b:
                continue
            if [hailstone_a, hailstone_b] in already_tested_pairs or [hailstone_b, hailstone_a] in already_tested_pairs:
                continue
            already_tested_pairs.append([hailstone_a, hailstone_b])
            # get intersection
            intersection = get_hailstone_intersection(hailstone_a, hailstone_b)
            if intersection is None:
                continue
            if intersection is math.inf:
                intersections.append(hailstone_a[0])
                continue
            if intersection[0] >= min_val and intersection[0] <= max_val and intersection[1] >= min_val and intersection[1] <= max_val:
                # if intersection is in the direction of the velocity
                if (intersection[0] - hailstone_a[0][0]) * hailstone_a[1][0] >= 0 and (intersection[1] - hailstone_a[0][1]) * hailstone_a[1][1] >= 0:
                  if (intersection[0] - hailstone_b[0][0]) * hailstone_b[1][0] >= 0 and (intersection[1] - hailstone_b[0][1]) * hailstone_b[1][1] >= 0:
                    intersections.append(intersection)
    return intersections


def part1(input):
    data = parse_input(input)

    return len(get_intersections_within_test_area(data, 200000000000000, 400000000000000))


print("(Part 1) Intersections within test area:", part1(input))

# not my code
import numpy as np
from sympy import Symbol
from sympy import solve_poly_system

handle = open("input.txt","r")

shards = []
for line in handle:
  pos, vel = line.strip().split(" @ ")
  px,py,pz = pos.split(", ")
  vx,vy,vz = vel.split(", ")
  shards.append((int(px),int(py),int(pz),int(vx),int(vy),int(vz)))

#Part 2 uses SymPy. We set up a system of equations that describes the intersections, and solve it.
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
vx = Symbol('vx')
vy = Symbol('vy')
vz = Symbol('vz')

equations = []
t_syms = []
#the secret sauce is that once you have three shards to intersect, there's only one valid line
#so we don't have to set up a huge system of equations that would take forever to solve. Just pick the first three.
for idx,shard in enumerate(shards[:3]):
  #vx is the velocity of our throw, xv is the velocity of the shard we're trying to hit. Yes, this is a confusing naming convention.
  x0,y0,z0,xv,yv,zv = shard
  t = Symbol('t'+str(idx)) #remember that each intersection will have a different time, so it needs its own variable

  #(x + vx*t) is the x-coordinate of our throw, (x0 + xv*t) is the x-coordinate of the shard we're trying to hit.
  #set these equal, and subtract to get x + vx*t - x0 - xv*t = 0
  #similarly for y and z
  eqx = x + vx*t - x0 - xv*t
  eqy = y + vy*t - y0 - yv*t
  eqz = z + vz*t - z0 - zv*t

  equations.append(eqx)
  equations.append(eqy)
  equations.append(eqz)
  t_syms.append(t)

#To my great shame, I don't really know how this works under the hood.
result = solve_poly_system(equations,*([x,y,z,vx,vy,vz]+t_syms))
print("(Copied - Part 2) Initial Position Sum:", result[0][0]+result[0][1]+result[0][2]) #part 2 answer
