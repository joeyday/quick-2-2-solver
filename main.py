import re

def move (c, m):
    face = m[0]
    count = int(m[1])

    for i in range(0, count):
        if face == 'R':
            c = [
                (c[5][0], (c[5][1] + 2) % 3),
                (c[1][0], c[1][1]),
                (c[2][0], c[2][1]),
                (c[0][0], (c[0][1] + 1) % 3),
                (c[3][0], (c[3][1] + 2) % 3),
                (c[4][0], (c[4][1] + 1) % 3),
                (c[6][0], c[6][1])
            ]
    
        if face == 'U':
            c = [
                (c[3][0], c[3][1]),
                (c[0][0], c[0][1]),
                (c[1][0], c[1][1]),
                (c[2][0], c[2][1]),
                (c[4][0], c[4][1]),
                (c[5][0], c[5][1]),
                (c[6][0], c[6][1])
            ]
    
        if face == 'F':
            c = [
                (c[1][0], (c[1][1] + 1) % 3),
                (c[6][0], (c[6][1] + 2) % 3),
                (c[2][0], c[2][1]),
                (c[3][0], c[3][1]),
                (c[4][0], c[4][1]),
                (c[0][0], (c[0][1] + 2) % 3),
                (c[5][0], (c[5][1] + 1) % 3)
            ]

    return c
    
def move_inverse (c, m):
    m = m.replace('1', 'x')
    m = m.replace('3', '1')
    m = m.replace('x', '3')
    return move(c, m)

def p1_str (cube):
    return ''.join("%s" % str(x[1]) for x in cube)

def p2_str (cube):
    return ''.join("%s" % ''.join(map(str, x)) for x in cube)

def build_table (allowed_moves, str_fn, max_moves):
    cube = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
    p = { str_fn(cube): [] }
    pa = [ [ { 'cube': cube, 'sequence': [] } ] ]
    
    for i in range(0, max_moves):
        pa.append([])
        for previous in pa[i]:
            for current_move in allowed_moves:
                if len(previous['sequence']) == 0 or previous['sequence'][0] != current_move:
                    current = {
                        'cube': move_inverse(previous['cube'], current_move),
                        'sequence': previous['sequence'].copy()
                    }
                    current['sequence'].insert(0, current_move)
                    if str_fn(current['cube']) not in p:
                        p[str_fn(current['cube'])] = current['sequence']
                        pa[i + 1].append(current)
    
    # print(len(p))
    # lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # for cube, solution in p.items():
    #     lengths[len(solution)] += 1
    # print(lengths)
    
    return p

# p0 = build_table([ 'U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3' ], str, 11) # very slow!
p1 = build_table([ 'U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3' ], p1_str, 6) # build lookup table for phase 1
p2 = build_table([ 'U1', 'U2', 'U3', 'F2', 'R2' ], p2_str, 13) # build lookup table for phase 2

def move_sequence (c, s):
    s = s.replace("'", '3')
    s = re.sub(r'([RUF])\b', r'\g<1>1', s)
    for current_move in s.split(' '):
        c = move(c, current_move)
    return c

scramble_sequence = "U2 R2 U R' U2 R' U2 F' R'"
print(scramble_sequence)
scramble = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
scramble = move_sequence(scramble, scramble_sequence) # scramble the cube

# print(p0[str(scramble)]) # look up optimal solution
print(p1[p1_str(scramble)]) # look up first phase solution
for current_move in p1[p1_str(scramble)]:
    scramble = move(scramble, current_move) #execute first phase solution on cube
print(p2[p2_str(scramble)]) # look up second phase solution