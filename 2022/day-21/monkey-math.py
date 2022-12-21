#!/usr/bin/env python3

import math
import os
import random
import re
import sys

lines = []

file_name = "monkeys.txt"
with open(file_name, "r") as f:
    lines = [l.strip() for l in f.readlines() if len(l.strip()) > 0]


class Node:
    def __init__(self):
        self.name = None
        self.op = None
        self.l = None
        self.r = None
        self.v = None
        self.h = None
        self.res_l = None
        self.res_r = None


nodes = {}
for l in lines:
    n = Node()
    n.name = l.split(": ")[0]
    if len(l[6:].split(" ")) == 1:
        n.v = int(l[6:].split(" ")[0])
    else:
        n.l = l[6:].split(" ")[0]
        n.op = "//" if l[6:].split(" ")[1] == "/" else l[6:].split(" ")[1]
        n.r = l[6:].split(" ")[2]

    nodes[n.name] = n

for name, n in nodes.items():
    if n.v is not None:
        continue
    n.l = nodes[n.l]
    n.r = nodes[n.r]


def traversal(n):
    if n.v is not None:
        if n.name == "humn":
            n.h = "h"
        return (n.v, n.h)

    l = traversal(n.l)
    r = traversal(n.r)

    if l[1] is not None:
        n.h = "l"
    if r[1] is not None:
        n.h = "r"

    n.res_l = l[0]
    n.res_r = r[0]

    return (eval(f"{n.res_l} {n.op} {n.res_r}"), n.h)


def inv(expr, a, b):
    m = {
        "a = x + b": f"{a} -  {b}",
        "a = x - b": f"{a} +  {b}",
        "a = x * b": f"{a} // {b}",
        "a = x // b": f"{a} *  {b}",
        "a = b + x": f"{a} -  {b}",
        "a = b - x": f"{b} -  {a}",
        "a = b * x": f"{a} // {b}",
        "a = b // x": f"{b} // {a}",
    }

    return eval(m[expr])


def set_humn(n, v=None):
    if n.name == "humn":
        return v

    new_v = v
    if n.name == "root":
        new_v = n.res_r if n.h == "l" else n.res_l
    else:
        new_v = (
            inv(f"a = x {n.op} b", v, n.res_r)
            if n.h == "l"
            else inv(f"a = b {n.op} x", v, n.res_l)
        )

    if n.h == "l":
        return set_humn(n.l, new_v)
    else:
        return set_humn(n.r, new_v)


print(traversal(nodes["root"])[0])
print(set_humn(nodes["root"]))
