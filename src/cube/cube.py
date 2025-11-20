"""
三阶魔方类
"""

import random
from typing import Optional

from .core.cube import Cube as CoreCube
from .solver import Solver
from .typing import Color, Face, Move

INITIAL_CUBE_STR = "R" * 9 + "B" * 9 + "G" * 9 + "Y" * 9 + "W" * 9 + "O" * 9


class Cube(CoreCube):
    """三阶魔方类"""

    def __init__(self, colors: Optional[str] = None):
        super().__init__(Face.str_to_core_cube(colors) or "None")

    def reset(self):
        """重置魔方到初始状态"""
        return super().__init__()

    def is_solved(self) -> bool:
        """检查魔方是否已还原"""
        return str(self) == INITIAL_CUBE_STR

    def moves(self, ops: str):
        """应用一系列转动操作"""
        moves = Move.to_core(ops)
        return super().doMoves(moves)

    def scramble(self, moves_count: int = 100):
        """打乱魔方"""
        moves = [m.value for m in Move]
        moves = random.choices(moves, k=moves_count)
        ops = " ".join(moves)
        self.moves(ops)
        return ops

    def solve(self):
        """解决魔方"""
        solver = Solver(self)
        solution = solver.solve()
        self.moves(solution.ops)
        return solution

    def __str__(self) -> str:
        """获取魔方状态的字符串表示"""
        return Face.core_cube_to_str(self.cube)

    def visualize(self):
        """
        按面打印魔方状态，标准展开图格式：
              上(U)
        左(L) 前(F) 右(R) 后(B)
              下(D)
        """
        print()
        print(Color.to_chinese(Color.from_core(super().__str__())))
        print()
