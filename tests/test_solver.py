from cube.cube import Cube
from cube.solver import Solver


class TestSolver:
    def test_solve_scrambled_cube(self):
        cube = Cube()
        # Scramble the cube

        scramble_moves = "R U R' U' L' U' L F' U F"
        cube.apply_moves(scramble_moves)
        assert not cube.is_solved()

        # Solve
        solution = Solver(cube).solve()
        print(f"Solution: {solution}")

        # Verify
        assert cube.is_solved()

    def test_solve_random_scramble(self):
        cube = Cube().reset().scramble()
        assert not cube.is_solved()

        solution = Solver(cube).solve()
        print(f"Solution length: {len(solution)}")

        assert cube.is_solved()
