from tkinter import *

flat_diags = True
real_diags = True
optim_sym = False

depth = 27

n = 3
plateau = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]

def prim_stringify(p):
    s = ""
    for z in range(n):
        for x in range(n):
            for y in range(n):
                v = p[z][x][y]
                if v is None:
                    s += "."
                elif v:
                    s += "X"
                else:
                    s += "O"
    return s

# plateau[z][x][y]
# None, True, False

# z stays z
# x goes to y
# y goes to -x

def rotate(p):
    new_p = []
    for z in range(n):
        new_p.append(list(zip(*p[z][::-1])))
    return new_p

def sym_axial(p):
    new_p = []
    for z in range(n):
        line = []
        for x in range(n):
            line.append(list(reversed(p[z][x])))
        new_p.append(line)
    return new_p

def available(plateau):
    a = []
    for x in range(n):
        for y in range(n):
            z = 0
            while z < n and plateau[z][x][y] is not None:
                z += 1
            if z < n:
                a.append((x, y, z))
    return a

def print2D(p):
    s = ""
    for x in range(n):
        for y in range(n):
            if p[x][y] is None:
                s += "."
            elif p[x][y]:
                s += "X"
            else:
                s += "O"
        s += "\n"
    print(s)

def print_board(p):
    for z in range(2, -1, -1):
        print(z)
        print2D(p[z])

def stringify(p):
    m = prim_stringify(p)
    if not optim_sym:
        return m
    for _ in range(3):
        p = rotate(p)
        m = min(m, prim_stringify(p))
    p = sym_axial(p)
    m = min(m, prim_stringify(p))
    for _ in range(3):
        p = rotate(p)
        m = min(m, prim_stringify(p))
    return m

def scoreTriple(a, b, c):
    if a is not None and b is not None and c is not None:
        if a and b and c:
            return 1
        elif (not a) and (not b) and (not c):
            return -1
    return 0

def score2D(p):
    c = 0
    for i in range(n):
        c += scoreTriple(p[i][0], p[i][1], p[i][2])
        c += scoreTriple(p[0][i], p[1][i], p[2][i])

    # Diagonals
    c += scoreTriple(p[0][0], p[1][1], p[2][2])
    c += scoreTriple(p[0][2], p[1][1], p[2][0])

    return c

# No diagonals
def scoreHeight(p):
    c = 0
    for x in range(n):
        for y in range(n):
            c += scoreTriple(p[0][x][y], p[1][x][y], p[2][x][y])
    return c

def scoreWallDiags(p):
    c = 0
    for i in range(n):
        c += scoreTriple(p[0][i][0], p[1][i][1], p[2][i][2])
        c += scoreTriple(p[0][i][2], p[1][i][1], p[2][i][0])
    for i in range(n):
        c += scoreTriple(p[0][0][i], p[1][1][i], p[2][2][i])
        c += scoreTriple(p[0][2][i], p[1][1][i], p[2][0][i])
    return c

def scoreRealDiags(p):
    c = 0
    c += scoreTriple(p[0][0][0], p[1][1][1], p[2][2][2])
    c += scoreTriple(p[2][0][0], p[1][1][1], p[0][2][2])
    c += scoreTriple(p[0][0][2], p[1][1][1], p[2][2][0])
    c += scoreTriple(p[2][0][2], p[1][1][1], p[0][2][0])
    return c

def score3D(p):
    c = 0

    # Only per board
    for z in range(n):
        c += score2D(p[z])

    c += scoreHeight(p)

    if flat_diags:
        c += scoreWallDiags(p)
    if real_diags:
        c += scoreRealDiags(p)

    return c

scores = {}
succ = {}

import copy

# Stop game at 1 won

def solvePlateau(p, depth, turn=True):
    print("Solving...", depth)
    # print_board(p)
    if depth == 0:
        return score3D(p)


    s = stringify(p)
    if s not in scores:
        # turn = True --> max
        # turn = False --> min
        m = 10000000
        if turn:
            m = -10000000
        l = available(p)
        done = False
        for (x, y, z) in l:
            assert(p[z][x][y] is None)
            p[z][x][y] = turn
            sc = score3D(p)
            if (turn and sc > 0) or (not turn and sc < 0):
                scores[s] = sc
                succ[s] = copy.deepcopy(p)
                scores[stringify(p)] = sc
                done = True
            p[z][x][y] = None

        if not done:
            for (x, y, z) in l:
                p[z][x][y] = turn
                r = solvePlateau(p, depth - 1, not turn)
                if turn:
                    # Max
                    if r > m:
                        succ[s] = copy.deepcopy(p)
                        m = r
                        if r > 0:
                            p[z][x][y] = None
                            break
                else:
                    # Min
                    if r < m:
                        succ[s] = copy.deepcopy(p)
                        m = r
                        if r < 0:
                            p[z][x][y] = None
                            break
                p[z][x][y] = None
            scores[s] = m
    return scores[s]

#plateau[0][1][1] = True
#plateau[0][2][0] = False
#plateau[1][1][1] = True
#plateau[0][2][1] = False

# plateau[0][0][0] = True
# plateau[0][1][1] = False
#plateau[1][1][1] = True

print(solvePlateau(plateau, depth, True))

p = plateau
s = stringify(p)
#print_board(p)
while s in succ:
    print("-----------------------------------")
    #break
    p = succ[s]
    s = stringify(p)
    #print_board(p)

#print_board(plateau)
#print_board(sym_axial(plateau))

for x in range(n):
    break
    for y in range(n):
        p = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]
        p[0][x][y] = True
        if scores[stringify(p)] > 0:
            print2D(p[0])

# from tkinter import *
from tkinter.ttk import *

# creating main tkinter window/toplevel
master = Tk()

stack = [[(0, 0, 0)]]

p = [p]

def count_x_o(p):
    c_x = 0
    c_o = 0
    for z in range(n):
        for x in range(n):
            for y in range(n):
                r = p[z][x][y]
                if r is not None:
                    if r:
                        c_x += 1
                    else:
                        c_o += 1
    return (c_x, c_o)

# Considering we are X
# Real p
def remaining_before_death(p, turn):
    print("Remaining", stringify(p), turn)
    if score3D(p) > 0:
        return 0
    if turn:
        return 1 + remaining_before_death(succ[stringify(p)], False)
    m = 0
    pp = [[[p[z][x][y] for y in range(n)] for x in range(n)] for z in range(n)]
    for (x, y, z) in available(p):
        pp[z][x][y] = False
        m = max(m, remaining_before_death(pp, True))
        pp[z][x][y] = None
    return m + 1

def update_board_tk(infos, labels, labels_var, master, p):

    for z in range(3):
        for x in range(n):
            for y in range(n):
                s = ""
                if p[0][z][x][y] is None:
                    s = "."
                elif p[0][z][x][y]:
                    s = "X"
                else:
                    s = "O"
                labels_var[z][x][y].set(s)
                if stack[0][-1] == (z, x, y):
                    labels[z][x][y]["background"] = "yellow"
                else:
                    labels[z][x][y]["background"] = master.cget("bg")

    infos[0].set(scores[stringify(p[0])])
    infos[1].set(score3D(p[0]))
    (c_x, c_o) = count_x_o(p[0])
    print(c_x, c_o)
    infos[2].set(remaining_before_death(p[0], c_x == c_o))

def init_board_tk(infos, labels, labels_var, master, p):

    def prep(z, x, y, turn):
        def f(event):
            p[0][z][x][y] = turn
            stack[0].append((z, x, y))
            update_board_tk(infos, labels, labels_var, master, p)
        return f

    for z in range(3):
        for x in range(n):
            for y in range(n):
                l = labels[z][x][y]
                l.bind('<Button-1>', prep(z, x, y, True))
                l.bind('<Button-3>', prep(z, x, y, False))
                l.config(font=("Courier", 44))
                l.grid(row = y + (2 - z) * 4, column = x)

    for x in range(n):
        for z in [3, 7, 11]:
            l = Label(master, text = "-")
            l.config(font=("Courier", 44))
            l.grid(row = z, column = x)

    def solveNext():
        old_p = p[0]
        p[0] = succ[stringify(p[0])]
        # Highlight first difference
        for z in range(n):
            for x in range(n):
                for y in range(n):
                    if p[0][z][x][y] != old_p[z][x][y]:
                        stack[0].append((z, x, y))
        update_board_tk(infos, labels, labels_var, master, p)

    button = Button(master, text="Show next move", command=solveNext)
    button.grid(row = 15, column = 0)

    def reset():
        p[0] = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]
        update_board_tk(infos, labels, labels_var, master, p)

    def cancel():
        (z, x, y) = stack[0][-1]
        p[0][z][x][y] = None
        stack[0] = stack[0][:-1]
        update_board_tk(infos, labels, labels_var, master, p)

    button = Button(master, text="Reset board", command=reset)
    button.grid(row = 15, column = 1)

    button = Button(master, text="Cancel last move", command=cancel)
    button.grid(row = 15, column = 2)

labels_var = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]
labels = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]
for z in range(n):
    for x in range(n):
        for y in range(n):
            v = StringVar()
            labels_var[z][x][y] = v
            l = Label(master, textvariable = v)
            labels[z][x][y] = l

infos = []
for i in range(3):
    v = StringVar()
    infos.append(v)
    l = Label(master, textvariable = v)
    l.config(font=("Courier", 44))
    l.grid(row = 16, column = i)
    
# infinite loop which can be terminated by keyboard
# or mouse interrupt
init_board_tk(infos, labels, labels_var, master, p)
update_board_tk(infos, labels, labels_var, master, p)

mainloop()
