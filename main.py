import re

def move (c, m, inverse=False):
    face = m[0]
    count = int(3 if m[1] == "'" else m[1]) if len(m) > 1 else 1
    
    if inverse == True and count != 2:
        count = 3 if (count + 2) % 3 == 0 else (count + 2) % 3

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

def build_table (cube, allowed_moves, max_moves):
    p = { str(cube): [] }
    pa = [ [ { 'cube': cube, 'sequence': [] } ] ]
    
    for i in range(0, max_moves):
        pa.append([])
        for previous in pa[i]:
            for current_move in allowed_moves:
                if len(previous['sequence']) == 0 or previous['sequence'][0] != current_move:
                    current = {
                        'cube': move(previous['cube'], current_move, True), # inverse move
                        'sequence': previous['sequence'].copy()
                    }
                    current['sequence'].insert(0, current_move)
                    if str(current['cube']) not in p:
                        p[str(current['cube'])] = current['sequence']
                        pa[i + 1].append(current)
    
    # print(len(p))
    # lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # for cube, solution in p.items():
    #     lengths[len(solution)] += 1
    # print(lengths)
    
    return p

# p0 = build_table([(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)], ['U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3'], 11) # very slow!
p1 = build_table([(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)], ['U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3'], 6)
p2 = build_table([(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)], ['U1', 'U2', 'U3', 'F2', 'R2'], 13)

def move_sequence (c, s):
    for current_move in s:
        c = move(c, current_move)
    return c

scramble_sequence = "R2 F U R2 U' R U2 F' R"
print(scramble_sequence)
scramble = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]
scramble = move_sequence(scramble, scramble_sequence.split(' ')) # scramble the cube

# print(p0[str(scramble)]) # look up optimal solution
orientation_scramble = list(map(lambda n: (0, n[1]), scramble))
print(p1[str(orientation_scramble)]) # look up first phase solution
scramble = move_sequence(scramble, p1[str(orientation_scramble)]) # execute first phase solution on cube
print(p2[str(scramble)]) # look up second phase solution