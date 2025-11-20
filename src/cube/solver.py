from .core.solver import Solver as CoreSolver
from .typing import Solution


class Solver(CoreSolver):
    def __init__(self, cube):
        super().__init__(cube)

    def solve(self):
        self.solveCube(optimize=True)
        current = -1
        alignmentMoves = ""
        baseCrossMoves = ""
        firstLayerMoves = ""
        ollMoves = ""
        pllMoves = ""
        for form in self.__forms:
            if form == "--align--":
                current = 0
            elif form == "--base--":
                current = 1
            elif form == "--first--":
                current = 2
            elif form == "--oll--":
                current = 3
            elif form == "--pll--":
                current = 4
            else:
                if current == 0:
                    alignmentMoves += form
                elif current == 1:
                    baseCrossMoves += form
                elif current == 2:
                    firstLayerMoves += form
                elif current == 3:
                    ollMoves += form
                elif current == 4:
                    pllMoves += form

        return Solution(
            align=alignmentMoves,
            cross=baseCrossMoves,
            f2l=firstLayerMoves,
            oll=ollMoves,
            pll=pllMoves,
        )
