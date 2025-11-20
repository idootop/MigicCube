# local perspective (for 0 - 3) moves to global moves
movedata = {
    "R": ["R", "B", "L", "F", "R", "R"],
    "R'": ["R'", "B'", "L'", "F'", "R'", "R'"],
    "U": ["U", "U", "U", "U", "F", "B"],
    "U'": ["U'", "U'", "U'", "U'", "F'", "B'"],
    "L": ["L", "F", "R", "B", "L", "L"],
    "L'": ["L'", "F'", "R'", "B'", "L'", "L'"],
    "D": ["D", "D", "D", "D", "B", "F"],
    "D'": ["D'", "D'", "D'", "D'", "B'", "F'"],
    "F": ["F", "R", "B", "L", "D", "U"],
    "F'": ["F'", "R'", "B'", "L'", "D'", "U'"],
    "B": ["B", "L", "F", "R", "U", "D"],
    "B'": ["B'", "L'", "F'", "R'", "U'", "D'"],
    "M": ["M", "S", "M'", "S'", "M", "M"],
    "M'": ["M'", "S'", "M", "S", "M'", "M'"],
    "S": ["S", "M'", "S'", "M", "E", "E'"],
    "S'": ["S'", "M", "S", "M'", "E'", "E"]
}

move_pole_perspective = {
    "R": ["R", "B", "L", "F", "R", "B", "L", "F"],
    "R'": ["R'", "B'", "L'", "F'", "R'", "B'", "L'", "F'"],
    "U": ["F", "R", "B", "L", "B", "L", "F", "R"],
    "U'": ["F'", "R'", "B'", "L'", "B'", "L'", "F'", "R'"],
    "L": ["L", "F", "R", "B", "L", "F", "R", "B"],
    "L'": ["L'", "F'", "R'", "B'", "L'", "F'", "R'", "B'"],
    "D": ["B", "L", "F", "R", "F", "R", "B", "L"],
    "D'": ["B'", "L'", "F'", "R'", "F'", "R'", "B'", "L'"],
    "F": ["D", "D", "D", "D", "U", "U", "U", "U"],
    "F'": ["D'", "D'", "D'", "D'", "U'", "U'", "U'", "U'"],
    "B": ["U", "U", "U", "U", "D", "D", "D", "D"],
    "B'": ["U'", "U'", "U'", "U'", "D'", "D'", "D'", "D'"],
    "M": ["M", "S", "M'", "S'", "M", "S", "M'", "S'"],
    "M'": ["M'", "S'", "M", "S", "M'", "S'", "M", "S"],
    "S": ["E", "E", "E", "E", "E'", "E'", "E'", "E'"],
    "S'": ["E'", "E'", "E'", "E'", "E", "E", "E", "E"]
}

# local perspective (for 0 - 3) positions to global positions
positionTransformData = [
    # target
    [
        # sides
        [[(0, 0, 0), (0, 0, 1), (0, 0, 2)], [(0, 1, 0), (0, 1, 1), (0, 1, 2)], [(0, 2, 0), (0, 2, 1), (0, 2, 2)]],
        [[(1, 0, 0), (1, 0, 1), (1, 0, 2)], [(1, 1, 0), (1, 1, 1), (1, 1, 2)], [(1, 2, 0), (1, 2, 1), (1, 2, 2)]],
        [[(2, 0, 0), (2, 0, 1), (2, 0, 2)], [(2, 1, 0), (2, 1, 1), (2, 1, 2)], [(2, 2, 0), (2, 2, 1), (2, 2, 2)]],
        [[(3, 0, 0), (3, 0, 1), (3, 0, 2)], [(3, 1, 0), (3, 1, 1), (3, 1, 2)], [(3, 2, 0), (3, 2, 1), (3, 2, 2)]],
        [[(4, 0, 0), (4, 0, 1), (4, 0, 2)], [(4, 1, 0), (4, 1, 1), (4, 1, 2)], [(4, 2, 0), (4, 2, 1), (4, 2, 2)]],
        [[(5, 0, 0), (5, 0, 1), (5, 0, 2)], [(5, 1, 0), (5, 1, 1), (5, 1, 2)], [(5, 2, 0), (5, 2, 1), (5, 2, 2)]]
    ],
    [
        [[(1, 0, 0), (1, 0, 1), (1, 0, 2)], [(1, 1, 0), (1, 1, 1), (1, 1, 2)], [(1, 2, 0), (1, 2, 1), (1, 2, 2)]],
        [[(2, 0, 0), (2, 0, 1), (2, 0, 2)], [(2, 1, 0), (2, 1, 1), (2, 1, 2)], [(2, 2, 0), (2, 2, 1), (2, 2, 2)]],
        [[(3, 0, 0), (3, 0, 1), (3, 0, 2)], [(3, 1, 0), (3, 1, 1), (3, 1, 2)], [(3, 2, 0), (3, 2, 1), (3, 2, 2)]],
        [[(0, 0, 0), (0, 0, 1), (0, 0, 2)], [(0, 1, 0), (0, 1, 1), (0, 1, 2)], [(0, 2, 0), (0, 2, 1), (0, 2, 2)]],
        [[(4, 0, 2), (4, 1, 2), (4, 2, 2)], [(4, 0, 1), (4, 1, 1), (4, 2, 1)], [(4, 0, 0), (4, 1, 0), (4, 2, 0)]],
        [[(5, 2, 0), (5, 1, 0), (5, 0, 0)], [(5, 2, 1), (5, 1, 1), (5, 0, 1)], [(5, 2, 2), (5, 1, 2), (5, 0, 2)]]
    ],
    [
        [[(2, 0, 0), (2, 0, 1), (2, 0, 2)], [(2, 1, 0), (2, 1, 1), (2, 1, 2)], [(2, 2, 0), (2, 2, 1), (2, 2, 2)]],
        [[(3, 0, 0), (3, 0, 1), (3, 0, 2)], [(3, 1, 0), (3, 1, 1), (3, 1, 2)], [(3, 2, 0), (3, 2, 1), (3, 2, 2)]],
        [[(0, 0, 0), (0, 0, 1), (0, 0, 2)], [(0, 1, 0), (0, 1, 1), (0, 1, 2)], [(0, 2, 0), (0, 2, 1), (0, 2, 2)]],
        [[(1, 0, 0), (1, 0, 1), (1, 0, 2)], [(1, 1, 0), (1, 1, 1), (1, 1, 2)], [(1, 2, 0), (1, 2, 1), (1, 2, 2)]],
        [[(4, 2, 2), (4, 2, 1), (4, 2, 0)], [(4, 1, 2), (4, 1, 1), (4, 1, 0)], [(4, 0, 2), (4, 0, 1), (4, 0, 0)]],
        [[(5, 2, 2), (5, 2, 1), (5, 2, 0)], [(5, 1, 2), (5, 1, 1), (5, 1, 0)], [(5, 0, 2), (5, 0, 1), (5, 0, 0)]]
    ],
    [
        [[(3, 0, 0), (3, 0, 1), (3, 0, 2)], [(3, 1, 0), (3, 1, 1), (3, 1, 2)], [(3, 2, 0), (3, 2, 1), (3, 2, 2)]],
        [[(0, 0, 0), (0, 0, 1), (0, 0, 2)], [(0, 1, 0), (0, 1, 1), (0, 1, 2)], [(0, 2, 0), (0, 2, 1), (0, 2, 2)]],
        [[(1, 0, 0), (1, 0, 1), (1, 0, 2)], [(1, 1, 0), (1, 1, 1), (1, 1, 2)], [(1, 2, 0), (1, 2, 1), (1, 2, 2)]],
        [[(2, 0, 0), (2, 0, 1), (2, 0, 2)], [(2, 1, 0), (2, 1, 1), (2, 1, 2)], [(2, 2, 0), (2, 2, 1), (2, 2, 2)]],
        [[(4, 2, 0), (4, 1, 0), (4, 0, 0)], [(4, 2, 1), (4, 1, 1), (4, 0, 1)], [(4, 2, 2), (4, 1, 2), (4, 0, 2)]],
        [[(5, 0, 2), (5, 1, 2), (5, 2, 2)], [(5, 0, 1), (5, 1, 1), (5, 2, 1)], [(5, 0, 0), (5, 1, 0), (5, 2, 0)]]
    ]
]

# white edge - other color pairs
whiteEdgePairs = {
    (0, 0, 1): (5, 2, 1),
    (0, 1, 2): (1, 1, 0),
    (0, 2, 1): (4, 0, 1),
    (0, 1, 0): (3, 1, 2),
    (5, 0, 1): (2, 0, 1),
    (5, 1, 2): (1, 0, 1),
    (5, 2, 1): (0, 0, 1),
    (5, 1, 0): (3, 0, 1)
}

# moves for aligning the identified white edge to the correct global slot (if position is global), else local slot (if position is local) 
# as long as the relative orientation is matching
# more efficient than the proper version as i removed redundant "Dx" moves in the end
whiteEdgeDirectMoves = {
    (0, 0, 1): ["FDR'", "FR'F'", "DF'LF", "F'LF"],
    (0, 1, 2): ["DR'", "R'", "D'R'", "F2LF2"],
    (0, 2, 1): ["F'DR'", "F'R'", "F'D'R'", "FL"],
    (0, 1, 0): ["D'L", "F2R'F2", "DL", "L"],
    (5, 0, 1): ["U2F2", "UR2", "B2", "U'L2"],
    (5, 1, 2): ["UF2", "R2", "U'B2", "U2L2"],
    (5, 2, 1): ["F2", "U'R2", "U2B2", "UL2"],
    (5, 1, 0): ["U'F2", "U2R2", "UB2", "L2"]
}

# proper moves for the alignment (without removal of any redundant "Dx"s)
whiteEdgeDirectMovesProper = {
    (0, 0, 1): ["FDR'D'", "FR'F'", "DF'LFD'", "F'LF"],
    (0, 1, 2): ["DR'D'", "R'", "D'R'D", "F2LF2"],
    (0, 2, 1): ["F'DR'D'", "F'R'", "F'D'R'D", "FL"],
    (0, 1, 0): ["D'LD", "F2R'F2", "DLD'", "L"],
    (5, 0, 1): ["U2F2", "UR2", "B2", "U'L2"],
    (5, 1, 2): ["UF2", "R2", "U'B2", "U2L2"],
    (5, 2, 1): ["F2", "U'R2", "U2B2", "UL2"],
    (5, 1, 0): ["U'F2", "U2R2", "UB2", "L2"]
}

LyreLookUpSystem = {
    "corners": [
        ((5, 0, 0), (3, 0, 0), (2, 0, 2), 1),
        ((5, 0, 2), (2, 0, 0), (1, 0, 2), 3),
        ((5, 2, 2), (1, 0, 0), (0, 0, 2), 5),
        ((5, 2, 0), (0, 0, 0), (3, 0, 2), 7)
    ],
    "corners-down": [
        ((4, 2, 0), (2, 2, 2), (3, 2, 0), 1),
        ((4, 2, 2), (1, 2, 2), (2, 2, 0), 3),
        ((4, 0, 2), (0, 2, 2), (1, 2, 0), 5),
        ((4, 0, 0), (3, 2, 2), (0, 2, 0), 7),
    ],
    "edges": [
        ((5, 0, 1), (2, 0, 1), 2),
        ((5, 1, 2), (1, 0, 1), 4),
        ((5, 2, 1), (0, 0, 1), 6),
        ((5, 1, 0), (3, 0, 1), 8)
    ],
    "edges-mid": [
        ((3, 1, 2), (0, 1, 0)),
        ((0, 1, 2), (1, 1, 0)),
        ((1, 1, 2), (2, 1, 0)),
        ((2, 1, 2), (3, 1, 0))
    ],
    "f2ldb": [
        ["1a", "U", "E", 1, 3, "U2RUR'URU'R'"],
        ["1a", "U", "E", 0, 3, "URU2R'URU'R'"],
        ["1a", "U", "X", 1, 3, "yU'L'U2LU'L'ULy'"],
        ["1a", "U", "X", 0, 3, "yU2L'U'LU'L'ULy'"],
        ["1a", "U", "E", 1, 1, "UFR'F'RURUR'"],
        ["1a", "U", "E", 0, 1, "RU2R'U'RUR'"],
        ["1a", "U", "X", 1, 1, "yL'U2LUL'U'Ly'"],
        ["1a", "U", "X", 0, 1, "FURU'R'F'RU'R'"],

        ["1a", "L", "E", 1, 3, "yUL'U'LU2L'ULy'"],
        ["1a", "L", "E", 0, 3, "yUL'U2LU2L'ULy'"],
        ["1a", "L", "X", 1, 3, "U'RUR'URUR'"],
        ["1a", "L", "X", 0, 3, "RUR'"],
        ["1a", "L", "E", 1, 1, "yU'L'ULy'"],
        ["1a", "L", "E", 0, 1, "RU'R'U2yL'U'Ly'"],
        ["1a", "L", "X", 1, 1, "R'U2R2UR'2UR"],
        ["1a", "L", "X", 0, 1, "U'RU'R'URUR'"],

        ["1a", "R", "E", 1, 3, "U'RU2R'U2RU'R'"],
        ["1a", "R", "E", 0, 3, "U'RUR'U2RU'R'"],
        ["1a", "R", "X", 1, 3, "yL'U'Ly'"],
        ["1a", "R", "X", 0, 3, "yUL'U'LU'L'U'Ly'"],
        ["1a", "R", "E", 1, 1, "UR'FRF'URUR'"],
        ["1a", "R", "E", 0, 1, "URU'R'"],
        ["1a", "R", "X", 1, 1, "yUL'ULU'L'U'Ly'"],
        ["1a", "R", "X", 0, 1, "yLU2L'2U'L2U'L'y'"],


        ["1b1", "U", "E", "URU'R'URU'R'URU'R'"],
        ["1b1", "U", "X", "U'R'FRF'RU'R'"],

        ["1b1", "L", "E", "URUR'U2RUR'"],
        ["1b1", "L", "X", "UF'U'FU'RUR'"],
        
        ["1b1", "R", "E", "U'RU'R'U2RU'R'"],
        ["1b1", "R", "X", "U'RUR'UyL'ULy'"],

        ["1b2", "D", "R", "U'R'FRF'RUR'"],
        ["1b2", "D", "L", "URU'R'U'yL'ULy'"],

        ["1b2", "L", "R", "RUR'U'RUR'"],
        ["1b2", "L", "L", "yL'ULU'L'ULy'"],

        ["1b2", "R", "R", "RU'R'URU'R'"],
        ["1b2", "R", "L", "yL'U'LUL'U'Ly'"],
    ]
}

ScythePatternMatcher = {
    "target": [
        (2, 0, 2), (2, 0, 1), (2, 0, 0),
        (3, 0, 0), (5, 0, 0), (5, 0, 1), (5, 0, 2), (1, 0, 2),
        (3, 0, 1), (5, 1, 0), (5, 1, 1), (5, 1, 2), (1, 0, 1),
        (3, 0, 2), (5, 2, 0), (5, 2, 1), (5, 2, 2), (1, 0, 0),
        (0, 0, 0), (0, 0, 1), (0, 0, 2)
    ],
    # corners oriented
    "xyx-xyxyx-yxyyx-xyyyx-xxx": "M'UMU2M'UM",
    "xyx-xyxyx-xyyyx-xyxyx-xyx": "RUR'U'M'URU'Rw'",
    # cross
    "yxy-xxyxx-xyyyx-xxyxx-yxy": "RU2R'U'RUR'U'RU'R'",
    "xxy-yxyxx-xyyyx-yxyxx-xxy": "RU2R2U'R2U'R2U2R",
    "yxy-xxyxx-xyyyx-xyyyx-xxx": "R2D'RU2R'DRU2R",
    "yxx-xxyyx-xyyyx-xxyyx-yxx": "RwUR'U'Rw'FRF'",
    "xxx-yxyyx-xyyyx-xyyxx-xxy": "F'RwUR'U'Rw'FR",
    "xxx-yxyyx-xyyyx-xxyxy-yxx": "RU2R'U'RU'R'",
    "yxx-xxyxy-xyyyx-xyyxx-xxy": "RUR'URU2R'",
    # dot
    "xyx-xyxyx-yxyxy-xyxyx-xyx": "Rw'RURUR'U'Rw2R'2URU'Rw'",
    "yyx-xxxxy-yxyxy-yxxyx-xyx": "FwRUR'U'Fw'U'FRUR'U'F'",
    "xyx-yxxyx-yxyxy-xxxxy-yyx": "FwRUR'U'Fw'UFRUR'U'F'",
    "xyy-xyxxx-yxyxy-yxxyx-xyx": "RUR'UR'FRF'U2R'FRF'",
    "xyx-xyxyx-yxyxy-yxxxy-xyx": "Rw'RURUR'U'RwxR'2URU'x'",
    "yyy-xxxxx-yxyxy-xyxyx-xyx": "FRUR'Uy'R'U2R'FRF'",
    "xyy-yxxxx-yxyxy-yxxxx-xyy": "FRUR'U'SRUR'U'Fw'",
    "xyx-yxxxy-yxyxy-yxxxy-xyx": "RU2R'2FRF'U'2R'FRF'",
    # T
    "yyx-xxxyx-xyyyx-xxxyx-yyx": "RUR'U'R'FRF'",
    "xyx-yxxyx-xyyyx-yxxyx-xyx": "FRUR'U'F'",
    # P
    "xyx-yxxyx-yxyyx-yxyyx-xxx": "FwRUR'U'Fw'",
    "xyx-xyxxy-xyyxy-xyyxy-xxx": "Fw'L'U'LUFw",
    "yyx-xxxyx-yxyyx-xxyyx-yxx": "RDwL'Dw'R'ULwULw'",
    "yxx-xxyyx-yxyyx-xxxyx-yyx": "R'U'FURU'R'F'R",
    # W
    "yxx-xxyyx-xyyxy-xyxxy-xyx": "RUR'URU'R'U'R'FRF'",
    "xxy-xyyxx-yxyyx-yxxyx-xyx": "L'U'LU'L'ULULF'L'F",
    # L
    "xxx-yxyxy-yxyyx-yxxxy-xyx": "RwUR'URU'R'URU'2Rw'",
    "xyx-yxxxy-yxyyx-yxyxy-xxx": "Rw'U'RU'R'URU'R'U2Rw",
    "xyy-yxxxx-yxyyx-yxyxx-xxy": "RB'RBR'2U2FR'F'R",
    "xxy-yxyxx-yxyyx-yxxxx-xyy": "R'FR'F'R2U2yR'FRF'",
    "xxy-yxyxx-xyyxy-yxxxx-xyy": "FRUR'U'RUR'U'F'",
    "yxx-xxyxy-yxyyx-xxxxy-yyx": "F'L'U'LUL'U'LUF",
    # big lightning bolts
    "yyx-xxxyx-xyyyx-xyxxy-xyx": "LF'L'U'LUFU'L'",
    "xyy-xyxxx-xyyyx-yxxyx-xyx": "R'FRUR'U'F'UR",
    # C
    "xyx-yxxxy-xyyyx-xyxyx-xyx": "RUR'2U'R'FRURU'F'",
    "xxx-xyyxy-yxyxy-xyyxy-xxx": "R'U'R'FRF'UR",
    # Squares
    "yyx-xxxxy-yxyyx-yxyyx-xxx": "Rw'U2RUR'URw",
    "xxx-yxyyx-yxyyx-xxxxy-yyx": "RwU2R'U'RU'Rw'",
    # small lightning bolts
    "yxx-xxyxy-xyyxy-xyxxx-xyy": "RwUR'URU2Rw'",
    "xyy-yxxxx-xyyxy-xxyyx-yxx": "MU2R'U'RU'R'U2RUM'",
    "xyy-xyxxx-xyyxy-xxyxy-yxx": "Rw'U'RU'R'U2Rw",
    "yyx-xxxxy-yxyyx-xyyxx-xxy": "Rw'R2UR'URU2R'UM'",
    # fish
    "xxx-xyyxy-xyyxy-xxxyx-yyx": "FRU'R'U'RUR'F'",
    "xyx-xyxxy-yxyyx-xxyyx-yxx": "RU2R2FRF'RU2R'",
    "yyx-xxxyx-xyyxy-yxyxx-xxy": "RUR'UR'FRF'RU2R'",
    "xxy-yxyxx-xyyxy-xxxyx-yyx": "RUR'U'R'FR2UR'U'F'",
    # I
    "xyy-yxxxx-xyyyx-yxxxx-xyy": "FwRUR'U'RUR'U'Fw'",
    "yxx-xxyxy-yxyxy-xxyxy-yxx": "RUR'URDw'RU'R'F'",
    "yxy-xxyxx-yxyxy-xxyxx-yxy": "FwRUR'U'Fw'FRUR'U'RUR'U'F'",
    "xxx-yxyxy-yxyxy-yxyxy-xxx": "RU2R2U'RU'R'U2FRF'",
    # knight moves
    "yyx-xxxxy-xyyyx-xyxxx-xyy": "RwU'Rw'U'RwURw'y'R'UR",
    "xyx-yxxyx-xyyyx-xxxxy-yyx": "RwURw'RUR'U'RwU'Rw'",
    "xyy-yxxxx-xyyyx-xxxyx-yyx": "R'FRUR'F'Ry'RU'R'",
    "xyx-xyxxy-xyyyx-yxxxx-xyy": "Lw'U'LwL'U'LULw'ULw",
    # awkward
    "xyx-xyxyx-yxyyx-xxyxx-yxy": "RU'R'U2RUyRU'R'U'F'",
    "xyx-xyxyx-yxyyx-yxyxy-xxx": "R'2UR'B'RU'R'2ULwULw'",
    "xyx-xyxyx-xyyxy-xxyxx-yxy": "L'ULU'2L'U'y'L'ULUF",
    "xyx-xyxyx-xyyxy-yxyxy-xxx": "L2U'LBL'UL2U'Rw'U'Rw"
}

RunePatternMatcher = {
    "shufflemap": [
        {"G": "G", "O": "O", "B": "B", "R": "R"},
        {"G": "G", "O": "O", "B": "R", "R": "B"},
        {"G": "G", "O": "B", "B": "O", "R": "R"},
        {"G": "G", "O": "B", "B": "R", "R": "O"},
        {"G": "G", "O": "R", "B": "O", "R": "B"},
        {"G": "G", "O": "R", "B": "B", "R": "O"},
        {"G": "O", "O": "G", "B": "B", "R": "R"},
        {"G": "O", "O": "G", "B": "R", "R": "B"},
        {"G": "O", "O": "B", "B": "G", "R": "R"},
        {"G": "O", "O": "B", "B": "R", "R": "G"},
        {"G": "O", "O": "R", "B": "G", "R": "B"},
        {"G": "O", "O": "R", "B": "B", "R": "G"},
        {"G": "B", "O": "G", "B": "O", "R": "R"},
        {"G": "B", "O": "G", "B": "R", "R": "O"},
        {"G": "B", "O": "O", "B": "G", "R": "R"},
        {"G": "B", "O": "O", "B": "R", "R": "G"},
        {"G": "B", "O": "R", "B": "G", "R": "O"},
        {"G": "B", "O": "R", "B": "O", "R": "G"},
        {"G": "R", "O": "G", "B": "O", "R": "B"},
        {"G": "R", "O": "G", "B": "B", "R": "O"},
        {"G": "R", "O": "O", "B": "G", "R": "B"},
        {"G": "R", "O": "O", "B": "B", "R": "G"},
        {"G": "R", "O": "B", "B": "G", "R": "O"},
        {"G": "R", "O": "B", "B": "O", "R": "G"}
    ],
    "target": [
        (2, 0, 2), (2, 0, 1), (2, 0, 0),
        (1, 0, 2), (1, 0, 1), (1, 0, 0),
        (0, 0, 2), (0, 0, 1), (0, 0, 0),
        (3, 0, 2), (3, 0, 1), (3, 0, 0)
    ],
    # permutations of edges only
    "BBBOGOGRGROR": "R2URUR'U'R'U'R'UR'",
    "BRBOGOGOGRBR": "M'2UM'2UM'U2M'2U2M'",
    "BBBOROGOGRGR": "RU'RURURU'R'U'R2",
    "OROGBGRORBGB": "M'2UM'2U2M'2UM'2",
    # permutations of corners only
    "GOGRGBORRBBO": "xR'UR'D2RU'R'D2R2x'",
    "BOGRGOGRBOBR": "x'RU'R'DRUR'D'RUR'DRU'R'D'x",
    "ROBOGOGRRBBG": "xR'2D2RUR'D2RU'Rx'",
    # swap one set of adjacent corners
    "BROGOBOGGRBR": "RU'R'U'RURDR'U'RD'R'U2R'",
    "ORRBOOGGGRBB": "R'UL'U2RU'R'U2RL",
    "OOGRBOGRRBGB": "RUR'U'R'FR2U'R'U'RUR'F'",
    "GOBORGRGRBBO": "R'U2RU'2R'FRUR'U'R'F'R2",
    "OOGRROGGRBBB": "RUR'F'RUR'U'R'FR2U'R'",
    "BGOGOBOBGRRR": "R'U'F'RUR'U'R'FR2U'R'U'RUR'UR",
    # swap one set of diagonal corners
    "RGOGOBORRBBG": "R'UR'U'yR'F'R2U'R'UR'FRF",
    "OORBBGRROGGB": "RUR'URUR'F'RUR'U'R'FR2U'R'U2RU'R'",
    "RBOGGBORRBOG": "FRU'R'U'RUR'F'RUR'U'R'FRF'",
    "ROOGBBORRBGG": "R'URU'R'F'U'FRUR'FR'F'RU'R",
    # G permutations (double cycles)
    "GBRBOGRRBOGO": "R2UR'UR'U'RU'R2DU'R'URD'",
    "GRRBOGRGBOBO": "R2U'RU'RUR'UR2D'URU'R'D",
    "OROGORBBGRGB": "F'U'FR2UwR'URU'RUw'R'2",
    "GBRBGGROBORO": "D'RUR'U'DR2U'RU'R'UR'UR2",
}