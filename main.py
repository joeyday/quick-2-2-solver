# The cube itself is represented with a list of tuples; The indices 0–6
# correspond to the positions UBL, UBR, UFR, UFL, DBR, DFR, DFL; since the
# only moves are U, F, and R, piece DBL is fixed in place and can neither
# be permuted nor oriented, so no sense in keeping track of it; the first
# value in the tuple is which piece is in the position; the second value
# in the tuple is how the piece is oriented on the U/D axis (0 = oriented,
# 1 = twisted clockwise, 2 = twisted counter-clockwise)
cube = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)]

def do_move (cube, move, inverse=False):
    face = move[0]
    turn_count = int(3 if move[1] == "'" else move[1]) if len(move) > 1 else 1

    if inverse == True and turn_count != 2:
        turn_count = 3 if (turn_count + 2) % 3 == 0 else (turn_count + 2) % 3

    for i in range(0, turn_count):
        if face == 'U':
            cube = [
                (cube[3][0], cube[3][1]),
                (cube[0][0], cube[0][1]),
                (cube[1][0], cube[1][1]),
                (cube[2][0], cube[2][1]),
                (cube[4][0], cube[4][1]),
                (cube[5][0], cube[5][1]),
                (cube[6][0], cube[6][1])
            ]

        if face == 'F':
            cube = [
                (cube[0][0], cube[0][1]),
                (cube[1][0], cube[1][1]),
                (cube[3][0], (cube[3][1] + 1) % 3),
                (cube[6][0], (cube[6][1] + 2) % 3),
                (cube[4][0], cube[4][1]),
                (cube[2][0], (cube[2][1] + 2) % 3),
                (cube[5][0], (cube[5][1] + 1) % 3)
            ]

        if face == 'R':
            cube = [
                (cube[0][0], cube[0][1]),
                (cube[2][0], (cube[2][1] + 1) % 3),
                (cube[5][0], (cube[5][1] + 2) % 3),
                (cube[3][0], cube[3][1]),
                (cube[1][0], (cube[1][1] + 2) % 3),
                (cube[4][0], (cube[4][1] + 1) % 3),
                (cube[6][0], cube[6][1])
            ]

    return cube

def do_sequence (cube, sequence):
    for move in sequence:
        cube = do_move(cube, move)
    return cube

def generate_phase_lookup_table (cube, allowed_moves, max_moves):
    # A phase lookup table is a dictionary where the keys are stringified cube states
    # and values are optimal solution sequences; initialized here with solved cube and
    # optimal zero-move "solution"
    phase_lookup_table = { str(cube): [] }

    # The helper table is a list of lists; the list at index 0 is all cube states
    # reachable in zero moves, the list at index 1 will be all cube states reachable
    # in one move, and so on; this enables breadth-first searching so the first time
    # we see any given cube position we know we reached it in optimal move count;
    # initialized here with the only cube state reachable in zero moves
    helper_table = [ [ { 'cube': cube, 'sequence': [] } ] ]

    for i in range(0, max_moves):
        helper_table.append([])
        
        # Loop through positions generated in previous step (i.e. positions reachable
        # in i moves), execute each of the allowed moves from each position to generate
        # all positions reachable in i + 1 moves
        for previous in helper_table[i]:
            for move in allowed_moves:
                if len(previous['sequence']) == 0 or previous['sequence'][0][0] != move[0]:
                    current = {
                        'cube': do_move(previous['cube'], move, True), # inverse move
                        'sequence': previous['sequence'].copy()
                    }
                    current['sequence'].insert(0, move)

                    # only save the position if we haven't seen it before
                    key = str(current['cube'])
                    if key not in phase_lookup_table:
                        phase_lookup_table[key] = current['sequence']
                        helper_table[i + 1].append(current)

    return phase_lookup_table

# The phase 1 lookup table is generated with a cube that doesn't track corner
# permutation (the first value of each tuple is zero); this generates all the
# possible cases for corner orientation (3^6 or 729 cases) and records optimal
# sequences for orienting them on the U/D axis (domino reduction)
phase_1_lookup_table = generate_phase_lookup_table(
    [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)],
    ['U1', 'U2', 'U3', 'F1', 'F2', 'F3', 'R1', 'R2', 'R3'],
    6
)

# The phase 2 lookup table is generated with a normal cube but a reduced move
# set (the moves that preserve domino reduction); this generates all the possible
# cases for corner permutation where corners are oriented (7! or 5040 cases) and
# records optimal sequences for solving them
phase_2_lookup_table = generate_phase_lookup_table(
    [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0)],
    ['U1', 'U2', 'U3', 'F2', 'R2'],
    13
)

# The rest of the code just uses the lookup table to find and print the solution
# to some scramble; replace this with whatever scramble you'd like to solve :-)
scramble_sequence = "R2 F U R2 U' R U2 F' R"
scrambled_cube = do_sequence(cube, scramble_sequence.split(' '))
scrambled_cube_orientation_only = list(map(lambda n: (0, n[1]), scrambled_cube))
phase_1_solution = phase_1_lookup_table[str(scrambled_cube_orientation_only)]
scrambled_cube = do_sequence(scrambled_cube, phase_1_solution)
phase_2_solution = phase_2_lookup_table[str(scrambled_cube)]

print('Scramble: ' + scramble_sequence)
print('Phase 1: ' + str(phase_1_solution))
print('Phase 2: ' + str(phase_2_solution))