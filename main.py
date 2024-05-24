import re

def move (c, m):
    if m == 'R1':
        return [
            (c[5][0], (c[5][1] + 2) % 3),
            (c[1][0], c[1][1]),
            (c[2][0], c[2][1]),
            (c[0][0], (c[0][1] + 1) % 3),
            (c[3][0], (c[3][1] + 2) % 3),
            (c[4][0], (c[4][1] + 1) % 3),
            (c[6][0], c[6][1])
        ]

    if m == 'R2':
        return move(move(c, 'R1'), 'R1')

    if m == 'R3':
        return move(move(move(c, 'R1'), 'R1'), 'R1')

    if m == 'U1':
        return [
            (c[3][0], c[3][1]),
            (c[0][0], c[0][1]),
            (c[1][0], c[1][1]),
            (c[2][0], c[2][1]),
            (c[4][0], c[4][1]),
            (c[5][0], c[5][1]),
            (c[6][0], c[6][1])
        ]

    if m == 'U2':
        return move(move(c, 'U1'), 'U1')

    if m == 'U3':
        return move(move(move(c, 'U1'), 'U1'), 'U1')

    if m == 'F1':
        return [
            (c[1][0], (c[1][1] + 1) % 3),
            (c[6][0], (c[6][1] + 2) % 3),
            (c[2][0], c[2][1]),
            (c[3][0], c[3][1]),
            (c[4][0], c[4][1]),
            (c[0][0], (c[0][1] + 2) % 3),
            (c[5][0], (c[5][1] + 1) % 3)
        ]

    if m == 'F2':
        return move(move(c, 'F1'), 'F1')
    
    if m == 'F3':
        return move(move(move(c, 'F1'), 'F1'), 'F1')

def move_inverse (c, m):
    m = m.replace('1', 'x')
    m = m.replace('3', '1')
    m = m.replace('x', '3')
    return move(c, m)

def move_sequence (c, s):
    s = s.replace("'", '3')
    s = re.sub(r'([RUF])\b', r'\g<1>1', s)
    for current_move in s.split(' '):
        c = move(c, current_move)
    return c

def p1_str (cube):
    return ''.join("%s" % str(x[1]) for x in cube)

def p2_str (cube):
    return ''.join("%s" % ''.join(map(str, x)) for x in cube)

cube = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
allowed_moves = [ 'U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3' ]
p1 = { p1_str(cube): [] }
p1a = [ [ { 'cube': cube, 'sequence': [] } ] ]

for i in range(1, 14): # ranges don't include stop value, so this goes from 1 to 13
    p1a.append([])
    for previous in p1a[i - 1]:
        for current_move in allowed_moves:
            if len(previous['sequence']) == 0 or previous['sequence'][0] != current_move:
                current = {
                    'cube': move_inverse(previous['cube'], current_move),
                    'sequence': previous['sequence'].copy()
                }
                current['sequence'].insert(0, current_move)
                if p1_str(current['cube']) not in p1:
                    p1[p1_str(current['cube'])] = current['sequence']
                    p1a[i].append(current)

# print(len(p1))
# print(dr_tree)

# lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# for cube, solution in p1.items():
#     lengths[len(solution)] += 1
# print(lengths)

cube = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
allowed_moves = [ 'U1', 'U2', 'U3', 'F2', 'R2' ]
p2 = { p2_str(cube): [] }
p2a = [ [ { 'cube': cube, 'sequence': [] } ] ]

for i in range(1, 14): # ranges don't include stop value, so this goes from 1 to 13
    p2a.append([])
    for previous in p2a[i - 1]:
        for current_move in allowed_moves:
            if len(previous['sequence']) == 0 or previous['sequence'][0] != current_move:
                current = {
                    'cube': move_inverse(previous['cube'], current_move),
                    'sequence': previous['sequence'].copy()
                }
                current['sequence'].insert(0, current_move)
                if p2_str(current['cube']) not in p2:
                    p2[p2_str(current['cube'])] = current['sequence']
                    p2a[i].append(current)
    
# print(len(p2))
# print(dr_tree)

# lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# for cube, solution in p2.items():
#     lengths[len(solution)] += 1
# print(lengths)


scramble = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
scramble = move_sequence(scramble, "R U2 R' F2 R2 F2 U F' U2")
print(p1[p1_str(scramble)])
for current_move in p1[p1_str(scramble)]:
    scramble = move(scramble, current_move)
print(p2[p2_str(scramble)])