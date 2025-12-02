import os
import pathlib
import requests
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from copy import deepcopy


def download_input(year, day):

    filename = f"inputs/day_{str(day).zfill(2)}_input.txt"

    if not os.path.exists(filename):
        url = f"https://adventofcode.com/{year}/day/{day}/input"

        with open("cookie.txt", "r") as file:
            session = file.read()

        headers = {"cookie": f"session={session}"}

        pathlib.Path("inputs").mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as file:
            file.write(requests.get(url, headers=headers).content)


def read_input(day, test=False):
    lines = [
        x.strip()
        for x in open(
            f"inputs/day_{str(day).zfill(2)}_{'test_' if test else ''}input.txt", "r"
        )
    ]

    aoc = "\n".join(deepcopy(lines))

    if "" in lines:
        end = lines.index("")

        G = [[x for x in line.strip()] for line in lines[:end]]
        lines = lines[end + 1 :]

    else:
        G = [[x for x in line.strip()] for line in lines]

    R = len(G)
    C = len(G[0])

    print(f"{lines[:5]=}")
    print(f"{R=}, {C=}")

    return aoc, lines, G, R, C


dir_dict = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
dirs = [x for x in dir_dict.values()]


def print_grid(G):
    for r, row in enumerate(G):
        str_row = ""
        for c, cell in enumerate(row):
            str_row += str(cell)
        print(str_row)
    print(*"\n")


def rotate_grid(inp):
    N = len(inp)
    M = len(inp[0])
    outp = [[] for x in range(M)]
    for i in reversed(range(N)):
        for j in range(M):
            outp[j].append(inp[i][j])
    return outp


def display_image(G):
    Y = len(G)
    X = len(G[0])

    char_dict = {".": 1, "#": 2, "O": 3, "@": 4}

    unique_chars = set(cell for row in G for cell in row)
    for char in unique_chars:
        if char not in char_dict:
            raise ValueError(f"Character '{char}' not found in char_dict.")

    arr = np.zeros((Y, X))

    use_dict = isinstance(G[0][0], str)

    for r, row in enumerate(G):
        for c, cell in enumerate(row):
            if use_dict:
                arr[r][c] = char_dict[cell]
            else:
                arr[r][c] = cell

    cmap = ListedColormap(["black", "white", "red", "blue", "green"])

    plt.imshow(arr, cmap=cmap, interpolation="nearest")
    plt.colorbar(ticks=range(len(char_dict) + 1), label="Character Mapping")
    plt.clim(0, len(char_dict))
    plt.show()
